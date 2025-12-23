from django.contrib import admin
from django.utils.html import format_html
from api.models.category import Category
from api.models.subcategory import SubCategory
from api.models.media import Media
from api.models.event import Event, EventMedia
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.timezone import now
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.urls import path
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import timedelta
import csv
from django.contrib import messages
from django import forms
from django.template.response import TemplateResponse
from django.contrib.admin.widgets import FilteredSelectMultiple



original_get_urls = admin.site.get_urls

class SubCategoryInline(admin.StackedInline):
    model = SubCategory
    extra = 0

class MediaInline(admin.TabularInline):
    # Use the auto-generated through model for the ManyToMany relation
    model = Media.subcategories.through
    extra = 1
    verbose_name = "Media"
    verbose_name_plural = "Media"
    raw_id_fields = ('media',)

@admin.register(Category)
class CategoryAdminConfig(admin.ModelAdmin):
    exclude = []
    list_display = ['id','name', 'subcategories_list', 'media_count',  'is_active', 'order']
    search_fields=['name']
    list_filter=['name']
    # actions=[make_inactive,make_active]
    list_per_page = 15
    sortable_by=['id','name']
    ordering = ['order', 'id']
    inlines = [SubCategoryInline]

    def subcategories_list(self, obj):
        subcats = obj.subcategories.all()
        if not subcats:
            return "-"
        return ", ".join(subcat.name for subcat in subcats)
    
    subcategories_list.short_description = "Subcategories"

    def media_count(self, obj):
        # Count all Media linked to this category 
        return obj.media.count()
    media_count.short_description = "Media Count"
    

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'media_count' ,'is_active']
    search_fields = ['name']
    list_filter = ['category']
    ordering = ['category', 'name']
    inlines = [MediaInline]

    def media_count(self, obj):
        # Count all Media linked to this subcategory 
        return obj.media.count()
    media_count.short_description = "Media Count"




    
# ✅ Inline for Category (link existing media)
class CategoryMediaInline(admin.TabularInline):
    model = Media.categories.through
    extra = 1
    verbose_name = "Media"
    verbose_name_plural = "Media"

@admin.register(Media)
class MediaAdminConfig(admin.ModelAdmin):
    list_display = ('image_tag', 'title', 'rating','categories_list', 'subcategories_list')
    exclude = ['image', 'thumbnail', 'categories', 'subcategories']  # hide original multi-selects
    form = None  # set below
    list_per_page = 15

    def save_model(self, request, obj, form, change):
        # Ensure combined category_subcategory selections are applied to M2M fields
        super().save_model(request, obj, form, change)
        try:
            selected = form.cleaned_data.get('category_subcategory', [])
        except Exception:
            selected = []

        cat_ids = set()
        sub_ids = set()
        for token in selected:
            if token.startswith('c:'):
                try:
                    cid = int(token.split(':', 1)[1])
                    cat_ids.add(cid)
                except Exception:
                    continue
            elif token.startswith('sc:'):
                try:
                    sid = int(token.split(':', 1)[1])
                    sub_ids.add(sid)
                    try:
                        sc = SubCategory.objects.get(id=sid)
                        if sc.category_id:
                            cat_ids.add(sc.category_id)
                    except SubCategory.DoesNotExist:
                        pass
                except Exception:
                    continue

        if cat_ids or sub_ids:
            obj.categories.set(list(cat_ids))
            obj.subcategories.set(list(sub_ids))

    # def image_tag(self, obj):
    #     if obj.thumbnail:
    #         return format_html('<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:4px;" />', obj.thumbnail)
    #     return "-"
    
    # image_tag.short_description = 'Image'

    def image_tag(self, obj):
        if obj.media:  # <-- changed from obj.thumbnail
            ext = obj.media.name.split('.')[-1].lower()
            if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                # For images and GIFs
                return format_html(
                    '<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:4px;" />',
                    obj.thumbnail
                )
            elif ext in ['mp4', 'mov']:
                # For videos
                return format_html(
                    '<video width="60" height="60" controls>'
                    '<source src="{}" type="video/{}">'
                    '</video>',
                    obj.media.url, ext
                )
        return "-"

    image_tag.short_description = 'Media'
    def categories_list(self, obj):
        return ", ".join([c.name for c in obj.categories.all()])
    categories_list.short_description = "Categories"

    def subcategories_list(self, obj):
        try:
            subs = obj.subcategories.all()
            if not subs:
                return "-"
            return ", ".join([s.name for s in subs])
        except Exception as e:
            return f"Error: {e}"
    subcategories_list.short_description = "SubCategories"

    def delete_queryset(self, request, queryset):
        print("Call delete() on each object to trigger Node.js cleanup")
        for obj in queryset:
            print(obj)
            obj.delete()


# Custom ModelForm to present a single combined multi-select for Category|SubCategory
class MediaAdminForm(forms.ModelForm):
    category_subcategory = forms.MultipleChoiceField(
        required=False,
        widget=FilteredSelectMultiple("Category | SubCategory", is_stacked=False)
    )

    class Meta:
        model = Media
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Build choices: for categories with subcategories, show "Category | Subcategory" per subcategory
        choices = []
        for cat in Category.objects.all().order_by('name'):
            subs = list(cat.subcategories.all())
            if subs:
                for s in subs:
                    choices.append((f"sc:{s.id}", f"{cat.name} | {s.name}"))
            else:
                choices.append((f"c:{cat.id}", f"{cat.name}"))

        self.fields['category_subcategory'].choices = choices

        # Set initial selections from instance
        if self.instance and self.instance.pk:
            initial = []
            sub_ids = set(self.instance.subcategories.values_list('id', flat=True))
            # Mark subcategory selections
            for sid in sub_ids:
                initial.append(f"sc:{sid}")

            # For categories, only include category-level choices if none of its subcategories are selected
            for c in self.instance.categories.all():
                # if category has subcategories and any subcategory of this category is already selected, skip
                cat_subs = set(c.subcategories.values_list('id', flat=True))
                if cat_subs and cat_subs & sub_ids:
                    continue
                initial.append(f"c:{c.id}")

            self.fields['category_subcategory'].initial = initial

    def save(self, commit=True):
        instance = super().save(commit=False)
        selected = self.cleaned_data.get('category_subcategory', [])
        cat_ids = set()
        sub_ids = set()
        for token in selected:
            if token.startswith('c:'):
                try:
                    cid = int(token.split(':', 1)[1])
                    cat_ids.add(cid)
                except Exception:
                    continue
            elif token.startswith('sc:'):
                try:
                    sid = int(token.split(':', 1)[1])
                    sub_ids.add(sid)
                    # ensure parent category is also included
                    try:
                        sc = SubCategory.objects.get(id=sid)
                        if sc.category_id:
                            cat_ids.add(sc.category_id)
                    except SubCategory.DoesNotExist:
                        pass
                except Exception:
                    continue

        if commit:
            instance.save()
            instance.categories.set(list(cat_ids))
            instance.subcategories.set(list(sub_ids))
            self.save_m2m()
        else:
            # store pending m2m for save_m2m later
            self._pending_m2m = (list(cat_ids), list(sub_ids))

        return instance

    def save_m2m(self):
        # handle pending m2m if present
        if hasattr(self, '_pending_m2m'):
            cat_ids, sub_ids = self._pending_m2m
            self.instance.categories.set(cat_ids)
            self.instance.subcategories.set(sub_ids)
        else:
            super().save_m2m()


# attach form to admin
MediaAdminConfig.form = MediaAdminForm

class EventMediaInline(admin.StackedInline):
    model = EventMedia
    extra = 0

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:4px;" />', obj.image)
        return "-"
    
    image_tag.short_description = 'Image'

    def delete_queryset(self, request, queryset):
        print("Call delete() on each object to trigger Node.js cleanup")
        for obj in queryset:
            print(obj)
            obj.delete()

@admin.register(Event)
class EventAdminConfig(admin.ModelAdmin):
    exclude = []
    list_display = ['name', 'date', 'media_count']
    search_fields=['name']
    list_filter=['name']
    # actions=[make_inactive,make_active]
    list_per_page = 15
    sortable_by=['name', 'date']
    ordering = ['date']
    inlines = [EventMediaInline]

    def media_count(self, obj):
        return obj.events.count()

    media_count.short_description = "Media Count"


@staff_member_required
def custom_recent_actions_view(request):
    query = request.GET.get("q", "")
    days = request.GET.get("days", "7")
    page = request.GET.get("page", 1)
    ordering = request.GET.get("ordering", "-action_time")
    action_flag = request.GET.get("action_flag", "")
    export = request.GET.get("export", "")

    logs = LogEntry.objects.all().select_related('user', 'content_type')

    if query:
        logs = logs.filter(
            Q(object_repr__icontains=query) |
            Q(change_message__icontains=query)
        )

    if days.isdigit():
        cutoff = now() - timedelta(days=int(days))
        logs = logs.filter(action_time__gte=cutoff)

    if action_flag in ['1', '2', '3']:
        logs = logs.filter(action_flag=action_flag)

    logs = logs.order_by(ordering)

    if export == "csv":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=admin_actions.csv"
        writer = csv.writer(response)
        writer.writerow(["Time", "User", "Action", "Model", "Object", "Change Message"])
        for log in logs:
            writer.writerow([
                log.action_time,
                log.user,
                log.get_action_flag_display(),
                log.content_type,
                log.object_repr,
                log.get_change_message(),
            ])
        return response

    paginator = Paginator(logs, 20)
    try:
        logs_page = paginator.page(page)
    except PageNotAnInteger:
        logs_page = paginator.page(1)
    except EmptyPage:
        logs_page = paginator.page(paginator.num_pages)

    context = {
        'logs': logs_page,
        'title': "Recent Admin Actions",
        'query': query,
        'days': days,
        'ordering': ordering,
        'action_flag': action_flag,
        'paginator': paginator,
        'page_obj': logs_page,
        'is_paginated': logs_page.has_other_pages(),
    }
    return render(request, 'admin/custom_recent_actions.html', context)

def custom_get_urls():
    custom_urls = [
        path('recent-actions/', custom_recent_actions_view, name='custom_recent_actions')
    ]
    return custom_urls + original_get_urls()

# Register the custom URL
# admin.site.get_urls = lambda: [path('recent-actions/', custom_recent_actions_view, name='custom_recent_actions')] + admin.site.get_urls()
# Override the admin site URLs
admin.site.get_urls = custom_get_urls