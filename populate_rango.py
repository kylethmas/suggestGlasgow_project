import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'suggestGlasgow_project.settings')

import django
django.setup()
from rango.models import Category, Place, User


def populate():

    places = [
        {'place_type': 'Cafe',
         'place_name': 'Cafe Kyle',
         'place_map': 'ADD MAP THINGY HERE G3 6RF',
         'url':'https://kylescatering.ie/delivery/kyles-cafe/',
         'slug': 'cafe_kyle'},
        {'place_type': 'Nightlife',
         'place_name': 'Bamboo',
         'place_map': 'G2 6RT',
         'url': 'http://www.bamboonightclub.co.uk/',
         'slug': 'bamboo'},
        {'place_type': 'Restaurant',
         'place_name': 'Sugo',
         'place_map': 'G1 3LX',
         'url': 'https://www.sugopasta.co.uk/',
         'slug': 'sugo'},
        {'place_type': 'Fast Food',
         'place_name': "McDonald's Finnieston",
         'place_map': 'G3 8JU',
         'url': 'https://www.just-eat.co.uk/restaurants-mcdonalds-finnieston-glasgow/menu',
         'slug': 'mcdonalds_finnieston'}
    ]

    for p in places:
        add_place(p['place_type'],p['place_name'], p['url'],p['place_map'], p['slug'])

    users = [
        {'username':'john101',
         'email':'lennon@thebeatles.com',
         'password':'johnpassword'},
        {'username': 'ali',
         'email': 'ali@gmail.com',
         'password': 'ali987654'},
        {'username': 'kyle',
         'email': 'decbihlcdihblcdihl@gmail.com',
         'password': 'kylethomas'},
        {'username': 'niamh',
         'email': 'niamh1010@gmail.com',
         'password': 'ilovepuppies'},
        {'username': 'jack',
         'email': 'jack@gmail.com',
         'password': 'armingdale'},
        {'username': 'peterpiper23',
         'email': 'peterpiper23',
         'password': 'nurseryRhymes'},
        {'username': 'scowell',
         'email': 'simon@xfactor.com',
         'password': 'ihatethevoice'},
        {'username': 'jackwhitehall',
         'email': 'jack@netflix.com',
         'password': 'solotravel'},
        {'username': 'dbecks',
         'email': 'david.beckham@me.com',
         'password': 'hasBeen'},
        {'username': 'ronron',
         'email': 'ron@hp.com',
         'password': 'abracadabra'}
    ]

    for u in users:
        add_user(u['username'],u['email'], u['password'])


def add_place(place_type, place_name, url, location,slugName = '', comments = []):
    p = Place.objects.get_or_create(place_type=place_type, place_name=place_name)[0]
    p.url = url
    p.place_map = location
    p.slug = slugName
    p.comments = comments
    p.save()
    return p


def add_user(name,email,password):
    users = User.objects
    if users.filter(username=name).exists():
        user = User.objects.get(username=name)
    else:
        user = User.objects.create_user(username,email,password)
    return user


if __name__ == '__main__':
    print('Populating...')
    populate()