from django.urls import path
from . import views
from .views import UpdateClassView

urlpatterns = [
    path('', views.home, name='home'),

    path('profile-settings', views.profile_settings, name='profile_settings'),

    path('create-studio/',views.create_studio, name='create_studio'),
    path('studios/', views.studios, name='studios'),
    path('studio/<slug:name>/', views.single_studio, name='single_studio'),
    path('studio/edit/<slug:slug>/', views.update_studio, name='update_studio' ),

    path('create-class/', views.create_class, name='create'),
    path('class/<slug:name>/', views.display_class, name='display_class'),
    path('class/edit/<slug:slug>/', views.UpdateClassView.as_view(), name='update_class'),

    path('create-lesson/', views.create_lesson, name='create_lesson'),
    path('lessons/', views.display_lessons, name='display'),

    path('testing/',views.testing, name='testing'),
    
]

