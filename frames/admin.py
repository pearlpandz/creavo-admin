from django.contrib import admin
from .models.type import FrameType
from django.utils.html import format_html


# Register your models here.
@admin.register(FrameType)
class EventAdminConfig(admin.ModelAdmin):
    exclude = []
    list_display = ['image_tag', 'name']
    search_fields=['name']
    list_filter=['name']
    list_per_page = 15
    sortable_by=['name']
    ordering = ['order']
    exclude = ['image'] 

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