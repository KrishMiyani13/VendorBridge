from django.db import models
from django.contrib.auth.models import User


from django.contrib.auth.models import User
class UserProfile(models.Model):

    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Vendor', 'Vendor'),
        ('Manager', 'Manager'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    phone = models.CharField(
        max_length=10
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    country = models.CharField(
        max_length=50
    )

    photo = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username