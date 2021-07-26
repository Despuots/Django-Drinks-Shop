"""mysite URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import ProductDetailView, ProductView, add_to_cart, remove_from_cart, OrderSummaryView, remove_single_product_from_cart, featured_view, CheckoutView, product_by_category, PaypalPayment, cart_cleaner, HistoryView


app_name = 'drink_shop'


urlpatterns = [
    path('', featured_view, name='featured_view'),
    path('product_by_category/<slug>', product_by_category, name='product_by_category'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('products/', ProductView.as_view(), name='products'),
    path('user_history/', HistoryView.as_view(), name='user_history'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ProductDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-product-from-cart/<slug>/', remove_single_product_from_cart, name='remove-single-product-from-cart'),
    path('cart_cleaner/', cart_cleaner, name='cart_cleaner'),
    path('paypal/', PaypalPayment.as_view(), name='paypal'),
    path('register/', views.register, name='register'),
]