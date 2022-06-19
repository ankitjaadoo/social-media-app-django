from django.urls import path
from . import views
 
urlpatterns = [
    path('',views.Login),
    path('signup', views.AccountSignup),
    path('login', views.Login),
    path('token', views.GetToken),
    path('auth', views.Auth),
]