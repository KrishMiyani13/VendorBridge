from django.contrib import admin
from .models import PurchaseOrder
from .models import Invoice

# Register your models here.

admin.site.register(PurchaseOrder)
admin.site.register(Invoice)