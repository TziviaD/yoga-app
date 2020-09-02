from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
path('login/', LoginView.as_view(template_name='access/login.html'), name='login'),
path('signup/', views.signup, name='signup'),
path('logout/', LogoutView.as_view(), name='logout'), #we dont have a template name cause we are redirecting it to a page

path('owner-invite/<slug:studio_slug>', views.owner_invite, name='owner_invite'),

# Forget Password
path('password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='commons/password-reset/password_reset.html',
            subject_template_name='commons/password-reset/password_reset_subject.txt',
            email_template_name='commons/password-reset/password_reset_email.html',
            # success_url='/login/'
        ),
        name='password_reset'),
path('password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='commons/password-reset/password_reset_done.html'
        ),
        name='password_reset_done'),
path('password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='commons/password-reset/password_reset_confirm.html'
        ),
        name='password_reset_confirm'),
path('password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='commons/password-reset/password_reset_complete.html'
        ),
        name='password_reset_complete'),
]


