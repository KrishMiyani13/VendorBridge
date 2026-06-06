from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from .models import PurchaseOrder, Invoice
from .forms import PurchaseOrderForm, InvoiceForm


# Purchase Orders

def po_list(request):
    pos = PurchaseOrder.objects.all()

    return render(
        request,
        'procurement/po_list.html',
        {'pos': pos}
    )


def create_po(request):
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('procurement:po_list')

    else:
        form = PurchaseOrderForm()

    return render(
        request,
        'procurement/create_po.html',
        {'form': form}
    )


# Invoice List

def invoice_list(request):
    invoices = Invoice.objects.all()

    return render(
        request,
        'procurement/invoice_list.html',
        {'invoices': invoices}
    )


# Create Invoice

def generate_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('procurement:invoice_list')

    else:
        form = InvoiceForm()

    return render(
        request,
        'procurement/generate_invoice.html',
        {'form': form}
    )


# PDF Download

def generate_invoice_pdf(request, invoice_id):
    invoice = get_object_or_404(
        Invoice,
        id=invoice_id
    )

    template = get_template(
        'procurement/invoice_pdf.html'
    )

    html = template.render({
        'invoice': invoice
    })

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'filename="invoice_{invoice.invoice_number}.pdf"'
    )

    pisa.CreatePDF(
        html,
        dest=response
    )

    return response


# Invoices Summary List PDF

def invoice_list_pdf(request):
    invoices = Invoice.objects.all().order_by('-created_at')
    total_registry_sum = sum(inv.total_amount for inv in invoices)

    template = get_template('procurement/invoice_list_pdf.html')
    html = template.render({
        'invoices': invoices,
        'total_registry_sum': total_registry_sum
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoices_list_report.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response


# Consolidated All Invoices Details PDF

def all_invoices_pdf(request):
    invoices = Invoice.objects.all().order_by('-created_at')

    template = get_template('procurement/all_invoices_pdf.html')
    html = template.render({
        'invoices': invoices
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="all_invoices_consolidated.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response