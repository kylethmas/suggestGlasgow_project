from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# might come in useful later 
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default = 0)
    likes = models.IntegerField(default = 0)
    slug = models.SlugField(unique = True)
    
    def save( self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
        
        
class Place(models.Model):
    place_type = models.CharField(max_length = 128) # this could be helpful for later >>> ForeignKey(Category, on_delete=models.CASCADE)
    place_name = models.CharField(max_length=128)
    place_map = models.CharField(max_length = 128)
    url = models.URLField()
    likes = models.IntegerField(default = 0)
    dislikes = models.IntegerField(default = 0)
    #comments data structure goes here?
    
    class Meta:
        verbose_name_plural = 'places'

    def __str__(self):
        return self.place_name
        
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    #don't know if we want profile pictures?
    picture = models.ImageField(upload_to = 'profile_images', blank = True)
    
    def __str__(self):
        return self.user.username