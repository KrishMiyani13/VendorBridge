from django.urls import path
from . import views

app_name = 'procurement'

urlpatterns = [
    path('', views.po_list, name='po_list'),
    path('create/', views.create_po, name='create_po'),
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/create/', views.generate_invoice, name='generate_invoice'),
    path('invoices/<int:invoice_id>/pdf/', views.generate_invoice_pdf, name='generate_invoice_pdf'),
    path('invoices/list-pdf/', views.invoice_list_pdf, name='invoice_list_pdf'),
    path('invoices/all-pdf/', views.all_invoices_pdf, name='all_invoices_pdf'),
]