from django.contrib import admin
from rango.models import UserProfile, Place


class PlaceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('place_name',)}


admin.site.register(UserProfile)
admin.site.register(Place,PlaceAdmin)
