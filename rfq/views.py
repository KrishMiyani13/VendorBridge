from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone

from .models import RFQ, RFQItem, RFQVendorAssignment, RFQAttachment
from .forms import RFQForm, RFQItemFormSet, VendorAssignmentForm
from vendors.models import Vendor


@login_required
def rfq_list(request):
    rfqs = RFQ.objects.select_related('created_by').prefetch_related('items', 'vendor_assignments').all()

    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '')

    if search:
        rfqs = rfqs.filter(Q(title__icontains=search) | Q(rfq_number__icontains=search))
    if status:
        rfqs = rfqs.filter(status=status)

    context = {
        'rfqs': rfqs,
        'search': search,
        'status': status,
        'status_choices': RFQ.STATUS_CHOICES,
        'total': rfqs.count(),
        'open_count': rfqs.filter(status='open').count(),
        'draft_count': rfqs.filter(status='draft').count(),
        'awarded_count': rfqs.filter(status='awarded').count(),
    }
    return render(request, 'rfq/rfq_list.html', context)


@login_required
def create_rfq(request):
    if request.method == 'POST':
        form = RFQForm(request.POST)
        formset = RFQItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            rfq = form.save(commit=False)
            rfq.created_by = request.user
            rfq.save()

            formset.instance = rfq
            formset.save()

            # Handle file attachments
            for f in request.FILES.getlist('attachments'):
                RFQAttachment.objects.create(rfq=rfq, file=f, uploaded_by=request.user)

            messages.success(request, f'RFQ "{rfq.rfq_number}" created successfully!')
            return redirect('rfq:rfq_details', pk=rfq.pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = RFQForm()
        formset = RFQItemFormSet()

    return render(request, 'rfq/create_rfq.html', {
        'form': form,
        'formset': formset,
        'title': 'Create RFQ',
    })


@login_required
def rfq_details(request, pk):
    rfq = get_object_or_404(
        RFQ.objects.prefetch_related('items', 'vendor_assignments__vendor', 'attachments'),
        pk=pk
    )
    context = {
        'rfq': rfq,
        'items': rfq.items.all(),
        'assignments': rfq.vendor_assignments.select_related('vendor').all(),
        'attachments': rfq.attachments.all(),
    }
    return render(request, 'rfq/rfq_details.html', context)


@login_required
def rfq_edit(request, pk):
    rfq = get_object_or_404(RFQ, pk=pk)

    if rfq.status in ['awarded', 'cancelled']:
        messages.warning(request, 'This RFQ cannot be edited in its current status.')
        return redirect('rfq:rfq_details', pk=rfq.pk)

    if request.method == 'POST':
        form = RFQForm(request.POST, instance=rfq)
        formset = RFQItemFormSet(request.POST, instance=rfq)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, f'RFQ "{rfq.rfq_number}" updated successfully!')
            return redirect('rfq:rfq_details', pk=rfq.pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = RFQForm(instance=rfq)
        formset = RFQItemFormSet(instance=rfq)

    return render(request, 'rfq/create_rfq.html', {
        'form': form,
        'formset': formset,
        'rfq': rfq,
        'title': f'Edit {rfq.rfq_number}',
    })


@login_required
def assign_vendor(request, pk):
    rfq = get_object_or_404(RFQ, pk=pk)
    already_assigned = rfq.vendor_assignments.values_list('vendor_id', flat=True)
    available_vendors = Vendor.objects.filter(status='active').exclude(id__in=already_assigned)

    if request.method == 'POST':
        vendor_ids = request.POST.getlist('vendors')
        assigned_count = 0
        for vid in vendor_ids:
            vendor = Vendor.objects.filter(pk=vid).first()
            if vendor:
                RFQVendorAssignment.objects.get_or_create(
                    rfq=rfq,
                    vendor=vendor,
                    defaults={'assigned_by': request.user}
                )
                assigned_count += 1

        if assigned_count:
            # Update status to open if draft
            if rfq.status == 'draft':
                rfq.status = 'open'
                rfq.save()
            messages.success(request, f'{assigned_count} vendor(s) assigned to {rfq.rfq_number}!')
        else:
            messages.warning(request, 'No new vendors were assigned.')
        return redirect('rfq:rfq_details', pk=rfq.pk)

    return render(request, 'rfq/assign_vendor.html', {
        'rfq': rfq,
        'available_vendors': available_vendors,
        'assigned_vendors': rfq.vendor_assignments.select_related('vendor').all(),
    })


@login_required
def remove_vendor_assignment(request, pk, vendor_pk):
    rfq = get_object_or_404(RFQ, pk=pk)
    assignment = get_object_or_404(RFQVendorAssignment, rfq=rfq, vendor_id=vendor_pk)
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, 'Vendor removed from RFQ.')
    return redirect('rfq:assign_vendor', pk=pk)
