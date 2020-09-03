from django.db import models
from django.db import models

from django.utils import timezone
from django.utils.text import slugify

from django.contrib.auth.models import User 





class Profile(models.Model): #techinacally move this to the access app makes more sence
    GENDER = (
        ('Female','Female'),
        ('Male', 'Male')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    gender = models.CharField(max_length=100, null=True, choices=GENDER)
    is_teacher = models.BooleanField(default=False)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics') #profile_pics just the directory the images get upluad to
    email = models.EmailField(unique=True)
    def __str__(self):
        return f"Profile {self.user.username}  {self.is_teacher}"
    

class ClassInfo(models.Model):
    title = models.CharField(max_length=100)
    oneliner = models.CharField(max_length=300)
    about = models.TextField()
    cost = models.SmallIntegerField()
    studio = models.ForeignKey('Studio', on_delete=models.CASCADE) # can havae many classes
    slug = models.SlugField(unique=True) # first make defalt make migrations and migrate then go into shell
    # add the connection then go back and delete default anf make migrations
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title + self.studio.name)
        super().save(*args, **kwargs)   

class ClassInfoImage(models.Model):
	classinfo = models.ForeignKey(ClassInfo, on_delete=models.CASCADE)
	image = models.ImageField(default='class_default.jpg', upload_to='class_pics')
    
# s1 = Studio.objects.get(id=1)
# studioimages = s1.studioimage_set.all()
# for studioimage in studioimages:
# 	studioimage.image

    


    # def get_absolute_url(self): i dont think it does anything
    #     return reverse('display_class', kwargs={'slug': self.slug})


class Lesson(models.Model):
    datetime = models.DateTimeField()
    duration = models.SmallIntegerField()
    classinfo =models.ForeignKey(ClassInfo, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True,
    limit_choices_to={'is_teacher':True}) #if teacher gets deleted class still stays
     #a lesson has one 'program' its apart of and can have many lessons 
    # developers is like a studio and python course like the classinfo and the each days is the lessons 

    # def __str__(self): how does this work?
    #     return self.lesson.classinfo.title
    def __str__(self):
        return self.datetime





class Address(models.Model):
    address = models.CharField(max_length=300, null=True)
    address2 = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=300, null=True)
    studio = models.ForeignKey('Studio', on_delete=models.PROTECT)
    def __str__(self):
        return self.address

class Studio(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True) #take ouut null true so it cant be blank
     #have many teachers for one studio
    headings = models.CharField(max_length=300)  #blank = true add this in
    about = models.TextField()
    cover_image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owned_studios')
    invited_teachers = models.ManyToManyField(Profile, related_name='studio_invites')

    
    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reversed('update_single_studio', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)   



class StudioImage(models.Model):
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)
    image = models.ImageField(default='studio_default.jpg', upload_to='studio_pics')

    def __str__(self):
        return self.studio.name


# class Image(models.Model):
#     title = models.CharField(max_length=200)
#     image = models.ImageField(upload_to='images')

#     def __str__(self):
#         return self.title

# teachers have access to sign up