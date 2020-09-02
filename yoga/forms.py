from django import forms
from django.contrib.auth.models import User
from .models import *
from django.forms.widgets import DateTimeInput
from django.forms.models import inlineformset_factory

class ProfileForm(forms.ModelForm):
    class Meta():
        model = Profile
        fields = '__all__'


class ClassInfoForm(forms.ModelForm):
    
    class Meta():
        model = ClassInfo
        exclude = ['slug']
        labels = {
            'title':'Class Name'
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Title of Class',
                'class':'form-control'
            }),
            'oneliner': forms.TextInput(attrs={
                'placeholder': 'Studio One Liner',
                'class':'form-control'
            }),
            'about': forms.Textarea(attrs={
                'placeholder': 'Tell us all about your studio',
                'class':'form-control'
            }),
            'cost': forms.TextInput(attrs={
                'placeholder': 'How much does this class cost?',
                'class':'form-control'
            }),
            'studio': forms.Select(attrs={
                'class':'form-control'
            }),
        }


class ClassInfoImageForm(forms.ModelForm):
    class Meta:
        model = ClassInfoImage
        fields = ['image']
    


class StudioForm(forms.ModelForm):
    class Meta:
        model = Studio
        exclude = ['address','slug', 'owner','invited_teachers' ]
        labels = {
            'name':'Studio Name',
            'headings':'Slogan'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Name of Studio',
                'class':'form-control'
            }),
            'headings': forms.TextInput(attrs={
                'placeholder': 'Studio One Liner',
                'class':'form-control'
            }),
            'about': forms.Textarea(attrs={
                'placeholder': 'About',
                'class':'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class':'form-control'
            }),

        }


class UpdateStudioForm(forms.ModelForm):
    class Meta:
        model = Studio
        exclude = ['address','slug', 'owner','invited_teachers' ]
        labels = {
            'name':'Studio Name',
            'headings':'Slogan'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Name of Studio',
                'class':'form-control'
            }),
            'headings': forms.TextInput(attrs={
                'placeholder': 'Studio One Liner',
                'class':'form-control'
            }),
            'about': forms.TextInput(attrs={
                'placeholder': 'About',
                'class':'form-control'
            }),
            'owner': forms.TextInput(attrs={
                'placeholder': 'owner of the studio',
                'class':'form-control'
            }),
            'invited_teachers': forms.TextInput(attrs={
                'placeholder': 'invited_teachers',
                'class':'form-control'
            }),
        }


class ImageStudioForm(forms.ModelForm):
    class Meta:
        model = StudioImage
        fields = ['image']


        


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['studio']
        widgets = {
            'address': forms.TextInput(attrs={
                'placeholder': '1234 Main St',
                'class':'form-control'
            }),
            'address2': forms.TextInput(attrs={
                'placeholder': 'Apartment, studio, or floor',
                'class': 'form-control'
            }),
            'city': forms.TextInput(attrs={
                'placeholder': 'City',
                'class': 'form-control'
            }),
        }

class LessonForm(forms.ModelForm):
    datetime = forms.DateTimeField(input_formats=['%Y%m%d %H:%M'])
    class Meta:
        model = Lesson
        exclude = ['teacher']
        # date = forms.DateTimeField(
        #     input_formats=['%a/%d/%m/%Y %H:%M'],
        #     widget= forms.DateTimeInput(attrs={
        #         'class':'form-control datetimepicker-input',
        #         'data-target':'#datetimepicker1'
        #     })
        # )
        # date = forms.DateTimeField(input_formats=['%Y%m%d %H:%M'])
        help_texts = {'duration': 'Min'}
        # range(start, stop[, step])
        # DURATION_CHOICES= [tuple([x,x,x]) for x in range(30,200,10)]
        widgets = { 
            # 'datetime': DateTimeInput(input_formats=['%Y%m%d %H:%M']),
# 
            'duration': forms.NumberInput(attrs ={
                'placeholder': 'Minutes',
                'class':'form-control'
                }),
            'classinfo':forms.Select(attrs={
                'placeholder':'What class does this belong to?',
                'class':'form-control'
            }),
            'studio':forms.TextInput(attrs={
                'placeholder':'Studio you are connected to, but should be automatic that it is connected with th user you are signed in as',
                'class':'form-control'
            })}
        labels = {
            'datetime': 'Time and date of Lesson'
        }
        #  dont delete for admin
        # def __init__(self, studio, *args, **kwargs):
        #     super(LessonForm, self).__init__(*args, **kwargs)
        #     self.fields['classinfo'].queryset = studio.classinfo_set.all()



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name',]


class EmailPassword(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','password',]




class ProfileUpdatedForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']