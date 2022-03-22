import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'suggestGlasgow_project.settings')

import django
django.setup()
from rango.models import Category, Place


def populate():

    places = [
        {'place_type': 'Cafe',
         'place_name': 'Cafe Kyle',
         'place_map': 'ADD MAP THINGY HERE G3 6RF',
         'url':'https://kylescatering.ie/delivery/kyles-cafe/',
         'likes': 54,
         'dislikes': 2},
        {'place_type': 'Nightlife',
         'place_name': 'Bamboo',
         'place_map': 'G2 6RT',
         'url': 'http://www.bamboonightclub.co.uk/',
         'likes': 97,
         'dislikes': 62},
        {'place_type': 'Restaurant',
         'place_name': 'Sugo',
         'place_map': 'G1 3LX',
         'url': 'https://www.sugopasta.co.uk/',
         'likes': 23,
         'dislikes': 14},
        {'place_type': 'Fastfood',
         'place_name': "McDonald's Finnieston",
         'place_map': 'G3 8JU',
         'url': 'https://www.just-eat.co.uk/restaurants-mcdonalds-finnieston-glasgow/menu',
         'likes': 12,
         'dislikes': 27}
    ]

    for p in places:
        add_place(p['place_type'],p['place_name'], p['url'],p['place_map'],p['likes'], p['dislikes'])

    cafe_places = [] #cafe starting data goes here
    
    restaraunt_places = [] #restaurant starting data goes here
    
    nightlife_places = [] #nightlife starting data goes here
         
    fastfood_places = [] #fastfood starting data goes here


def add_place(place_type, place_name, url, location, likes = 0, dislikes = 0, comments = []):
    p = Place.objects.get_or_create(place_type=place_type, place_name=place_name)[0]
    p.url = url
    p.place_map = location
    p.likes = likes
    p.dislikes = dislikes
    p.comments = comments
    p.save()
    return p


if __name__ == '__main__':
    print('Populating...')
    populate()