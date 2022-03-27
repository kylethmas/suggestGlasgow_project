from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


# model for each place uses likes and dislikes as many to many
class Place(models.Model):
    PlaceID = models.BigAutoField(primary_key=True)
    place_type = models.CharField(max_length=128, choices=(
        ("Restaurant", "Restaurant"),
        ("Cafe", "Cafe"),
        ("Fast Food", "Fast Food"),
        ("Nightlife", "Nightlife")))
    place_name = models.CharField(max_length=150)
    place_image = models.ImageField(upload_to='place_images', default="/place_images/Default.jpg", blank=True)
    latitude = models.CharField(u'latitude', max_length=25, blank=True, default=0)
    longitude = models.CharField(u'longitude', max_length=25, blank=True, default=0)
    url = models.CharField(max_length=200)
    likes = models.ManyToManyField(User, related_name='place_like')
    dislikes = models.ManyToManyField(User, related_name='place_dislike')
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.place_name)
        super(Place, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'places'

    def __str__(self):
        return self.place_name

    def number_of_likes(self):
        return self.likes.count()

    def number_of_dislikes(self):
        return self.dislikes.count()


# comments model with username and placeID foreign keys
class Comments(models.Model):
    CommentID = models.BigAutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="the user", )
    PlaceID = models.ForeignKey(Place, on_delete=models.CASCADE, verbose_name="the related place", )
    comment = models.CharField(max_length=500)
    date = models.CharField(max_length=10)
    title = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = 'comments'

    def __str__(self):
        return self.comment


# links with the user model but allows us to add saves
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saves = models.ManyToManyField(Place, related_name='place_save')

    def __str__(self):
        return self.user.username

    def number_of_saves(self):
        return self.saves.count()

