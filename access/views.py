from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from access.forms import UserSignupForm

from .forms import OwnerInviteForm

from .tokens import SignupTokenGenerator

from yoga.models import Profile,Studio

from .mailers import send_teacher_invite


def signup(request): 
    if request.method == 'POST': 
        form = UserSignupForm(request.POST)
        print('line 13')   
        if form.is_valid():
            print('line 15')
            user = form.save()
            print('line 17')
            Profile.objects.create(user = user)
            print('line 19')
            login(request, user)
            print('line 21')
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
    studio_slug = Studio.objects.get(slug= studio_slug)
    profile = request.user.profile
    form = OwnerInviteForm(request.POST)
    if profile.owned_studios:
        if request.method == 'POST': 
            form = OwnerInviteForm(request.POST)
            if form.is_valid():
                profile = form.save()
                send_teacher_invite(request, profile.email)
                return render(request,'profile/profile_settings.html') 
    form = OwnerInviteForm()
    return render(request,'access/owner_invite.html',{'form':form})



    
    
    
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
