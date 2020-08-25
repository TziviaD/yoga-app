from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from access.forms import UserSignupForm

from yoga.models import Profile


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
            
          