import sys
import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from django.core import serializers
from rango.models import Place, Category, User, UserProfile, Comments
from rango.forms import PlaceForm, SuggestForm, UserForm
from datetime import datetime
import datetime
import random

logger = logging.getLogger(__name__)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

def home(request):
    place_list = Place.objects.all()
    context_dict = {}
    form = SuggestForm()
    try:
        random_place = random.choice(place_list)
        context_dict['place'] = random_place
    except Exception as e:
        # likely the database isnt populated need to handle this > force an error page?
        logger.error('Failed to load web page: ' + str(e))
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
                logger.error('Invalid Category: ' + str(e))
            if len(place_list) > 1:
                random_place = random.choice(place_list)
            elif len(place_list) == 1:
                random_place = place_list[0]
            else:
                # can change this for speed as this is predefined
                random_place = random.choice(Place.objects.all())
            logger.info('Category: ' + category)
            logger.info('Place: ' + random_place)
            return redirect(reverse('suggestGlasgow:show_place',
                                    kwargs={'place_name_slug':
                                                random_place.slug}))
        else:
            logger.error('Form is invalid: '+ str(form.errors))
            messages.warning(request,'Form is invalid. Did you fill it out correctly?')
    context_dict['form'] = form
    context_dict['reccomendation'] = Place.objects.get(slug='mactassos')
    return render(request, 'rango/home.html', context=context_dict)


def show_place(request, place_name_slug, **kwargs):
    context_dict = {}

    try:
        # place = Place.objects.get(slug = place_name_slug)
        place = Place.objects.get(slug=place_name_slug)
        logger.info('Request from: ' + request.user)
        context_dict['place'] = place
        if request.user.username != "":
            user = User.objects.get(username=request.user)

        # model = Place

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
            saved = False
            if user_connected.saves.filter(slug=self.request.place.slug).exists():
                saved = True
            context_dict['post_is_saved'] = saved
            return context_dict

    except Place.DoesNotExist:

        logger.error('Place does not exist.')
        context_dict['place'] = None

    return render(request, 'rango/place.html', context=context_dict)


@login_required
def add_place(request):
    if request.method == 'POST':
        place_form = PlaceForm(request.POST)

        if place_form.is_valid():

            logger.debug("Page has been saved.")
            place = place_form.save(commit=False)

            if 'place_image' in request.FILES:
                logger.info(request.FILES['place_image'])
                place.place_image = request.FILES['place_image']
            place.save()

            return redirect(reverse('suggestGlasgow:show_place',
                                    kwargs={'place_name_slug':
                                                place.slug}))

        else:
            logger.info('Failed to add place: ' + place.errors)
            messages.warning(request,'Failed to add place. Did you fill out the form correctly?')

    else:
        place = PlaceForm()

    context_dict = {'form': place}
    return render(request, 'rango/add_place.html', context=context_dict)


def sign_up(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = User.objects.create_user(user_form.cleaned_data['username'], user_form.cleaned_data['email'],
                                            user_form.cleaned_data['password'])
            u = UserProfile.objects.get_or_create(user=user)[0]
            u.save()
            
            messages.success(request,'Succesfully created user!')
            logger.info('Successfully created %(user)s' % ({'user': user_form.cleaned_data['username']}))

            # need to add back in user profile stuff
            login(request, user)
            registered = True
            return redirect(reverse('suggestGlasgow:home'))
        else:
            messages.info(request,'Failed to create user. Did you fill out the form?')
            logger.info('Failed to create user: ' + user_form.errors)

    else:
        user_form = UserForm()

    return render(request, 'rango/signup.html',
                  context={'user_form': user_form,
                           'registered': registered})


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
            messages.warning(request, 'Invalid login details.')
            logger.error(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:
        # not http post, retutn to login
        return render(request, 'rango/login.html')


@login_required
def profile(request):
    user = get_object_or_404(UserProfile, user=request.user)
    context_dict = {}
    context_dict['saved'] = user.saves.all()
    logger.info(context_dict)

    return render(request, 'rango/profile.html', context=context_dict)


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('suggestGlasgow:home'))


def PlaceLike(request, slug):
    post = get_object_or_404(Place, slug=request.POST.get('slug'))
    print(post)
    if post.likes.filter(id=request.user.id).exists():
        messages.info(request, 'You unliked this place.')
        logger.info('%(user)s unliked %(place)s' % ({'user': request.user, 'place': post.place_name}))
        post.likes.remove(request.user)
    else:
        messages.success(request, 'You liked this place.')
        logger.info('%(user)s liked %(place)s' % ({'user': request.user, 'place': post.place_name}))
        post.likes.add(request.user)

    # return HttpResponseRedirect(reverse('show_place', args=[str(post)]))
    return HttpResponseRedirect(reverse('suggestGlasgow:show_place',
                                        kwargs={'place_name_slug':
                                                    slug}))


def PlaceDislike(request, slug):
    post = get_object_or_404(Place, slug=request.POST.get('slug'))
    print(post)
    if post.dislikes.filter(id=request.user.id).exists():
        messages.info(request, 'You removed your dislike for this place.')
        logger.info('%(user)s removed disliked for %(place)s' % ({'user': request.user, 'place': post.place_name}))
        post.dislikes.remove(request.user)
    else:
        messages.info(request, 'You disliked this place.')
        logger.info('%(user)s disliked %(place)s' % ({'user': request.user, 'place': post.place_name}))
        post.dislikes.add(request.user)

    # return HttpResponseRedirect(reverse('show_place', args=[str(post)]))
    return HttpResponseRedirect(reverse('suggestGlasgow:show_place',
                                        kwargs={'place_name_slug':
                                                    slug}))


def PlaceSave(request, slug):
    post = get_object_or_404(Place, slug=request.POST.get('slug'))
    user = get_object_or_404(UserProfile, user=request.user)
    print(post, user)
    if user.saves.filter(PlaceID=post.PlaceID).exists():
        logger.info('%(user)s removed %(place)s' % ({'user': request.user, 'place': post.place_name}))
        user.saves.remove(post)
    else:
        logger.info('%(user)s saved %(place)s' % ({'user': request.user, 'place': post.place_name}))
        user.saves.add(post)

    return HttpResponseRedirect(reverse('suggestGlasgow:show_place',
                                        kwargs={'place_name_slug': slug}))


def PlaceUnsave(request, slug):
    post = get_object_or_404(Place, slug=request.POST.get('slug'))
    user = get_object_or_404(UserProfile, user=request.user)
    logger.info('%(user)s removed %(place)s' % ({'user': request.user, 'place': post.place_name}))
    user.saves.remove(post)

    return HttpResponseRedirect(reverse('suggestGlasgow:profile'))

    # p = Page.objects.get_or_create(category=category, title=title, url=url)

    # pages = Page.objects.filter(category=category).order_by('-views')
    # user = UserProfile
    # user.saved.extend(place)
    # return render(request, 'rango/page_listing.html', {'pages': pages})

def GetCommentsForPlace(request):
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

@login_required
def PostComment(request, slug):
    logger.info('%(user)s posted comment' % ({'user': request.user}))
    logger.info(request.POST.get("Comment"))
    Comments.objects.create(PlaceID = Place.objects.filter(slug = slug).first(), username = User.objects.filter(id=request.GET.get("userid")).first(), comment = request.POST.get("Comment"), date = datetime.datetime.now().isoformat()[:10], title = request.POST.get("Title"))
    return HttpResponseRedirect(reverse('suggestGlasgow:show_place',
                                        kwargs={'place_name_slug': slug}))
