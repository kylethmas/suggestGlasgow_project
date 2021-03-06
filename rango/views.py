from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views import View
from django.utils.decorators import method_decorator
from django.core import serializers
from rango.models import Place, User, UserProfile, Comments
from rango.forms import PlaceForm, SuggestForm, UserForm
from datetime import datetime
import datetime
import random

# the view for home, can return randomly generated suggestions based on the users chosen category 
# also will return the place of the week
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
                # invalid category > this is for development purposes
                print(e)
            if len(place_list) > 1:
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
    context_dict['reccomendation'] = Place.objects.get(slug='mactassos')
    return render(request, 'rango/home.html', context=context_dict)

# this will redirect the user to a place page
def show_place(request, place_name_slug, **kwargs):
    context_dict = {}

    try:
        place = Place.objects.get(slug=place_name_slug)
        print(request.user)
        context_dict['place'] = place
        if request.user.username != "":
            user = User.objects.get(username=request.user)

        def get_context_data(self, **kwargs):
            context_dict = super().get_context_data(**kwargs)
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
            context_dict['post_is_saved'] = saved
            return context_dict

    except Place.DoesNotExist:

        context_dict['place'] = None

    return render(request, 'rango/Place.html', context=context_dict)


#this is the view to add a place to the website, users need to be logged in to access this
@login_required
def add_place(request):
    if request.method == 'POST':
        place_form = PlaceForm(request.POST)

        if place_form.is_valid():

            print("Page has been saved!!!")
            place = place_form.save(commit=False)

            if 'place_image' in request.FILES:
                print(request.FILES['place_image'])
                place.place_image = request.FILES['place_image']
            place.save()

            return redirect(reverse('suggestGlasgow:show_place',
                                    kwargs={'place_name_slug':
                                                place.slug}))

        else:
            print(place_form.errors)
            place = PlaceForm()
    else:
        place = PlaceForm()

    context_dict = {'form': place}
    return render(request, 'rango/add_place.html', context=context_dict)


#this is the view to allow our users to sign up
def sign_up(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = User.objects.create_user(user_form.cleaned_data['username'], user_form.cleaned_data['email'],
                                            user_form.cleaned_data['password'])
            u = UserProfile.objects.get_or_create(user=user)[0]
            u.save()

            # need to add back in user profile stuff
            login(request, user)
            registered = True
            return redirect(reverse('suggestGlasgow:home'))
        else:
            print(user_form.errors)

    else:
        user_form = UserForm()

    return render(request, 'rango/signup.html',
                  context={'user_form': user_form,
                           'registered': registered})

# this is the view to allow our users to log in
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
                # account not active
                return HttpResponse("Oops.. your account is disabled.")
        else:
            # invalid login
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:
        # not http post, retutn to login
        return render(request, 'rango/login.html')


# this is the view which will display the saved places on the profile page
@login_required
def profile(request):
    user = get_object_or_404(UserProfile, user=request.user)
    context_dict = {}
    context_dict['saved'] = user.saves.all()
    print(context_dict)

    return render(request, 'rango/profile.html', context=context_dict)

# this view allows the user to log out
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('suggestGlasgow:home'))

# this view allows a user to like and then unlike a place (if they have already liked it)
def place_like(request, slug):
    post = get_object_or_404(Place, slug = slug)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('suggestGlasgow:show_place',
                                        kwargs={'place_name_slug':
                                                    slug}))

# this view allows a user to dislike and then undislike a place (if they have already disliked it)
def place_dislike(request, slug):
    post = get_object_or_404(Place, slug = slug)
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)

    return HttpResponseRedirect(reverse('suggestGlasgow:show_place',
                                        kwargs={'place_name_slug':
                                                    slug}))

# this allows a user to save and unsave a place from the place's page
def place_save(request, slug):
    post = get_object_or_404(Place, slug = slug)

    user = get_object_or_404(UserProfile, user=request.user)
    if user.saves.filter(PlaceID=post.PlaceID).exists():
        user.saves.remove(post)
    else:
        user.saves.add(post)

    return redirect(reverse('suggestGlasgow:show_place',
                                        kwargs={'place_name_slug': post.slug}))
                                        
# this view allows a user to unsave a place from the profile page                                       
def place_unsave(request, slug):
    post = get_object_or_404(Place, slug = slug)
    user = get_object_or_404(UserProfile, user=request.user)
    user.saves.remove(post)

    return redirect(reverse('suggestGlasgow:profile'))

# this view posts the comment for a place
def get_comments_for_place(request):
    Start = int(request.GET.get("start")) or 0
    if(Start < 0): Start = 0
    QueriedComments = Comments.objects.filter(PlaceID = Place.objects.filter(slug = request.GET.get("slug")).first()).order_by("-date")[Start:Start + 5] #Apparently, this actually makes the sql have LIMIT 5 instead of slicing after querying everything...
    CommentsArray = []
    for Comment in QueriedComments:
        CommentsArray.append({
            "Username": Comment.username.username,
            "Title": Comment.title,
            "Comment": Comment.comment,
            "Date": Comment.date
        })
    return JsonResponse(CommentsArray, safe=False)

# this view lets a logged in user add a comment
@login_required
def post_comment(request, slug):
    print("hiu")
    print(request.POST.get("Comment"))
    Comments.objects.create(PlaceID = Place.objects.filter(slug = slug).first(), username = User.objects.filter(id=request.GET.get("userid")).first(), comment = request.POST.get("Comment"), date = datetime.datetime.now().isoformat()[:10], title = request.POST.get("Title"))
    return HttpResponseRedirect(reverse('suggestGlasgow:show_place',
                                        kwargs={'place_name_slug': slug}))
