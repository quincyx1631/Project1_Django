from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.home, name = "home"),
    path('signin/', views.signin, name ="signin"),
    path('signup/', views.signup, name ="signup"),
    path('signout/', views.signout, name ="signout"),
]