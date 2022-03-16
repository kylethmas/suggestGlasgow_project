from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Place
from rango.forms import PlaceForm
from django.shortcuts import redirect
from django.urls import reverse
from rango.forms import UserForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime





def home(request):
    context_dict = {'boldmessage': 'This is the home page'}
    return render(request, 'rango/home.html', context=context_dict)

#might come in useful later :)
def show_category(request, category_name_slug):
    
    context_dict = {}
    
    try:
        category = Category.objects.get(slug = category_name_slug)
        
        pages = Page.objects.filter(category = category)
        
        context_dict['pages'] = pages
        context_dict['category'] = category
        
    except Category.DoesNotExist:
        
        context_dict['category'] = None
        context_dict['pages'] = None
        
    return render(request, 'rango/category.html', context = context_dict)
   

@login_required    
def add_place(request):
    form = PlaceForm()
        
    if request.method == 'POST':
        form = PlaceForm(request.POST)


    if form.is_valid():
        place.save()
        print("Page has been saved!!!")

    else:
        print(form.errors)

    context_dict = {'form': form}
    return render(request, 'rango/add_place.html', context=context_dict)


def sign_up(request):

    registered = False;
    
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        
        if user_form.is_valid():
            user = user_form.save()
            
            user.set_password(user.password)
            user.save()
           
            registered = True
            
        else:
            print(user_form.errors, profile_form.errors)
    
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
                return HttpResponse("Your suggestGlasgow account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'rango/login.html')


@login_required
def profile(request):
    return render(request, 'rango/profile.html')

    
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('suggestGlasgow:home'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if "picture" in request.FILES:
                profile.picture = request.FILES["picture"]

            profile.save()
            registered = True

        else:
            #invalid form
            print(user_form.errors, profile_form.errors)

    else:
        #not http post
        user_form = UserForm()
        profile_form = UserProfileForm()

    return  render(request, "rango/register.html",
                   context = {"user_form": user_form,
                              "profile_form": profile_form,
                              "registered": registered})


