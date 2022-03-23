from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

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
    PlaceID = models.BigAutoField(primary_key=True)
    place_type = models.CharField(max_length = 128, choices = (("Restaurant", "Restaurant"),("Cafe", "Cafe"),("Fast Food", "Fast Food"),("Nightlife", "Nightlife"))) # this could be helpful for later >>> ForeignKey(Category, on_delete=models.CASCADE)
    place_name = models.CharField(max_length=150)
    place_map = models.CharField(max_length = 128) #plus code or lat/long
    url = models.URLField()
    likes = models.IntegerField(User, default = 0)
    dislikes = models.IntegerField(User, default = 0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.place_name)
        super(Place, self).save(*args, **kwargs)

    #comments data structure goes here?
    #need place ID

    class Meta:
        verbose_name_plural = 'places'

    def __str__(self):
        return self.place_name

        
class Ratings(models.Model):
    PlaceID = models.ForeignKey(Place, on_delete=models.CASCADE, verbose_name="the related place",)
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="the user",)
    liked = models.BooleanField()
    disliked = models.BooleanField()
    saved = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'ratings'

    def __str__(self):
        return self.liked

class Comments(models.Model):
    CommentID = models.BigAutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="the user",)
    PlaceID = models.ForeignKey(Place, on_delete=models.CASCADE, verbose_name="the related place", )
    comment = models.CharField(max_length = 500)


    class Meta:
        verbose_name_plural = 'comments'

    def __str__(self):
        return self.comment

