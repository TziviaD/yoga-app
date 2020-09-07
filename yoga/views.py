from django.conf import settings
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.html import strip_tags

from django.db import transaction

from .forms import *
from .models import Studio, ClassInfo, Lesson, Address, Profile

from .filters import  LessonFilter

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from django.db.models import Max

import random 



from PIL import Image #autosave for the class if you delete



from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:

						return HttpResponse('Invalid header found.')
						
					messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
					return redirect ("home")
			messages.error(request, 'An invalid email has been entered.')
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})


def home(request):
    klasses = []
    klasses = random.choices(ClassInfo.objects.all(), k=3)
    # for num in range(3): doent really make sence but works
    #     id = random.randint(1, ClassInfo.objects.last().id)
    #     klasses.append(ClassInfo.objects.get(id=id))
    return render(request, 'yoga/home.html',{'klasses':klasses})

# def home(request):
#     max_id=ClassInfo.objects.all().aggregate(max_id=Max('id'))['max_id']
#     while True:
#         pk = random.randint(1, max_id)
#         classinfo = ClassInfo.objects.filter(pk=pk).first()
#         if classinfo:
#             return render(request, 'yoga/home.html', {'classinfo':classinfo})
#     return render(request, 'yoga/home.html')




    
# class HomePage():
#     def random_classes(self, request):
#         classinfos = ClassInfo.objects.filter(name =name) 
#         srandom_classes = random.randrange(classinfos)
#         return render(request,'home',random_classes)

@login_required(login_url='login') 

# s1 = Studio.objects.get(id=1)
# studioimages = s1.studioimage_set.all()
# for studioimage in studioimages:
# 	studioimage.image
def create_studio(request):
    print('line 15')
    if request.method == 'POST':
        print('method get')
        form = StudioForm(request.POST, request.FILES)
        addressform = AddressForm(request.POST)
        if form.is_valid() and addressform.is_valid():
            studio = form.save(commit=False) #save as python object not db cause we didnt add all requreid info
            studio.owner = request.user.profile
            studio.save()
            s1 = Studio.objects.get(id=1)
            studioimages = s1.studioimage_set.all()
            studio.images.save()
            address= addressform.save(commit=False)
            address.studio = studio
            address.save() #address not saving needs self? huh
            profile = request.user.profile
            profile.is_teacher = True
            profile.save()
                    
            # return HttpResponse("STUDIO SAVED")
            # return render(request, 'yoga/home.html') #redirect not working need to figure it out
            # is_teacher == True
            return redirect('single_studio', studio.slug ) #this view and variable
        else:
            print('errors')
            for error, message in addressform.errors.items():
                print(error, message)
    return render(request, 'studio/create_studio.html',context={'forms' : [StudioForm(),AddressForm()]})
    
    


@login_required(login_url='login') 
def create_class(request):
    form = ClassInfoForm(request.POST)
    # if request.user.profile.owned_studios or request.user.profile.studio_invites:
    #     studioname = form.studio.name 
    if request.method == 'POST':
        form = ClassInfoForm(request.POST, request.FILES)
        if form.is_valid():
            # studioname.save()
            classinfo = form.save(commit=False) 
            classinfo.slug =slugify(classinfo.title)
            classinfo.save()
            return redirect('single_studio',classinfo.studio.slug)
        else:
            print('errors')
            for error, message in form.errors.items():
                print(error, message)
            # return redirect('single_studio', classinfo.slug.name)
            # return render(request, 'yoga/single_studio.html', {'single_studio':single_studio})
            # return redirect('single_studio', single_studio ) #this view and variable
    else: #why dosent it come down to here?
        return render(request, 'studio/create_class.html',context={'form' : ClassInfoForm()})



# @login_required(login_url='login') 
# def create_class(request):
#     if request.method == 'POST':
#         form = ClassInfoForm(request.POST)
#         if form.is_valid():
#             classinfo = form.save()
#             single_studio =slugify(classinfo.studio.name)
#             return render(request, 'yoga/single_studio.html', {'single_studio':single_studio})
#             # return redirect('single_studio', single_studio ) #this view and variable
#     else:
#         return render(request, 'studio/create_class.html',context={'classinfoform' : ClassInfoForm()})


def figure_out_what_studio(request):
    owned_studios = request.user.profile.owned_studios.all()
    invited_studios = request.user.profile.studio_invites.all()
    if owned_studios.count() >0 and invited_studios.count() > 0:
        return render(request, 'yoga/select_studio.html')
    elif invited_studios.count() == 1:
        return redirect('create_lesson', request.user.profile.studio_invites.first().id)
    elif owned_studios.count() == 1:
        return redirect('create_lesson', request.user.profile.owned_studios.first().id)

    else:
        return render(request, 'yoga/select_studio.html')



@login_required(login_url='login')
def create_lesson(request, studio_id):
    from datetime import datetime
    studio = Studio.objects.get(id=studio_id)
    if request.method == 'POST':
        # request.POST['datetime'] = datetime.strptime(request.POST.get('datetime'), '%Y/%m/%d %H:%M')
        data ={
            'datetime':datetime.strptime(request.POST.get('datetime'), '%Y/%m/%d %H:%M'),
            'duration':request.POST.get('duration'),
            'classinfo':request.POST.get('classinfo')
        }
        form = LessonForm(data)
        if form.errors:
            for value in form.errors.values():
                print(value)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.teacher =  request.user.profile
            lesson.save()
            return redirect('display_class', lesson.classinfo.slug)
            # return redirect('single_studio,') i want it to redirect to single studio of the studio connected to
    lessonform = LessonForm()
    lessonform.fields['classinfo'].queryset = studio.classinfo_set.all()
    return render(request, 'studio/create_lesson.html', {'lessonform': lessonform})


@login_required(login_url='login')   
def update_lesson(request,lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    if request.method == "POST":
        lesson_form = UpdateLesson(request.POST, instance=lesson)
        if lesson_form.is_valid():
            lesson = lesson_form.save()
            return redirect('display_class', lesson.classinfo.slug)
    lesson_form = LessonForm(instance=lesson)
    return render (request, 'studio/edit_lesson.html', {'lesson_form': lesson_form})
   




# @login_required(login_url='login')
# def profile_settings(request):
#     return render(request,'profile/profile_settings.html')

# @login_required(login_url='login')
# def update_basic_profile(request):
#     profile = request.user.profile
#     form = ProfileUpdatedForm(instance=profile)
#     if request.method == 'POST':
#         form = ProfileUpdatedForm(request.POST,request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#     context={'form':form}
#     return render(request,'profile/profile_settings.html', context)
       

# @login_required(login_url='login')
# def update_basic_profile(request):
#     profile = request.user.profile
#     context = {}
#     if request.method == 'POST':
#         profile_form = ProfileForm(request.Post, instance=profile)
#         user_form = UserForm(request.POST, instance=profile.user)
#         uploaded_image = request.FILES['profileimage']
#         fs = FileSystemStorage()
#         name = fs.save(uploaded_image.name,uploaded_image)
        
#         context['url'] = fs.url(name)
#         if user_form.is_valid:
#             user=user_form.save()
#             return redirect('profile_settings')
#     user_form = UserForm(instance=User)
#     profile_form = ProfileForm(instance=Profile)
#     return render(request,'profile/profile_settings.html', {'profile_form':profile_form,'user_form': user_form} )


@login_required(login_url='login')
def update_basic_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        profile_form = ProfileUpdatedForm(request.POST, request.FILES, instance=profile)
        user_form = UserForm(request.POST, instance=profile.user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('update_basic_profile')
        else:
            print(profile_form.errors)
            print(user_form.errors)
    user_form = UserForm(instance=request.user)
    profile_form = ProfileUpdatedForm(instance=profile)
    return render(request,'profile/profile_settings.html', {'profile_form':profile_form,'user_form': user_form} )




# def account_settings(request):
#     profile = request.user.profile
#     if request.method == "POST":
#         emailpassword = EmailPassword(request.POST, instance=profile.user)
#         if emailpassword.is_valid():
#             emailpassword.save()
#             return redirect('profile_settings')
#     emailpassword= EmailPassword(instance=profile)
#     return render(request, 'profile/account_settings.html', {'form':emailpassword})





def account_settings(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = PasswordChangeForm(request.user.profile, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile/account_settings.html')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profile/account_settings.html', {
        'form': form
    })




# def account_settings(request):
#     profile = request.user.profile
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user.profile, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important!
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('profile/account_settings.html')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'profile/account_settings.html', {
#         'form': form
#     })





# @login_required() 
# def email_change(request):
#     form = EmailChangeForm()
#     if request.method=='POST':
#         form = EmailChangeForm(user, request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect("/accounts/profile/")
#     else:
#         return render_to_response("email_change.html", {'form':form},
#                                   context_instance=RequestContext(request))


# def profile(request):
#     user_form = UserUpdatedForm()
#     profile_form =ProfileUpdatedForm()

#     context ={
#         'user_form':user_form,
#         'profile_form':profile_form
#     }
#     return render(request,'profile/profile_settings.html', context)






def display_lessons(request): #all classes happening in the week #display class
    classinfos = ClassInfo.objects.all()
    lesson_filter = LessonFilter(request.GET, queryset = Lesson.objects.all())         
    datetime = Lesson.objects.order_by('-datetime')
    return render(request,'yoga/display_lessons.html', {'classinfos': classinfos,'lesson_filter':lesson_filter, 'datetime':datetime})


def display_class(request, name):
    single_class = ClassInfo.objects.get(slug =name)
    return render(request, 'yoga/display_class.html', {'single_class': single_class})

@login_required(login_url='login')   
def update_class(request,slug):
    classinfo = ClassInfo.objects.get(slug = slug)
    if request.method == "POST":
        classinfo_form = ClassInfoForm(request.POST,instance=classinfo)
        image_form = ClassInfoImageForm(request.POST,request.FILES)
        if classinfo_form.is_valid() and image_form.is_valid():
            classinfo = classinfo_form.save()
            image = image_form.save(commit=False)
            image.classinfo = classinfo
            image.save()
            return redirect('display_class', classinfo.slug)
    classinfo_form = ClassInfoForm(instance=classinfo)
    image_form = ClassInfoImageForm()
    return render (request, 'studio/edit_class.html', {'classinfo_form': classinfo_form,'image_form':image_form})
   

def delete_classinfo_image(request, classinfo_id):
    classinfo_image = ClassInfoImage.objects.get(id=classinfo_id)
    classinfo_slug = classinfo_image.classinfo.slug
    if classinfo_image.classinfo.studio.owner == request.user.profile:
        classinfo_image.delete()
    return redirect('display_class', classinfo_slug)


# class UpdateClassView(UpdateView):
#     model = ClassInfo
#     form = ClassInfoForm
#     fields = ['title','oneliner','about','teacher','cost','studio']
#     template_name = 'studio/edit_class.html'
#     slug_field = 'slug'

def studios(request): # all studios with clickable to go into specfic one
    studios = Studio.objects.all()
    return render(request, 'yoga/studios.html', {'studios':studios})
    
# def delete_head_studio_image(request,studio_id):
#     studio_id = Studio.objects.get(id=studio_id)
#     head_studio_image = studio_id.image
#     if studio.id.owner == request.user.profile:
#         head_studio_image.delete()
        
#     return redirect('studios')



@login_required(login_url='login')
def single_studio(request, name): #a specfic studio
    single_studio = Studio.objects.get(slug = name) 
    # studio_classes = ClassInfo.objects.filter(studio=single_studio) #get only classes that are in the studio
    # # studio_classes = single_studio.classinfo_set.all()
    return render(request, 'yoga/single_studio.html', {'single_studio':single_studio} ) #how do pick a specfic one

def delete_studio_image(request, studio_image_id):
    studio_image = StudioImage.objects.get(id=studio_image_id)
    studio_slug = studio_image.studio.slug
    if studio_image.studio.owner == request.user.profile:
        studio_image.delete()
        if studio_image.id == 0:
            studio_image = Image.open(default='studio_default.jpg')
            studio.show()
    return redirect('single_studio', studio_slug)


@login_required(login_url='login')
def update_studio(request,slug):
    studio = Studio.objects.get(slug = slug)
    if request.method == 'POST':
        studio_form = StudioForm(request.POST, request.FILES, instance=studio)
        address_form = AddressForm(request.POST, instance=studio.address_set.first())
        image_form = ImageStudioForm(request.POST, request.FILES)
        if studio_form.is_valid() and address_form.is_valid() and image_form.is_valid():
            studio = studio_form.save()
            address = address_form.save()
            image = image_form.save(commit=False)
            image.studio = studio
            image.save()  
            return redirect('single_studio', studio.slug)
        else:
            print(studio_form.errors)
            print(address_form.errors)
    studio_form = StudioForm(instance=studio)
    address_form = AddressForm(instance=studio.address_set.first())
    image_form = ImageStudioForm()
    return render(request, 'studio/edit_single_studio.html', {'studio_form':studio_form, 'image_form':image_form, 'address_form':address_form,'studio':studio})






# @login_required
# def post(request):
#     studio = Studio.objects.get(slug = slug)
#     ImageFormSet = modelformset_factory(Images,
#                                         form=ImageForm, extra=3)

#     if request.method == 'POST':
#         studio_form = StudioForm(request.POST, instance=studio)
#         address_form = AddressForm(request.POST, instance=studio.address_set.first())
#         formset = ImageFormSet(request.POST, request.FILES,
#                                queryset=Images.objects.none())


#         if postForm.is_valid() and formset.is_valid():
#             post_form = postForm.save(commit=False)
#             post_form.user = request.user
#             post_form.save()

#             for form in formset.cleaned_data:
#                 image = form['image']
#                 photo = Images(post=post_form, image=image)
#                 photo.save()
#             messages.success(request,
#                              "Posted!")
#             return HttpResponseRedirect("/")
#         else:
#             print postForm.errors, formset.errors
#     else:
#         postForm = PostForm()
#         formset = ImageFormSet(queryset=Images.objects.none())
#     return render(request, 'index.html',
#                   {'postForm': postForm, 'formset': formset},
#                   context_instance=RequestContext(request))




            
#    check slug
# teacher and studio

# def profile(request):
#     user_form = UserUpdatedForm()
#     profile_form =ProfileUpdatedForm()

#     context ={
#         'user_form':user_form,
#         'profile_form':profile_form
#     }
#     return render(request,'')






def testing(request):
    return render(request, 'yoga/testing.html', )
