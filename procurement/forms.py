from django import forms
from .models import PurchaseOrder, Invoice


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'