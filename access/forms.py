from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from yoga.models import Studio, Profile


class UserSignupForm(UserCreationForm):
    class Meta:
        model =User
        fields = ['first_name', 'last_name','email','username'] #all everything that will show up on the form
        # fields = ['username'] #all everything that will show up on the form


class StudioSignupForm(forms.ModelForm):

    class Meta:
        model =Studio
        fields = '__all__'



class ProfileSignupForm(forms.ModelForm):

    class Meta:
        model =Profile
        fields = '__all__'