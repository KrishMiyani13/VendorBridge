from django.shortcuts import render
from vendors.models import Vendor
from rfq.models import RFQ
from procurement.models import PurchaseOrder, Invoice

def analytics_dashboard(request):
    context = {
        'vendors_count': Vendor.objects.count(),
        'rfq_count': RFQ.objects.count(),
        'po_count': PurchaseOrder.objects.count(),
        'invoice_count': Invoice.objects.count(),
    }
    return render(request, 'analytics/analytics.html', context)

def analytics(request):
    return render(request, 'analytics/analytics.html')