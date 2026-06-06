from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Approval

@login_required
def approval_list(request):
    approvals = Approval.objects.all().order_by('-created_at')
    return render(request, 'approvals/approval_list.html', {'approvals': approvals})

@login_required
def approval_details(request, pk):
    approval = get_object_or_404(Approval, pk=pk)
    if request.method == 'POST':
        remarks = request.POST.get('remarks', '')
        action = request.POST.get('action', '')

        approval.remarks = remarks
        if action == 'approve':
            approval.status = 'Approved'
            messages.success(request, f'Approval for {approval.rfq_title} has been APPROVED!')
        elif action == 'reject':
            approval.status = 'Rejected'
            messages.warning(request, f'Approval for {approval.rfq_title} has been REJECTED.')
        
        approval.save()
        return redirect('approvals:approval_list')

    return render(request, 'approvals/approval_details.html', {'approval': approval})
