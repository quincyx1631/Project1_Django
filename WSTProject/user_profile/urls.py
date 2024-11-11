from django.urls import path
from . import views

app_name = "profile"
urlpatterns = [
    path('', views.view_profile, name='view_profile'),
    path('update/', views.update_profile, name='update_profile'),
    path('password/update/', views.update_password, name='update_password'),
]