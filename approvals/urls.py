from django.urls import path
from . import views

app_name = 'approvals'

urlpatterns = [
    path('', views.approval_list, name='approval_list'),
    path('<int:pk>/', views.approval_details, name='approval_details'),
]
