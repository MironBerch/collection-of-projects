from django.urls import path
from .views import *


urlpatterns = [
    path('', home_view, name='home'),
    path('checkout/', checkout_view, name='checkout'),
    path('order-summary/', order_summary_view, name='order-summary'),
    path('product/<slug>/', item_detail_view, name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', add_coupon_view, name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', payment_view, name='payment'),
    path('request-refund/', request_refund_view, name='request-refund')
]