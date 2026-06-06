from django.urls import path
from . import views

app_name = 'rfq'

urlpatterns = [
    path('', views.rfq_list, name='rfq_list'),
    path('create/', views.create_rfq, name='create_rfq'),
    path('<int:pk>/', views.rfq_details, name='rfq_details'),
    path('<int:pk>/edit/', views.rfq_edit, name='rfq_edit'),
    path('<int:pk>/assign-vendors/', views.assign_vendor, name='assign_vendor'),
    path('<int:pk>/assign-vendors/remove/<int:vendor_pk>/', views.remove_vendor_assignment, name='remove_vendor'),
]
