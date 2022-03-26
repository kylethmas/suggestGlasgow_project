from django.contrib import admin
from rango.models import Place, UserProfile


class PlaceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('place_name',)}


admin.site.register(Place,PlaceAdmin)
admin.site.register(UserProfile)