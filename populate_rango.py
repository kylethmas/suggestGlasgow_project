import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'suggestGlasgow_project.settings')

import django
django.setup()
from rango.models import Category, Place


def populate():
    cafe_places = [] #cafe starting data goes here
    
    restaraunt_places = [] #restaurant starting data goes here
    
    nightlife_places = [] #nightlife starting data goes here
         
    fastfood_places = [] #fastfood starting data goes here


def add_page(categort, place_name, url, location = "what goes here", likes = 0, dislikes = 0, comments = []):
    page = Page.objects.get_or_create(category=cat, title=title)[0]
    page.url = url
    page.location = location
    page.likes = likes
    page.dislikes = dislikes
    page.comments = comments
    page.save()
    return page


if __name__ == '__main__':
    print('Populating...')
    populate()