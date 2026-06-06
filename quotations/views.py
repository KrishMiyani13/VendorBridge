from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Quotation
import random

@login_required
def submit_quotation(request):
    if request.method == 'POST':
        rfq_title = request.POST.get('rfq_title', 'Office Furniture')
        notes = request.POST.get('notes', '')
        status = request.POST.get('status', 'submitted')
        grand_total = request.POST.get('grand_total', '0')
        vendor_name = request.POST.get('vendor_name', 'Demo Vendor')
        gst_percentage = request.POST.get('gst_percentage', '18')
        delivery_days = request.POST.get('delivery_days', '7')
        vendor_rating = request.POST.get('vendor_rating', '4.5')
        payment_terms = request.POST.get('payment_terms', '30 Days')

        count = Quotation.objects.count()
        quotation_number = f"QT-{1000 + count + random.randint(1, 99)}"

        quotation = Quotation.objects.create(
            quotation_number=quotation_number,
            vendor_name=vendor_name,
            rfq_title=rfq_title,
            grand_total=float(grand_total),
            gst_percentage=float(gst_percentage),
            delivery_days=int(delivery_days),
            vendor_rating=float(vendor_rating),
            payment_terms=payment_terms,
            status=status,
            notes=notes
        )

        messages.success(request, f'Quotation {quotation_number} saved successfully!')
        if status == 'draft':
            return redirect('quotations:draft_list')
        else:
            return redirect('quotations:compare_quotations')

    return render(request, 'quotations/quotation_submit.html')

@login_required
def draft_list(request):
    drafts = Quotation.objects.filter(status='draft').order_by('-created_at')
    return render(request, 'quotations/draft_list.html', {'drafts': drafts})

@login_required
def compare_quotations(request):
    quotations = Quotation.objects.filter(status='submitted').order_by('-created_at')
    return render(request, 'quotations/compare.html', {'quotations': quotations})

@login_required
def quotation_details(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    return render(request, 'quotations/quotation_details.html', {'quotation': quotation})

@login_required
def submit_draft(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk, status='draft')
    quotation.status = 'submitted'
    quotation.save()
    messages.success(request, f'Quotation {quotation.quotation_number} submitted successfully!')
    return redirect('quotations:compare_quotations')

@login_required
def delete_draft(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk, status='draft')
    num = quotation.quotation_number
    quotation.delete()
    messages.success(request, f'Draft {num} deleted.')
    return redirect('quotations:draft_list')
