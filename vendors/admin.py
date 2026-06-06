from django.contrib import admin
from .models import Vendor, VendorCategory


@admin.register(VendorCategory)
class VendorCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['name', 'company_name', 'email', 'category', 'status', 'rating', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['name', 'company_name', 'email', 'gst_number']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'company_name', 'email', 'phone', 'category', 'status')
        }),
        ('GST & Tax Details', {
            'fields': ('gst_number', 'pan_number'),
            'classes': ('collapse',)
        }),
        ('Address', {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'pincode', 'country'),
            'classes': ('collapse',)
        }),
        ('Contact Person', {
            'fields': ('contact_person_name', 'contact_person_email', 'contact_person_phone'),
            'classes': ('collapse',)
        }),
        ('Rating & Notes', {
            'fields': ('rating', 'notes'),
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
