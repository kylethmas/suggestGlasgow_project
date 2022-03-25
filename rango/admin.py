from django.contrib import admin
from rango.models import Ratings, Place, UserProfile


class PlaceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('place_name',)}


admin.site.register(Ratings)
admin.site.register(Place,PlaceAdmin)
admin.site.register(UserProfile)