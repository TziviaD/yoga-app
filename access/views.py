from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from access.forms import UserSignupForm

from .forms import OwnerInviteForm, TeacherSignupForm

from .tokens import SignupTokenGenerator

from yoga.models import Profile,Studio

from .mailers import send_teacher_invite

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text


def signup(request): 
    if request.method == 'POST': 
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user = user)
            login(request, user)
            return redirect('home') #shouldnt it be render? cause we want them to go to a new page its not redirecting?...
    #  return render(request, 'yoga/home.html', context={'studio':Studio()})
    form = UserSignupForm()
    return render(request, 'access/signup.html', {'form': form}) 


# if request.method == 'POST': 
#         if form.is_valid():
#             user = form.save()
#             submit = request.POST.get 
#             if submit = 'Student':
#                 return redirect('create_studio') 
#             if submit = 'Teacher':
#                 return redirect('create_studio')
#             if submit = 'Creating a Studio':
#                 return redirect('create_studio')
            



    
def owner_invite(request,studio_slug): # i only want the name of studio is cause i want it redirected to their studio page
    studio = Studio.objects.get(slug= studio_slug)
    profile = request.user.profile
    form = OwnerInviteForm(request.POST)
    if studio in profile.owned_studios.all():
        if request.method == 'POST': 
            form = OwnerInviteForm(request.POST)
            if form.is_valid():
                profile = form.save()
                send_teacher_invite(request, profile)
                return render(request,'profile/profile_settings.html') 
    form = OwnerInviteForm()
    return render(request,'access/owner_invite.html',{'form':form})


def teacher_signup(request,uidb64):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        profile = Profile.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Profile.DoesNotExist):
        profile = None    
    if request.method == 'POST': 
        form = TeacherSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile.user = user
            profile.is_teacher = True
            profile.save()
            login(request, user)
            return redirect('home')
    #  return render(request, 'yoga/home.html', context={'studio':Studio()})
    form = TeacherSignupForm()
    return render(request, 'access/signup.html', {'form': form}) 

    
    
    
# def owner_invite(request,studio_slug): # i only want the name of studio is cause i want it redirected to their studio page
#     studio_slug = Studio.objects.get(slug= studio_slug)
#     profile = request.user.profile
#     form = OwnerInviteForm(request.POST)
#     if profile.owned_studios:
#         if request.method == 'POST': 
#             form = OwnerInviteForm(request.POST)
#             profile, created = Profile.objects.get_or_create(email=email)
#             if created:

# 			generate token and uuid for profile 
# 			send email with singup link using uuid, token
# 		studio.invited_teachers.add(profile) 
# 		profile.is_teacher = True
#             if form.is_valid():
#                 form.save()
#                 return render(request,'profile/profile_settings.html') 
#     form = OwnerInviteForm()
#     return render(request,'access/owner_invite.html',{'form':form})
