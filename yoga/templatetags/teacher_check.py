from django import template
from yoga.models import Studio, ClassInfo

register = template.Library()



@register.filter(name="teacher_in_studio")
def teacher_in_studio(profile, studio_id):
    studio = Studio.objects.get(id=studio_id)
    classes = studio.classinfo_set.filter(teacher=profile)
    if classes:
        return True
    return False

@register.filter(name="teacher_in_class")
def teacher_in_class(profile, classinfo_id):
    classes = ClassInfo.objects.filter(id= classinfo_id, teacher=profile)
    if classes:
        return True
    return False



