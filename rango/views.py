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
    context_dict = {}
    form = SuggestForm()
    if request.method == 'POST':
        form = SuggestForm(request.POST)
        if form.is_valid():
            category = form['place_type'].value()
            place_list = Place.objects.filter(place_type=category)
            if len(place_list) > 1 :
                random_place = random.choice(place_list)
            else:
                random_place = place_list[0]
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
        user = User.objects.get(username = request.user)
        context_dict['place'] = place
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
    form = PlaceForm()
    
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        print("hi")
        
        if form.is_valid():
            form.save()

            print("Page has been saved!!!")
            name = form['place_name'].value()
            place = Place.objects.get(place_name=name)
            print(place)

            return redirect(reverse('suggestGlasgow:show_place',
                                        kwargs={'place_name_slug':
                                                    place.slug}))

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
        
        if user_form.is_valid():
            #user = user_form.save()
            print(user_form.data['username'])
            print(user_form.data['email'])
            user = User.objects.create_user(user_form.data['username'], user_form.data['email'], user_form.data['password'])
            user.set_password(user.password)
            user.save()
            u = UserProfile.objects.get_or_create(user=user)[0]
            u.save()

            registered = True
            return redirect(reverse('suggestGlasgow:home'))
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

    #return HttpResponseRedirect(reverse('show_place', args=[str(post)]))
    return HttpResponseRedirect(reverse('suggestGlasgow:show_place',
                     kwargs={'place_name_slug':
                                 slug}))
