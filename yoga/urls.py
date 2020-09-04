from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('profile-settings', views.update_basic_profile, name='update_basic_profile'),
    path('profile/account-settings', views.account_settings, name= 'account_settings'),



    path('create-studio/',views.create_studio, name='create_studio'),
    path('studios/', views.studios, name='studios'),



    path('studio/<slug:name>/', views.single_studio, name='single_studio'),
    path('studio/edit/<slug:slug>/', views.update_studio, name='update_studio' ),
    path('studio/delete/<int:studio_image_id>/', views.delete_studio_image, name='delete_studio_image'),

    path('create-class/', views.create_class, name='create'),
    path('class/<slug:name>/', views.display_class, name='display_class'),
    path('class/edit/<slug:slug>/', views.update_class, name='update_class'),
    path('class/delete/<slug:classinfo_id>/', views.delete_classinfo_image, name='delete_classinfo_image'),

    
    path('select-studio', views.figure_out_what_studio, name='figure_out_what_studio'),

    path('create-lesson/<int:studio_id>', views.create_lesson, name='create_lesson'),
    path('lessons/', views.display_lessons, name='display'),
    path('lesson/edit/<int:lesson_id>', views.update_lesson, name='update_lesson'),

    path('testing/',views.testing, name='testing'),

    path("password_reset", views.password_reset_request, name="password_reset"),
    
]
