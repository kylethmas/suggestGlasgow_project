from django.conf.urls import url
from django.urls import path
from rango import views

app_name = 'suggestGlasgow'

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:category_name_slug>/', views.show_category, name = 'show_category'),
    #path('add_category/', views.add_category, name='add_category'),
    #path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    path('SignUp/', views.sign_up, name='sign up'),
    path('Login/', views.user_login, name='login'),
    path('Profile/', views.profile, name='profile'),
    path('LogOut/', views.user_logout, name='logout'),
    path('Profile/AddPlace/', views.add_place, name='add place'),
]