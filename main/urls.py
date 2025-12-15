from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('analyze/', views.analyze, name='analyze'),
    path('products/', views.product_list, name='product_list'),
    path('mpesa/', views.mpesa_pay, name='mpesa_pay'),
]
