from django.db import models

class Approval(models.Model):
    approver_name = models.CharField(max_length=150)
    level = models.CharField(max_length=50, default='Manager Review')
    status = models.CharField(max_length=20, default='Pending')
    remarks = models.TextField(blank=True)
    rfq_title = models.CharField(max_length=200, default='Office Furniture Q2')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rfq_title} - {self.level} ({self.status})"
