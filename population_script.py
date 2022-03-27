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
         'url': 'https://kylescatering.ie/delivery/kyles-cafe/',
         'slug': 'cafe_kyle',
         'image': 'static/images/cafekyle.jpg'},
        {'place_type': 'Cafe',
         'place_name': 'Broken Clock Cafe & Patisserie',
         'latitude': '55.87511461980813',
         'longitude': '-4.278286866652939',
         'url': 'https://www.brokenclockcafe.co.uk/',
         'slug': 'broken_clock_cafe_&_patisserie',
         'image': 'static/images/brokenclock.jpg'},
        {'place_type': 'Cafe',
         'place_name': 'Grosvenor Cafe',
         'latitude': '55.87505232331034',
         'longitude': '-4.2933452926161975',
         'url': 'https://kylescatering.ie/delivery/kyles-cafe/',
         'slug': 'grosvenor_cafe',
         'image': 'static/images/grosvenor.jpg'},
        {'place_type': 'Cafe',
         'place_name': 'Cafe Go-Go',
         'latitude': '55.87629126929047',
         'longitude': '-4.291863274875268',
         'url': 'https://facebook.com/cafegogo',
         'slug': 'cafe_gogo',
         'image': 'static/images/gogo.jpg'},

        {'place_type': 'Nightlife',
         'place_name': 'Bamboo',
         'latitude': '55.87226',
         'longitude': '-4.27247',
         'url': 'http://www.bamboonightclub.co.uk/',
         'slug': 'bamboo',
         'image': 'static/images/bamboo.jpg'},
        {'place_type': 'Nightlife',
         'place_name': 'Glasgow University Union',
         'latitude': '55.87321019497019',
         'longitude': '-4.285060677314717',
         'url': 'http://www.guu.co.uk/',
         'slug': 'guu',
         'image': 'static/images/guu.jpg'},
        {'place_type': 'Nightlife',
         'place_name': "Kitty O'Shea's",
         'latitude': '55.87604777046624',
         'longitude': '-4.28234978665845',
         'url': 'https://kitty-osheas.com/glasgow-west-end/',
         'slug': 'kitty_osheas',
         'image': 'static/images/kittys.jpg'},
        {'place_type': 'Nightlife',
         'place_name': 'Driftwood Bar',
         'latitude': '55.86684366239111',
         'longitude': '-4.270592948782458',
         'url': 'http://www.driftwood-glasgow.foodndrinkscotland.co.uk/',
         'slug': 'driftwood_bar',
         'image': 'static/images/driftwood.jpg'},

        {'place_type': 'Restaurant',
         'place_name': 'Sugo',
         'latitude': '55.87226',
         'longitude': '-4.27247',
         'url': 'https://www.sugopasta.co.uk/',
         'slug': 'sugo',
         'image': 'static/images/sugo.jpg'},
        {'place_type': 'Restaurant',
         'place_name': 'MacTassos',
         'latitude': '55.867546761164064',
         'longitude': '-4.2882667016457905',
         'url': 'https://www.tripadvisor.co.uk/Restaurant_Review-g186534-d12580740-Reviews-MacTassos-Glasgow_Scotland.html',
         'slug': 'mactassos',
         'image': 'static/images/mactassos.jpg'},
        {'place_type': 'Restaurant',
         'place_name': 'Swadish ',
         'latitude': '55.859663584492296',
         'longitude': '-4.2426970774238155',
         'url': 'http://www.swadish.co.uk/',
         'slug': 'swadish',
         'image': 'static/images/swadish.jpg'},

        {'place_type': 'Fast Food',
         'place_name': "McDonald's Finnieston",
         'latitude': '55.87226',
         'longitude': '-4.27247',
         'url': 'https://www.just-eat.co.uk/restaurants-mcdonalds-finnieston-glasgow/menu',
         'slug': 'mcdonalds_finnieston',
         'image': 'static/images/mcd.jpg'},
        {'place_type': 'Fast Food',
         'place_name': "Chilli Flames",
         'latitude': '55.87320923452359',
         'longitude': '-4.27137931220944',
         'url': 'http://www.chilliflames.co.uk/',
         'slug': 'chilli_flames',
         'image': 'static/images/chilli.jpeg'},
        {'place_type': 'Fast Food',
         'place_name': "727",
         'latitude': '55.87754509476178',
         'longitude': '-4.289429790339065',
         'url': 'https://727fastfood.com/',
         'slug': '727',
         'image': 'static/images/727.jpg'}
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


def add_place(place_type, place_name, latitude, longitude, url, image = 'static/images/Default.jpg', slugName = '', comments = []):
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