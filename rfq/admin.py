from django.contrib import admin
from .models import RFQ, RFQItem, RFQAttachment, RFQVendorAssignment


class RFQItemInline(admin.TabularInline):
    model = RFQItem
    extra = 1
    fields = ['product_name', 'quantity', 'unit', 'specifications']


class RFQVendorAssignmentInline(admin.TabularInline):
    model = RFQVendorAssignment
    extra = 0
    readonly_fields = ['assigned_at']


@admin.register(RFQ)
class RFQAdmin(admin.ModelAdmin):
    list_display = ['rfq_number', 'title', 'status', 'deadline', 'created_by', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['rfq_number', 'title']
    readonly_fields = ['rfq_number', 'created_at', 'updated_at']
    inlines = [RFQItemInline, RFQVendorAssignmentInline]


@admin.register(RFQItem)
class RFQItemAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'rfq', 'quantity', 'unit']
    search_fields = ['product_name', 'rfq__rfq_number']
