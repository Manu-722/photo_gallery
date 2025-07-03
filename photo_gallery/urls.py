from django.urls import path
from . import views
from .views import email_login_view


app_name = 'photo_gallery'

urlpatterns = [
    path('', views.home, name='home'),
    path('photo/<int:pk>/', views.photo_detail, name='photo_detail'),
    path('photo/<int:pk>/like/', views.like_photo, name='like_photo'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('upload/', views.upload_photo, name='upload_photo'),
    path('register/', views.register, name='register'),
    path('change-password/', views.CustomPasswordChangeView.as_view(), name='change_password'),
    path('most-liked/', views.most_liked_photos, name='most_liked'),
    path('login/', email_login_view, name='login'),

]