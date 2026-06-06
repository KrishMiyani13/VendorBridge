from django.urls import path
from . import views

urlpatterns = [

    path(
        'purchase-orders/',
        views.po_list,
        name='po_list'
    ),

    path(
        'purchase-orders/create/',
        views.create_po,
        name='create_po'
    ),

    path(
        'invoices/',
        views.invoice_list,
        name='invoice_list'
    ),

    path(
        'invoice/create/',
        views.generate_invoice,
        name='generate_invoice'
    ),

    path(
        'invoice/pdf/<int:invoice_id>/',
        views.generate_invoice_pdf,
        name='invoice_pdf'
    ),

]