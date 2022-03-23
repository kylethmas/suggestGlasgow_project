from django.conf.urls import url
from django.urls import path
from rango import views

LOGIN_URL = 'rango:login'
app_name = 'suggestGlasgow'

urlpatterns = [
    path('', views.home, name='home'),
    path('Places/<slug:place_name_slug>/', views.show_place, name = 'show_place'),
    #path('add_category/', views.add_category, name='add_category'),
    #path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    path('SignUp/', views.sign_up, name='sign up'),
    path('Login/', views.user_login, name='login'),
    path('Profile/', views.profile, name='profile'),
    path('LogOut/', views.user_logout, name='logout'),
    path('Profile/AddPlace/', views.add_place, name='add place'),
    path('ExamplePlace/', views.example_place, name='example place'),
    path('LikePlace/', views.LikePlaceView.as_view(), name='like place'),
    path('DislikePlace/', views.DislikePlaceView.as_view(), name='dislike place'),
    path('SavePlace/', views.SavePlaceView.as_view(), name='save place'),
]
