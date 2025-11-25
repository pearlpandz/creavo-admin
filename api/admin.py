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



original_get_urls = admin.site.get_urls

class SubCategoryInline(admin.StackedInline):
    model = SubCategory
    extra = 0

class MediaInline(admin.StackedInline):
    model = Media
    extra = 1
    # filter_horizontal = ('categories', 'subcategories')
    fields = ('title', 'media', 'image', 'short_description', 'rating', 'categories', 'subcategories', 'image_tag')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:4px;" />',
                obj.thumbnail
            )
        return "-"
    image_tag.short_description = 'Image'

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
    list_display = ('image_tag', 'title', 'rating','categories_list', 'subcategory_name')
    filter_horizontal = ('categories',)  # Nice UI for multi-select
    exclude = ['image', 'thumbnail']  # hides the field from the form
    list_per_page = 15

    # def image_tag(self, obj):
    #     if obj.thumbnail:
    #         return format_html('<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:4px;" />', obj.thumbnail)
    #     return "-"
    
    # image_tag.short_description = 'Image'

    def image_tag(self, obj):
        if obj.media:  # <-- changed from obj.thumbnail
            ext = obj.media.name.split('.')[-1].lower()
            if ext in ['jpg', 'jpeg', 'png', 'gif']:
                # For images and GIFs
                return format_html(
                    '<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:4px;" />',
                    obj.media.url
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

    def subcategory_name(self, obj):
        return obj.subcategories.name if obj.subcategories else "-"
    subcategory_name.short_description = "SubCategory"

    def delete_queryset(self, request, queryset):
        print("Call delete() on each object to trigger Node.js cleanup")
        for obj in queryset:
            print(obj)
            obj.delete()


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