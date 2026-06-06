from django.db import models

class Quotation(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    quotation_number = models.CharField(max_length=50, unique=True)
    vendor_name = models.CharField(max_length=200, default='Demo Vendor')
    rfq_title = models.CharField(max_length=200, default='Office Furniture')
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    gst_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=18.0)
    delivery_days = models.IntegerField(default=7)
    vendor_rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    payment_terms = models.CharField(max_length=100, default='30 Days')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quotation_number} - {self.vendor_name} ({self.status})"