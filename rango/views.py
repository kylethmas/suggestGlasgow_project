from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views import View
from django.utils.decorators import method_decorator
from rango.models import Place, Ratings, Category, User, UserProfile
from rango.forms import PlaceForm, SuggestForm, UserForm
from datetime import datetime
import random


def home(request):
    place_list = Place.objects.all()
    context_dict = {}
    form = SuggestForm()
    try:
        random_place = random.choice(place_list)
        context_dict['place'] = random_place
    except Exception as e:
        # likely the database isnt populated need to handle this > force an error page?
        print(e)
        random_place = None
    if request.method == 'POST':
        form = SuggestForm(request.POST)
        if form.is_valid():
            category = form['place_type'].value()
            try:
                # place_type validation is from tuple "place_types" defined in forms.py AND field "choices" in "place_type" from "Place" class in models.py
                place_list = Place.objects.filter(place_type=category)
            except Exception as e:
                #invalid category > this is for development purposes
                print(e)
            if len(place_list) > 1 :
                random_place = random.choice(place_list)
            elif len(place_list) == 1:
                random_place = place_list[0]
            else:
                # can change this for speed as this is predefined
                random_place = random.choice(Place.objects.all())
            print(category, random_place)
            return redirect(reverse('suggestGlasgow:show_place',
                                    kwargs={'place_name_slug':
                                                random_place.slug}))
        else:
            print(form.errors)
    context_dict['form'] = form
    return render(request, 'rango/home.html', context=context_dict)

def suggest_place(request):
    form = SuggestForm()
    if request.method == 'POST':
        form = SuggestForm(request.POST)
        if form.is_valid():
            category = form['place_type'].value()
            place_list = Place.objects.filter(place_type=category)
            random_place = random.choice(place_list)
            print(category, random_place)
        else:
            print(form.errors)
    return render(request, 'rango/home.html')

def example_place(request):
    return render(request, 'rango/ExamplePlace.html')

def show_place(request, place_name_slug, **kwargs):
    
    context_dict = {}
    
    try:
        #place = Place.objects.get(slug = place_name_slug)
        place = Place.objects.get(slug = place_name_slug)
        print(request.user)
        context_dict['place'] = place
        if request.user.username != "":
            user = User.objects.get(username = request.user)

        #model = Place

        def get_context_data(self, **kwargs):
            data = super().get_context_data(**kwargs)
            likes_connected = get_object_or_404(place, slug=self.kwargs['slug'])
            liked = False
            if likes_connected.likes.filter(id=self.request.user.id).exists():
                liked = True

            context_dict['number_of_likes'] = likes_connected.number_of_likes()
            context_dict['post_is_liked'] = liked

            disliked = False
            if likes_connected.dislikes.filter(id=self.request.user.id).exists():
                disliked = True
            context_dict['number_of_dislikes'] = likes_connected.number_of_likes()
            context_dict['post_is_disliked'] = disliked

            user_connected = get_object_or_404(user, user=self.kwargs['user'])
            saved = false
            if user_connected.saves.filter(slug=self.request.place.slug).exists():
                saved = True
            data['post_is_saved'] = saved

    except Place.DoesNotExist:
        
        context_dict['place'] = None
        
    return render(request, 'rango/place.html', context = context_dict)

@login_required
def add_place(request):

    if request.method == 'POST':
        place = PlaceForm(request.POST)
        print("hi")

        if place.is_valid():

            print("Page has been saved!!!")

            #if 'place_image' in request.FILES:
             #   place.place_image = request.FILES['place_image']

            place.save()

            name = place['place_name'].value()
            place_get = Place.objects.get(place_name=name)
            print(place_get.slug)
            #return redirect(reverse('suggestGlasgow:show_place',
                                        #kwargs={'place_name_slug':
                                                    #place_get.slug}))
            redirect(reverse('suggestGlasgow:home'))

        else:
            print(place.errors)

    else:
        place = PlaceForm()

    context_dict = {'form': place}
    return render(request, 'rango/add_place.html', context=context_dict)


def sign_up(request):

    registered = False
    
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        
        if user_form.is_valid():
            user = User.objects.create_user(user_form.cleaned_data['username'], user_form.cleaned_data['email'], user_form.cleaned_data['password'])
            u = UserProfile.objects.get_or_create(user=user)[0]
            u.save()
            
            # need to add back in user profile stuff


            registered = True
            return redirect(reverse('suggestGlasgow:login'))
        else:
            print(user_form.errors)
        
    else:
        user_form = UserForm()
        
    return render(request, 'rango/signup.html',
            context = {'user_form' : user_form,
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
    user = get_object_or_404(UserProfile, user=request.user)
    context_dict = {}
    context_dict['saved'] = user.saves.all()
    print(context_dict)
    return render(request, 'rango/profile.html', context=context_dict)

    
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('suggestGlasgow:home'))


def PlaceLike(request, slug):
    post = get_object_or_404(Place, slug =request.POST.get('slug'))
    print(post)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    #return HttpResponseRedirect(reverse('show_place', args=[str(post)]))
    return HttpResponseRedirect(reverse('suggestGlasgow:show_place',
                     kwargs={'place_name_slug':
                                 slug}))

def PlaceDislike(request, slug):
    post = get_object_or_404(Place, slug =request.POST.get('slug'))
    print(post)
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)

    #return HttpResponseRedirect(reverse('show_place', args=[str(post)]))
    return HttpResponseRedirect(reverse('suggestGlasgow:show_place',
                     kwargs={'place_name_slug':
                                 slug}))
def PlaceSave(request, slug):
    post = get_object_or_404(Place, slug =request.POST.get('slug'))
    user = get_object_or_404(UserProfile,user = request.user)
    print(post,user)
    if user.saves.filter(PlaceID=post.PlaceID).exists():
        user.saves.remove(post)
    else:
        user.saves.add(post)

    return HttpResponseRedirect(reverse('suggestGlasgow:show_place',
                     kwargs={'place_name_slug': slug}))


    # p = Page.objects.get_or_create(category=category, title=title, url=url)

    # pages = Page.objects.filter(category=category).order_by('-views')
    # user = UserProfile
    # user.saved.extend(place)
    # return render(request, 'rango/page_listing.html', {'pages': pages})