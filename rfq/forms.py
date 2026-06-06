from django import forms
from django.forms import inlineformset_factory
from .models import RFQ, RFQItem, RFQVendorAssignment
from vendors.models import Vendor


class RFQForm(forms.ModelForm):
    class Meta:
        model = RFQ
        fields = ['title', 'description', 'deadline', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'RFQ Title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the procurement requirement...',
            }),
            'deadline': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class RFQItemForm(forms.ModelForm):
    class Meta:
        model = RFQItem
        fields = ['product_name', 'description', 'quantity', 'unit', 'specifications']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product/Service Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Item description'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Qty', 'min': 0}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'units / kg / pcs'}),
            'specifications': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Technical specifications'}),
        }


RFQItemFormSet = inlineformset_factory(
    RFQ, RFQItem,
    form=RFQItemForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
)


class VendorAssignmentForm(forms.Form):
    vendors = forms.ModelMultipleChoiceField(
        queryset=Vendor.objects.filter(status='active'),
        widget=forms.CheckboxSelectMultiple(),
        label="Select Vendors to Invite",
    )
