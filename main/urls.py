from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('analyze/', views.analyze, name='analyze'),
    path('analysis/delete/<int:analysis_id>/', views.delete_analysis, name='delete_analysis'),
    path('products/', views.product_list, name='product_list'),
    path('mpesa/', views.mpesa_pay, name='mpesa_pay'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('analysis/results/<int:analysis_id>/', views.analysis_results, name='analysis_results'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_qty, name='update_cart_qty'),
    path('cart/checkout/', views.checkout, name='checkout'),
    path('order/success/', views.order_success, name='order_success'),
]
