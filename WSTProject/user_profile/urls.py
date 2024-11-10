from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "profile"
urlpatterns = [
    path('', views.view_profile, name='view_profile'),
    path('update/', views.update_profile, name='update_profile'),
    path('password/update/', views.update_password, name='update_password'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)