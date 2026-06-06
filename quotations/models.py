from django.db import models

# Create your models here.

class Quotation(models.Model):
    quotation_number = models.CharField(
        max_length=50,
        unique=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.quotation_number