from django.db import models
from vendors.models import Vendor
from quotations.models import Quotation


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)

    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE
    )

    quotation = models.ForeignKey(
        Quotation,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.po_number


class Invoice(models.Model):
    invoice_number = models.CharField(
        max_length=50,
        unique=True
    )

    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    due_date = models.DateField()

    status = models.CharField(
        max_length=20,
        default='Unpaid'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.invoice_number