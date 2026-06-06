from django.db import models
from django.contrib.auth.models import User
from vendors.models import Vendor


class RFQ(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
        ('awarded', 'Awarded'),
    ]

    # Basic Info
    rfq_number = models.CharField(max_length=20, unique=True, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    # Dates
    issue_date = models.DateField(auto_now_add=True)
    deadline = models.DateField()

    # Meta
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_rfqs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "RFQ"
        verbose_name_plural = "RFQs"

    def __str__(self):
        return f"{self.rfq_number} — {self.title}"

    def save(self, *args, **kwargs):
        if not self.rfq_number:
            from django.utils import timezone
            year = timezone.now().year
            last = RFQ.objects.filter(rfq_number__startswith=f'RFQ-{year}').order_by('-rfq_number').first()
            if last:
                seq = int(last.rfq_number.split('-')[-1]) + 1
            else:
                seq = 1
            self.rfq_number = f'RFQ-{year}-{seq:04d}'
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        from django.utils import timezone
        return self.deadline < timezone.now().date() and self.status == 'open'


class RFQItem(models.Model):
    rfq = models.ForeignKey(RFQ, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50, default='units')
    specifications = models.TextField(blank=True)

    def __str__(self):
        return f"{self.product_name} ({self.quantity} {self.unit})"


class RFQAttachment(models.Model):
    rfq = models.ForeignKey(RFQ, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='rfq_attachments/')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.rfq.rfq_number}"


class RFQVendorAssignment(models.Model):
    rfq = models.ForeignKey(RFQ, on_delete=models.CASCADE, related_name='vendor_assignments')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='rfq_assignments')
    assigned_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    invitation_sent = models.BooleanField(default=False)
    invitation_sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['rfq', 'vendor']

    def __str__(self):
        return f"{self.vendor.name} → {self.rfq.rfq_number}"
