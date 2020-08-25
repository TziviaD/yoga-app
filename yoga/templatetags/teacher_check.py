from django import template
from yoga.models import Studio

register = template.Library()


@register.filter(name="teacher_in_studio")
def teacher_in_studio(profile, studio_id):
    studio = Studio.objects.get(id=studio_id)
    classes = studio.classinfo_set.filter(teacher=profile)
    if classes:
        return True
    return False



