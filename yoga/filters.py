
import django_filters
from .models import Studio, ClassInfo, Lesson

class StudioFilter(django_filters.FilterSet):
    class Meta:
       model = Studio
       fields = ('name','address')

    

class ClassInfoFilter(django_filters.FilterSet):
    class Meta:
        model = ClassInfo
        fields = ('cost','teacher')

class LessonFilter(django_filters.FilterSet):
    classinfo__studio__name = django_filters.CharFilter(field_name='classinfo__studio__name', lookup_expr='icontains')
    classinfo__studio__address__city = django_filters.CharFilter(field_name = 'classinfo__studio__address__city', lookup_expr='icontains')
    
    classinfo__title = django_filters.CharFilter(field_name='classinfo__title', lookup_expr='icontains')



    duration__gt = django_filters.NumberFilter(field_name='duration', lookup_expr='gte')
    duration__lt = django_filters.NumberFilter(field_name='duration', lookup_expr='lt')

    classinfo__cost__gt = django_filters.NumberFilter(field_name= 'classinfo__cost', lookup_expr='gt')
    classinfo__cost__lt = django_filters.NumberFilter(field_name= 'classinfo__cost', lookup_expr='lt')
    
    class Meta:
        model = Lesson
        fields = ('duration',)