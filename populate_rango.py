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
         'dislikes': 2,
         'slug': 'cafe_kyle'},
        {'place_type': 'Nightlife',
         'place_name': 'Bamboo',
         'place_map': 'G2 6RT',
         'url': 'http://www.bamboonightclub.co.uk/',
         'dislikes': 62,
         'slug': 'bamboo'},
        {'place_type': 'Restaurant',
         'place_name': 'Sugo',
         'place_map': 'G1 3LX',
         'url': 'https://www.sugopasta.co.uk/',
         'dislikes': 14,
         'slug': 'sugo'},
        {'place_type': 'Fast Food',
         'place_name': "McDonald's Finnieston",
         'place_map': 'G3 8JU',
         'url': 'https://www.just-eat.co.uk/restaurants-mcdonalds-finnieston-glasgow/menu',
         'dislikes': 27,
         'slug': 'mcdonalds_finnieston'}
    ]

    for p in places:
        add_place(p['place_type'],p['place_name'], p['url'],p['place_map'], p['dislikes'], p['slug'])



def add_place(place_type, place_name, url, location, dislikes = 0,slugName = '', comments = []):
    p = Place.objects.get_or_create(place_type=place_type, place_name=place_name)[0]
    p.url = url
    p.place_map = location
    p.dislikes = dislikes
    p.slug = slugName
    p.comments = comments
    p.save()
    return p


if __name__ == '__main__':
    print('Populating...')
    populate()