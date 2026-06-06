from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from vendors.models import Vendor
from rfq.models import RFQ
from procurement.models import PurchaseOrder, Invoice
from quotations.models import Quotation
from approvals.models import Approval

@login_required
def analytics(request):
    context = {
        'vendors_count': Vendor.objects.count(),
        'rfq_count': RFQ.objects.count(),
        'po_count': PurchaseOrder.objects.count(),
        'invoice_count': Invoice.objects.count(),
        'quotations_count': Quotation.objects.count(),
        'approvals_count': Approval.objects.count(),
    }

    return render(
        request,
        'analytics/analytics.html',
        context
    )