from django.urls import path
from . import views

urlpatterns = [

    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login_alias'),

    path('signup/',
         views.signup_view,
         name='signup'),

    path('dashboard/',
         views.dashboard_view,
         name='dashboard'),

    path('forgot-password/',
         views.forgot_password_view,
         name='forgot_password'),

    path('reset-password/',
         views.reset_password_view,
         name='reset_password'),

    path('logout/',
         views.logout_view,
         name='logout'),

]