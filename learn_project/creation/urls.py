from creation import  views
from django.urls import path
urlpatterns = [
    path('',views.login_view,name='login'),
    path('register', views.register_view,name='register'),
    path('about',views.about,name='about'),

]
