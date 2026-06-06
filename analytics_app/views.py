from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from vendors.models import Vendor
from rfq.models import RFQ
from procurement.models import PurchaseOrder, Invoice

@login_required
def analytics(request):
    context = {
        'vendors_count': Vendor.objects.count(),
        'rfq_count': RFQ.objects.count(),
        'po_count': PurchaseOrder.objects.count(),
        'invoice_count': Invoice.objects.count(),
    }

    return render(
        request,
        'analytics/analytics.html',
        context
    )