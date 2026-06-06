from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Vendor, VendorCategory
from .forms import VendorForm, VendorSearchForm


@login_required
def vendor_list(request):
    vendors = Vendor.objects.select_related('category', 'created_by').all()
    form = VendorSearchForm(request.GET)

    if form.is_valid():
        search = form.cleaned_data.get('search')
        category = form.cleaned_data.get('category')
        status = form.cleaned_data.get('status')

        if search:
            vendors = vendors.filter(
                Q(name__icontains=search) |
                Q(company_name__icontains=search) |
                Q(email__icontains=search) |
                Q(gst_number__icontains=search)
            )
        if category:
            vendors = vendors.filter(category=category)
        if status:
            vendors = vendors.filter(status=status)

    context = {
        'vendors': vendors,
        'form': form,
        'total_vendors': vendors.count(),
        'active_vendors': vendors.filter(status='active').count(),
        'pending_vendors': vendors.filter(status='pending').count(),
        'categories': VendorCategory.objects.all(),
    }
    return render(request, 'vendors/vendor_list.html', context)


@login_required
def vendor_add(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.created_by = request.user
            vendor.save()
            messages.success(request, f'Vendor "{vendor.name}" added successfully!')
            return redirect('vendors:vendor_details', pk=vendor.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = VendorForm()

    return render(request, 'vendors/vendor_add.html', {'form': form, 'title': 'Add Vendor'})


@login_required
def vendor_edit(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)

    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            messages.success(request, f'Vendor "{vendor.name}" updated successfully!')
            return redirect('vendors:vendor_details', pk=vendor.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = VendorForm(instance=vendor)

    return render(request, 'vendors/vendor_edit.html', {'form': form, 'vendor': vendor, 'title': 'Edit Vendor'})


@login_required
def vendor_details(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    rfqs = vendor.rfq_assignments.select_related('rfq').order_by('-assigned_at') if hasattr(vendor, 'rfq_assignments') else []
    quotations = vendor.quotations.select_related('rfq').order_by('-submitted_at') if hasattr(vendor, 'quotations') else []

    context = {
        'vendor': vendor,
        'rfqs': rfqs,
        'quotations': quotations,
    }
    return render(request, 'vendors/vendor_details.html', context)


@login_required
def vendor_delete(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == 'POST':
        name = vendor.name
        vendor.delete()
        messages.success(request, f'Vendor "{name}" deleted successfully.')
        return redirect('vendors:vendor_list')
    return render(request, 'vendors/vendor_confirm_delete.html', {'vendor': vendor})
