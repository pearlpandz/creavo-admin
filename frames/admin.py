from django.contrib import admin
from .models.type import FrameType
from django.utils.html import format_html

@admin.register(FrameType)
class FrameTypeAdmin(admin.ModelAdmin):
    # Use a method for M2M field instead of the raw field
    list_display = ['image_tag', 'name', 'description', 'order', 'subcategories_list']
    search_fields = ['name', 'description']
    list_filter = ['name']
    list_per_page = 15
    ordering = ['order']
    exclude = ['image']  # optional: if you want to hide the URL field in the form

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:4px;" />',
                obj.image  # Use FileField URL
            )
        return "-"
    image_tag.short_description = 'Image'


    # Display subcategories M2M as a string
    def subcategories_list(self, obj):
        return ", ".join([sub.name for sub in obj.subcategories.all()])
    subcategories_list.short_description = 'Subcategories'

    # Optional: custom delete
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()
