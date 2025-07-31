from creation import  views
from django.urls import path,include
urlpatterns = [
    path('',views.login_view,name='login'),

]
