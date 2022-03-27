from django.conf.urls import url
from django.urls import path
from rango import views

LOGIN_URL = 'rango:login'
app_name = 'suggestGlasgow'


urlpatterns = [
    path('', views.home, name='home'),
    path('Places/<slug:place_name_slug>/', views.show_place, name = 'show_place'),
    path('SignUp/', views.sign_up, name='sign up'),
    path('Login/', views.user_login, name='login'),
    path('Profile/', views.profile, name='profile'),
    path('LogOut/', views.user_logout, name='logout'),
    path('Profile/AddPlace/', views.add_place, name='add place'),
    path('place-like/<str:slug>', views.place_like, name="place_like"),
    path('place-dislike/<str:slug>', views.place_dislike, name="place_dislike"),
    path('place-save/<str:slug>', views.place_save, name="place_save"),
    path('place-unsave/<str:slug>', views.place_unsave, name="place_unsave"),
    path("GetComments/", views.get_comments_for_place, name="get_comments_for_place"),
    path("PostComment/<str:slug>", views.post_comment, name="post_comment")
]
