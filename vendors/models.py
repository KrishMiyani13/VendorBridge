from django.db import models
from django.contrib.auth.models import User


class VendorCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Vendor Categories"

    def __str__(self):
        return self.name


class Vendor(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('blacklisted', 'Blacklisted'),
        ('pending', 'Pending Approval'),
    ]

    # Basic Info
    name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    category = models.ForeignKey(VendorCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='vendors')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # GST Details
    gst_number = models.CharField(max_length=20, blank=True, null=True)
    pan_number = models.CharField(max_length=15, blank=True, null=True)

    # Address
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='India')

    # Contact Person
    contact_person_name = models.CharField(max_length=150)
    contact_person_email = models.EmailField(blank=True)
    contact_person_phone = models.CharField(max_length=20, blank=True)

    # Rating & Notes
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    notes = models.TextField(blank=True)

    # Meta
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_vendors')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.company_name})"

    @property
    def full_address(self):
        parts = [self.address_line1]
        if self.address_line2:
            parts.append(self.address_line2)
        parts.extend([self.city, self.state, self.pincode, self.country])
        return ', '.join(parts)
