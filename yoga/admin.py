from django.contrib import admin
from .models import Studio, Profile, Address, ClassInfo, Lesson

# Register your models here.

class StudioAdmin(admin.ModelAdmin):
    model = Studio
    list_display = ('name','headings','about')

admin.site.register(Studio, StudioAdmin)


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['is_teacher']
#     list_editable = list('is_teacher')
# doesnt work idk why error is list or a tuple both dont work


admin.site.register(Profile)

admin.site.register(Address)

class ClassInfoAdmin(admin.ModelAdmin):
    model = ClassInfo
    list_display = ('title','cost')

admin.site.register(ClassInfo, ClassInfoAdmin)

class LessonAdmin(admin.ModelAdmin):
    model = Lesson
    list_display = ['datetime','duration']

admin.site.register(Lesson, LessonAdmin)


