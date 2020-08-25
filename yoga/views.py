from django.conf import settings
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.core.files.storage import FileSystemStorage

from django.utils.text import slugify
from django.utils.html import strip_tags

from .forms import ClassInfoForm, StudioForm, AddressForm, LessonForm
from .models import Studio, ClassInfo, Lesson, Address


from .filters import StudioFilter, ClassInfoFilter, LessonFilter






# Create your views here.

@login_required(login_url='login') 
def home(request):
    return render(request, 'yoga/home.html')

@login_required(login_url='login') 
def create_studio(request):
    print('line 15')
    if request.method == 'POST':
        print('method get')
        form = StudioForm(request.POST)
        addressform = AddressForm(request.POST)
        if form.is_valid() and addressform.is_valid():
            studio = form.save(commit=False) #save as python object not db cause we didnt add all requreid info
            address, created = Address.objects.get_or_create(**form.cleaned_data)
            studio.address = address
            studio.slug = slugify(studio.name)
            
            studio.save()
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
    else:
        return render(request, 'studio/create_studio.html',context={'studioform' : StudioForm()})
    return render(request, 'studio/create_studio.html')
    


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'studio/create_studio.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'studio/create_studio.html')

    



@login_required(login_url='login') 
def create_class(request):
    form = ClassInfoForm(request.POST)
    if request.method == 'POST':
        form = ClassInfoForm(request.POST)
        if form.is_valid():
            classinfo = form.save(commit=False) 
            classinfo.slug =slugify(classinfo.title)
            classinfo.save()
            return redirect('single_studio',classinfo.studio.slug)
            # return redirect('single_studio', classinfo.slug.name)
            # return render(request, 'yoga/single_studio.html', {'single_studio':single_studio})
            # return redirect('single_studio', single_studio ) #this view and variable
    else: #why dosent it come down to here?
        return render(request, 'studio/create_class.html',context={'classinfoform' : ClassInfoForm()})



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




@login_required(login_url='login')
def create_lesson(request):
    from datetime import datetime
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
            lesson = form.save() 
            return redirect('display_class', lesson.classinfo.slug)
            # return redirect('single_studio,') i want it to redirect to single studio of the studio connected to
    return render(request, 'studio/create_lesson.html', {'lessonform': LessonForm()})


# class display_all_lessons():
#     def studio(self):
#         studio = Studio.objects.get(slug=name)
#         abc_order = studio.sort()
#         return abc_order

#     def cost(self):
#         cost = ClassInfo.objects.get(cost = cost)
#         cost_smallest_to_greatest = sorted(cost)
#         cost_greatest_to_smallest = cost.sort(reverse = True)

#     def cost(self,starting_price=0,ending_price=10):
#         range_of_cost = range(starting_price,ending_price)
#         cost = ClassInfo.objects.filter(cost = range_of_cost)
#         return cost

      



# Studio
# Location - 
# Cost
# Time
# Date

@login_required(login_url='login')
def profile_settings(request):
    return render(request,'profile/profile_settings.html')

def display_lessons(request): #all classes happening in the week #display class
    classinfos = ClassInfo.objects.all()
    lesson_filter = LessonFilter(request.GET, queryset = Lesson.objects.all())         
    datetime = Lesson.objects.order_by('-datetime')
    return render(request,'yoga/display_lessons.html', {'classinfos': classinfos,'lesson_filter':lesson_filter, 'datetime':datetime})


def display_class(request, name):
    # klassinfo = ClassInfo.objects.all()
    single_class = ClassInfo.objects.get(slug =name)
    return render(request, 'yoga/display_class.html', {'single_class': single_class})


def studios(request): # all studios with clickable to go into specfic one
    studios = Studio.objects.all()
    return render(request, 'yoga/studios.html', {'studios':studios})
    

@login_required(login_url='login')
def single_studio(request, name): #a specfic studio
    single_studio = Studio.objects.get(slug = name) 
    # studio_classes = ClassInfo.objects.filter(studio=single_studio) #get only classes that are in the studio
    # # studio_classes = single_studio.classinfo_set.all()
    return render(request, 'yoga/single_studio.html', {'single_studio':single_studio} ) #how do pick a specfic one


class UpdateSingleStudioView(UpdateView):
    model = Studio
    form = StudioForm()
    fields = ['name','headings','about','address']
    template_name = 'studio/edit_single_studio.html'
    slug_field = 'slug'



class UpdateClassView(UpdateView):
    model = ClassInfo
    form = ClassInfoForm
    exclude = ['slug']
    template_name = 'edit_class.html'
   





def testing(request):
    return render(request, 'yoga/testing.html', )
