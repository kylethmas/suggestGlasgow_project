import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'suggestGlasgow_project.settings')

import django
django.setup()
from rango.models import Category, Place, User, UserProfile, Comments
from PIL import Image
from django.core.files import File as DjangoFile

def populate():

    places = [
        {'place_type': 'Cafe',
         'place_name': 'Cafe Kyle',
         'latitude': '55.87226',
         'longitude': '-4.27247',
         'url':'https://kylescatering.ie/delivery/kyles-cafe/',
         'slug': 'cafe_kyle',
         'image':'static/images/cafekyle.jpg'},
        {'place_type': 'Nightlife',
         'place_name': 'Bamboo',
         'latitude': '55.87226',
         'longitude': '-4.27247',
         'url': 'http://www.bamboonightclub.co.uk/',
         'slug': 'bamboo',
         'image':'static/images/bamboo.jpg'},
        {'place_type': 'Restaurant',
         'place_name': 'Sugo',
         'latitude': '55.87226',
         'longitude': '-4.27247',
         'url': 'https://www.sugopasta.co.uk/',
         'slug': 'sugo',
         'image':'static/images/sugo.jpg'},
        {'place_type': 'Restaurant',
         'place_name': 'MacTassos',
         'latitude': '55.867546761164064',
         'longitude': '-4.2882667016457905',
         'url': 'https://www.tripadvisor.co.uk/Restaurant_Review-g186534-d12580740-Reviews-MacTassos-Glasgow_Scotland.html',
         'slug': 'mactassos',
         'image':'static/images/mactassos.jpg'},
        {'place_type': 'Fast Food',
         'place_name': "McDonald's Finnieston",
         'latitude': '55.87226',
         'longitude': '-4.27247',
         'url': 'https://www.just-eat.co.uk/restaurants-mcdonalds-finnieston-glasgow/menu',
         'slug': 'mcdonalds_finnieston',
         'image':'static/images/mcd.jpg'}
    ]

    for p in places:
        add_place(p['place_type'],p['place_name'],p['latitude'], p['longitude'], p['url'],p['image'], p['slug'])

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

    comments = [
        {"title": "Good Restaurant", "date": "2022-02-22", "comment": "I really enjoyed this restaurant, the staff were really nice!!"},
        {"title": "Enjoyed eating here", "date": "2022-03-01", "comment": "nice restaurant "},
        {"title": "Good food", "date": "2022-01-31", "comment": "Nice place!"},
        {"title": "Nice staff", "date": "2022-03-17", "comment": "the staff were really nice the fod wws also really goood "},
        {"title": "meh", "date": "2022-03-14", "comment": "idk what this is it certainly isnt a restaurant these people just dont care about there customers and they only care about the profits chichen the food isnt well good that it is not retty well done i must say"},
        {"title": "nice!", "date": "2022-01-14", "comment": "had a lovely night out!"}
    ]
    for c in comments:
        add_comment(c["title"], c["date"], c["comment"])


def add_comment(title, date, comment):
    Comments.objects.create(PlaceID = Place.objects.order_by('?').first(), username = User.objects.order_by("?").first(), comment = comment, date = date, title = title)


def add_place(place_type, place_name, latitude, longitude, url, slugName = '', comments = [], image = 'static/images/Default.jpg'):
    p = Place.objects.get_or_create(place_type=place_type, place_name=place_name)[0]
    p.url = url
    p.latitude = latitude
    p.longitude = longitude
    p.slug = slugName
    p.comments = comments
    file_obj1 = DjangoFile(open(image, mode='rb'), name=image)
    p.place_image = file_obj1
    p.save()
    return p


def add_user(name,email,password):
    users = User.objects
    if users.filter(username=name).exists():
        user = User.objects.get(username=name)
    else:
        user = User.objects.create_user(name,email,password)
        u = UserProfile.objects.get_or_create(user=user)[0]
        u.save()

    return user


if __name__ == '__main__':
    print('Populating...')
    populate()