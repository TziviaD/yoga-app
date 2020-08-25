from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
path('login/', LoginView.as_view(template_name='access/login.html'), name='login'),
path('signup/', views.signup, name='signup'),
path('logout/', LogoutView.as_view(), name='logout'), #we dont have a template name cause we are redirecting it to a page
]
