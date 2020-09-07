from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView



from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
path('login/', LoginView.as_view(template_name='access/login.html'), name='my_login'),
path('signup/', views.signup, name='signup'),
path('logout/', LogoutView.as_view(), name='logout'), #we dont have a template name cause we are redirecting it to a page

path('owner-invite/<slug:studio_slug>', views.owner_invite, name='owner_invite'),
path('teacher-signup/<uidb64>', views.teacher_signup, name='teacher_signup'),


path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),      




#path('accounts/', include('django.contrib.auth.urls')),#i might need to chane the accounts to somthing else..
]


# # Forget Password
# path('password-reset/',
#         auth_views.PasswordResetView.as_view(
#             template_name='commons/password-reset/password_reset.html',
#             subject_template_name='commons/password-reset/password_reset_subject.txt',
#             email_template_name='commons/password-reset/password_reset_email.html',
#             # success_url='/login/'
#         ),
#         name='password_reset'),
# path('password-reset/done/',
#         auth_views.PasswordResetDoneView.as_view(
#             template_name='commons/password-reset/password_reset_done.html'
#         ),
#         name='password_reset_done'),
# path('password-reset-confirm/<uidb64>/<token>/',
#         auth_views.PasswordResetConfirmView.as_view(
#             template_name='commons/password-reset/password_reset_confirm.html'
#         ),
#         name='password_reset_confirm'),
# path('password-reset-complete/',
#         auth_views.PasswordResetCompleteView.as_view(
#             template_name='commons/password-reset/password_reset_complete.html'
#         ),
#         name='password_reset_complete'),


