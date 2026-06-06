from django.urls import path
from . import views

app_name = 'quotations'

urlpatterns = [
    path('', views.submit_quotation, name='submit_quotation'),
    path('drafts/', views.draft_list, name='draft_list'),
    path('compare/', views.compare_quotations, name='compare_quotations'),
    path('<int:pk>/', views.quotation_details, name='quotation_details'),
    path('draft/<int:pk>/submit/', views.submit_draft, name='submit_draft'),
    path('draft/<int:pk>/delete/', views.delete_draft, name='delete_draft'),
]
