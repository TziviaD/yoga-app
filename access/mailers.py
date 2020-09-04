
from django.conf import settings 
from django.core.mail import send_mail 

from django.template.loader import render_to_string

from django.contrib.sites.shortcuts import get_current_site

def send_teacher_invite(request,teacher_email):
    current_site = get_current_site(request)
    subject = 'welcome to GFG world'
    message = render_to_string('access/signup_email.html', {
            'domain': current_site.domain})

    email_from = settings.EMAIL_HOST_USER 
    recipient_list = [teacher_email] 
    send_mail( subject, message, email_from, recipient_list ) 



