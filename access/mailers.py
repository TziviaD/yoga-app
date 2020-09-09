
from django.conf import settings 
from django.core.mail import send_mail 

from django.template.loader import render_to_string

from django.contrib.sites.shortcuts import get_current_site

from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def send_teacher_invite(request,teacher_profile):
    current_site = get_current_site(request)
    uid = urlsafe_base64_encode(force_bytes(teacher_profile.pk))
    string = reverse('teacher_signup',kwargs={'uidb64':uid})
    print(string)
    link = 'http://' + current_site.domain + string
    send_mail(
        'this is the subject line',
        f' hello this click here to sign up { link }',
        settings.DEFAULT_FROM_EMAIL, 
        [teacher_profile.email],
        html_message=render_to_string('access/signup_email.html', context={'url': link}),


    )




