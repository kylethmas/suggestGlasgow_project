from django.shortcuts import render, redirect
from django.http import HttpResponse
from rango.models import Category, Place, UserProfile
from rango.forms import PlaceForm, UserForm, UserProfileForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.views import View
from django.utils.decorators import method_decorator
import random


def home(request):
    place_list = Place.objects.filter(place_type="Cafe")
    random_place = random.choice(place_list)
    context_dict = {}
    context_dict['places'] = place_list
    context_dict['place'] = random_place
    return render(request, 'rango/home.html', context=context_dict)
    
def example_place(request):
    return render(request, 'rango/ExamplePlace.html')

def show_place(request, place_name_slug):
    
    context_dict = {}
    
    try:
        #place = Place.objects.get(slug = place_name_slug)
        place = Place.objects.get(place_name = place_name_slug)
        context_dict['place'] = place
        
    except Place.DoesNotExist:
        
        context_dict['place'] = None
        
    return render(request, 'rango/place.html', context = context_dict)


@login_required
def add_place(request):
    form = PlaceForm()
        
    if request.method == 'POST':
        form = PlaceForm(request.POST)

    if form.is_valid():
        form.save()
        print("Page has been saved!!!")
        # NOT WORKING REDIRECT
        return redirect(reverse('rango:show_place',
                                kwargs={'place_name_slug':
                                            place_name_slug}))

    else:
        print(form.errors)
        print("Page has wrong!!!")
        print(form.errors)
        #return redirect('/')

    context_dict = {'form': form}
    return render(request, 'rango/add_place.html', context=context_dict)


def sign_up(request):

    registered = False
    
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid():
            user = user_form.save()
            
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save()
            profile.user = user
            profile.save()
            
            registered = True
            
        else:
            print(user_form.errors, profile_form.errors)
    
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        
    return render(request, 'rango/signup.html',
            context = {'user_form' : user_form,
                       'profile_form': profile_form,
                       'registered' : registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('suggestGlasgow:home'))
            else:
                #account not active
                return HttpResponse("Oops.. your account is disabled.")
        else:
            #invalid login
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:
        #not http post, retutn to login
        return render(request, 'rango/login.html')

@login_required
def profile(request):
    return render(request, 'rango/profile.html')

    
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('suggestGlasgow:home'))


class LikePlaceView(View):
    @method_decorator(login_required)
    def get(self, request):
        place_id = request.GET['place_id']
        try:
            place = Place.objects.get(PlaceID = place_id)
            #request.user.userprofile.liked.add(place)
            
        except Place.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        
        #current_user = request.user
        #a = UserProfile.objects.get(user = current_user)
        #a.liked.add(place.PlaceID)
        #a.liked.add("10")
        #liked.add(UserProfile.objects.get(user = current_user))
        #a.save()
        
        
        place.likes = place.likes + 1
        place.save()
    
        return HttpResponse(place.likes)
        
class DislikePlaceView(View):
    @method_decorator(login_required)
    def get(self, request):
        place_id = request.GET['place_id']
        try:
            place = Place.objects.get(PlaceID = place_id)

        except Place.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
    
        place.dislikes = place.dislikes + 1
        place.save()
    
        return HttpResponse(place.dislikes)

class SavePlaceView(View):
    @method_decorator(login_required)
    def get(self, request):
        place_id = request.GET['place_id']

        try:
            place = Place.objects.get(PlaceID = place_id)

        except Place.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        
        #p = Page.objects.get_or_create(category=category, title=title, url=url)
        
        #pages = Page.objects.filter(category=category).order_by('-views')
        user = UserProfile
        user.saved.extend(place)
        #return render(request, 'rango/page_listing.html', {'pages': pages})


