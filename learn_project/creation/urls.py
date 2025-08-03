from . import  views
from django.urls import path
urlpatterns = [
    path('',views.login_view,name='login'),
    path('register', views.register_view,name='register'),
    path('about',views.about,name='about'),
    path('restaurant',views.restaurant,name='restaurant'),

    path('add_to_cart',views.add_to_cart,name='add_to_cart'),
    path('cart',views.cart_view,name='cart_view'),
    path('update_cart',views.update_cart,name='update_cart'),
    path('cart_summary',views.cart_summary, name='cart_summary'),
    path('place_order',views.place_order,name='place_order'),
    path('order_success',views.order_success,name='order_success'),
    path('restaurant_detail/<int:restaurant_id>',views.restaurant_detail,name='restaurant_detail'),


]
