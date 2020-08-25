from django import forms
from .models import ClassInfo, Studio, Address,Lesson
from django.forms.widgets import DateTimeInput



class ClassInfoForm(forms.ModelForm): 
    class Meta():
        model = ClassInfo
        exclude = ['slug']
        # fields = '__all__'


class StudioForm(forms.ModelForm):
    class Meta:
        model = Studio
        exclude = ['address','slug']





class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'


class LessonForm(forms.ModelForm):
    datetime = forms.DateTimeField(input_formats=['%Y%m%d %H:%M'])
    class Meta:
        model = Lesson
        fields = '__all__'
        # date = forms.DateTimeField(
        #     input_formats=['%a/%d/%m/%Y %H:%M'],
        #     widget= forms.DateTimeInput(attrs={
        #         'class':'form-control datetimepicker-input',
        #         'data-target':'#datetimepicker1'
        #     })
        # )
        # date = forms.DateTimeField(input_formats=['%Y%m%d %H:%M'])
        help_texts = {'duration': 'Min'}
        widgets = { 
            # 'datetime': DateTimeInput(input_formats=['%Y%m%d %H:%M']),
            'duration': forms.NumberInput(attrs ={
                'placeholder': 'Minutes',
                })
        }
        labels = {
            'datetime': 'Time and date of Lesson'
        }


