from django.test import TestCase
from rango.models import Place, User, UserProfile
from django.urls import reverse
from rango import forms
from django.db import models
import rango.models
from population_script import populate

# Create your tests here.
class PlaceMethodTests(TestCase):
    def test_slug_line_creation(self):
        """
        Checks to make sure that when a place is created, an
        appropriate slug is created.
        Example: "Random Place String" should be "random-place-string".
        """
        place = Place(place_name='Random Place String')
        place.save()
        self.assertEqual(place.slug, 'random-place-string')
        
    def test_name_creation(self):
        """
        Checks to make sure that when a place is created, an
        appropriate name is created.
        Example: "Random Place String" should be "Random Place String".
        """
        place = Place(place_name='Random Place String')
        place.save()
        self.assertEqual(place.place_name, 'Random Place String')
        
    def test_type_creation(self):
        """
        Checks to make sure that when a place is created, an
        appropriate type is created.
        Example: type should be "Cafe".
        """
        place = Place(place_type = 'Cafe')
        place.save()
        self.assertEqual(place.place_type, 'Cafe')
        
    def test_latitude_creation(self):
        """
        Checks to make sure that when a place is created, an
        appropriate latitude is created.
        Example: latitude should be "55.46".
        """
        place = Place(latitude = '55.46')
        place.save()
        self.assertEqual(place.latitude, '55.46')
        
    def test_longitude_creation(self):
        """
        Checks to make sure that when a place is created, an
        appropriate longitude is created.
        Example: latitude of "Random Place String" should be "55.46".
        """
        place = Place(longitude = '4.54' )
        place.save()
        self.assertEqual(place.longitude, '4.54')

    def test_default_image_creation(self):
        """
        Checks to make sure that when a place is created without 
        specifiying an image, an default image is created.
        Example: default image should be "/place_images/Default.jpg".
        """
        place = Place()
        place.save()
        self.assertEqual(place.place_image, "/place_images/Default.jpg")
       
    def test_added_image_creation(self):
        """
        Checks to make sure that when a place is created, an
        appropriate image is created.
        Example: image should be "Testing.jpg".
        """
        place = Place(place_image = "Testing.jpg" )
        place.save()
        self.assertEqual(place.place_image, "Testing.jpg")
        
    def test_url_creation(self):
        """
        Checks to make sure that when a place is created, an
        appropriate url is created.
        Example: url should be "https://moodle.gla.ac.uk/course/view.php?id=29970".
        """
        place = Place(url = "https://moodle.gla.ac.uk/course/view.php?id=29970" )
        place.save()
        self.assertEqual(place.url, "https://moodle.gla.ac.uk/course/view.php?id=29970")
        
    def test_all_works_together(self):
        """
        Checks to make sure that when a place is created, all the 
        appropriate fields are saved.
        """
        place = Place(place_name = "Random Place String", place_type = "Cafe", place_image = "Testing.png", latitude = '55.46', longitude = '4.46', url= 'https://moodle.gla.ac.uk/course/view.php?id=29970')
        place.save()
        
        self.assertEqual(place.place_name, "Random Place String")
        self.assertEqual(place.place_type, "Cafe")
        self.assertEqual(place.place_image, "Testing.png")
        self.assertEqual(place.latitude, "55.46")
        self.assertEqual(place.longitude, "4.46")
        self.assertEqual(place.url, "https://moodle.gla.ac.uk/course/view.php?id=29970")
        self.assertEqual(place.slug, "random-place-string")
        
    
     
    def test_str_method(self):
        """
        Checks to make sure the __str__ method works.
        """
        place = Place(place_name = "Random Place String")
        place.save()
        self.assertEqual(str(place), "Random Place String")
        
    def test_number_of_likes_method(self):
        """
        Checks to make sure that when a place is created, an
        default number of likes is created.
        Example: likes should be 0.
        """
        place = Place(place_name = "Random Place String")
        place.save()
        self.assertEqual(place.number_of_likes(), 0)
        
        
    def test_number_of_dislikes_method(self):
        """
        Checks to make sure that when a place is created, an
        default number of likes is created.
        Example: dislikes should be 0.
        """
        place = Place(place_name = "Random Place String")
        place.save()
        self.assertEqual(place.number_of_dislikes(), 0)
    


class UserMethodTests(TestCase):
        
    def test_username_creation(self):
        """
        Checks to make sure that when a user is created, an
        appropriate username is created.
        Example: user.username should be "Niamh".
        """
        user = User.objects.create_user('Niamh', "n@gmail.com", "thisisabadpassword")
        u = UserProfile.objects.get_or_create(user=user)[0]
        u.save()
        self.assertEqual(user.username, "Niamh")
        
    def test_email_creation(self):
        """
        Checks to make sure that when a user is created, an
        appropriate email is created.
        Example: user.email should be "n@gmail.com".
        """
        user = User.objects.create_user('Niamh', "n@gmail.com", "thisisabadpassword")
        u = UserProfile.objects.get_or_create(user=user)[0]
        u.save()
        
        self.assertEqual(user.email, "n@gmail.com")
    
    """
    def test_password_creation(self):
        "" "
        Checks to make sure that when a user is created, an
        appropriate saves list is created.
        Example: userProfile.saves should be null.
        "" "
        user = User.objects.create_user('Niamh', "n@gmail.com", "thisisabadpassword")
        u = UserProfile.objects.get_or_create(user=user)[0]
        u.save()
        
        self.assertEqual(u.number_of_saves, 0) #why istn this working
    """

class HomeViewTests(TestCase):
    def test_if_drop_down_categories_are_present(self):
        """
        Check if the categories are displaying properly
        """
        populate()
        response = self.client.get(reverse('suggestGlasgow:home'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Restaurant')
        self.assertContains(response, 'Cafe')
        self.assertContains(response, 'Fast Food')
        self.assertContains(response, 'Nightlife')
        
    def test_if_header_works(self):
        """
        Check if the header is displaying properly
        """
        populate()
        response = self.client.get(reverse('suggestGlasgow:home'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'suggestGlasgow')
        
    def test_if_footer_works(self):
        """
        Check if the footer is displaying properly
        """
        populate()
        response = self.client.get(reverse('suggestGlasgow:home'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contact us!')


def create_a_user():
    """
    A helper function which creates a user
    """
    user = User.objects.get_or_create(username='Niamh', email='Niamh@test.com')[0]
    user.set_password('1234')
    user.save()   
    u = UserProfile.objects.get_or_create(user=user)[0]
    u.save()
    
class LogInViewTests(TestCase):
    def test_login_display(self):
        """
        Check if the log in display is working
        """
        response = self.client.get(reverse('suggestGlasgow:login'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Log in to SuggestGlasgow')
        self.assertContains(response, 'Username')
        self.assertContains(response, 'Password')
        self.assertContains(response, 'Log in')
        self.assertContains(response, 'Go back')
        self.assertContains(response, "Don't have an account? Sign up now!")
        
    def test_login(self): 
        """
        test if login works 
        """
        user = create_a_user()
        
        response = self.client.post(reverse('suggestGlasgow:login'), {'username' : 'Niamh', 'password' : '1234'})
       
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('suggestGlasgow:home'))
        
class LogOutViewTests(TestCase):
    def test_logout(self): 
        """
        test if logout works 
        """
        user = create_a_user()
        
        self.client.login(username='Niamh', password='1234')
        
        response = self.client.get(reverse('suggestGlasgow:logout'))
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('suggestGlasgow:home'))
        self.assertTrue('_auth_user_id' not in self.client.session)
        
class SignUpViewTests(TestCase):
    def test_signup_display_working(self):
        """
        Check if the sign up display is working
        """
        response = self.client.get(reverse('suggestGlasgow:sign up'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign up to SuggestGlasgow')
        self.assertContains(response, 'Username')
        self.assertContains(response, 'Password')
        self.assertContains(response, 'Email')
        self.assertContains(response, 'Log in')
        self.assertContains(response, 'Go back')
        self.assertContains(response, "Already have an account? Log in!")
        
    def test_signup_working(self):
        response = self.client.post(reverse('suggestGlasgow:sign up'), {'username' : 'Niamh', 'password' : '1234', 'email':'n@gmail.com'})

        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(len(rango.models.UserProfile.objects.all()), 1)
        self.assertTrue(self.client.login(username='Niamh', password='1234'))
        
        
class ShowPlaceViewTests(TestCase):
    def test_basic_view(self):
        """
        Check if a cafe page displays correctly
        """
        place = Place(place_name = "Niamh testing cafe", place_type = "Cafe", place_image = "Testing.png", latitude = '55.46', longitude = '4.46', url= 'https://moodle.gla.ac.uk/course/view.php?id=29970')
        place.save()
        response = self.client.get(reverse('suggestGlasgow:show_place', kwargs={'place_name_slug': place.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Niamh testing cafe")
        self.assertContains(response, 'This is in the Cafe category')
        self.assertContains(response, 'Testing.png')
        self.assertContains(response, '55.46')
        self.assertContains(response, '4.46')
        self.assertContains(response, 'https://moodle.gla.ac.uk/course/view.php?id=29970')
        self.assertContains(response,  "Click here to visit their website")
        
    def test_basic_view_restaurant(self):
        """
        Check if a restaurant page displays correctly
        """
        place = Place(place_name = "Niamh testing restaurant", place_type = "Restaurant", place_image = "Testing.png", latitude = '55.46', longitude = '4.46', url= 'https://moodle.gla.ac.uk/course/view.php?id=29970')
        place.save()
        response = self.client.get(reverse('suggestGlasgow:show_place', kwargs={'place_name_slug': place.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Niamh testing restaurant")
        self.assertContains(response, 'This is in the Restaurant category')
        self.assertContains(response, 'Testing.png')
        self.assertContains(response, '55.46')
        self.assertContains(response, '4.46')
        self.assertContains(response, 'https://moodle.gla.ac.uk/course/view.php?id=29970')
        self.assertContains(response,  "Click here to visit their website")
        
    def test_basic_view_fast_food(self):
        """
        Check if a fast food page displays correctly
        """
        place = Place(place_name = "Niamh testing fast food", place_type = "Fast Food", place_image = "Testing.png", latitude = '55.46', longitude = '4.46', url= 'https://moodle.gla.ac.uk/course/view.php?id=29970')
        place.save()
        response = self.client.get(reverse('suggestGlasgow:show_place', kwargs={'place_name_slug': place.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Niamh testing fast food")
        self.assertContains(response, 'This is in the Fast Food category')
        self.assertContains(response, 'Testing.png')
        self.assertContains(response, '55.46')
        self.assertContains(response, '4.46')
        self.assertContains(response, 'https://moodle.gla.ac.uk/course/view.php?id=29970')
        self.assertContains(response,  "Click here to visit their website")
        
    def test_basic_view_nightlife(self):
        """
        Check if a nightlife page displays correctly
        """
        place = Place(place_name = "Niamh testing bar", place_type = "Nightlife", place_image = "Testing.png", latitude = '55.46', longitude = '4.46', url= 'https://moodle.gla.ac.uk/course/view.php?id=29970')
        place.save()
        response = self.client.get(reverse('suggestGlasgow:show_place', kwargs={'place_name_slug': place.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Niamh testing bar")
        self.assertContains(response, 'This is in the Nightlife category')
        self.assertContains(response, 'Testing.png')
        self.assertContains(response, '55.46')
        self.assertContains(response, '4.46')
        self.assertContains(response, 'https://moodle.gla.ac.uk/course/view.php?id=29970')
        self.assertContains(response,  "Click here to visit their website")
        
        
    def test_likes_and_dislikes(self):
        place = Place(place_name = "Niamh testing cafe", place_type = "Cafe", place_image = "Testing.png", latitude = '55.46', longitude = '4.46', url= 'https://moodle.gla.ac.uk/course/view.php?id=29970')
        place.save()
        

        response = self.client.get(reverse('suggestGlasgow:show_place', kwargs={'place_name_slug': place.slug}))
        
        self.assertContains(response, place.likes.count())
        self.assertContains(response, place.dislikes.count())
        
        
### not working from here on out :) ###   
class AddPageViewTests(TestCase):
    def test_basic_view_not_logged_in(self):
        """
        Since the user is not logged in this page should not load
        """
        response = self.client.get(reverse('suggestGlasgow:add place'))
        
        self.assertEqual(response.status_code, 302)
        
    def test_basic_view_logged_in(self):
        """
        Since the user is logged in this page should load,
        tests ensure display is working properly
        no places will be saved here
        """
        user = create_a_user()
        
        response = self.client.post(reverse('suggestGlasgow:login'), {'username' : 'Niamh', 'password' : '1234'})
        
        response = self.client.get(reverse('suggestGlasgow:add place'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Place name")
        self.assertContains(response, "Category")
        self.assertContains(response, "Restaurant")
        self.assertContains(response, "Cafe")
        self.assertContains(response, "Fast Food")
        self.assertContains(response, "Nightlife")
        #self.assertContains(response, "Choose file")
        self.assertContains(response, "Map")
        
    def test_add_page(self):
        populate()
        response = self.client.post(reverse('suggestGlasgow:add place'), {'place_name' : 'Niamh test', 'place_type' : 'Cafe', 'place_image':'Testing.png', 'latitude': 55.67, 'longitude':4.43, 'url':"https://moodle.gla.ac.uk/course/view.php?id=29970"})
        
        #place_made = Place.get_or_create(place_name = "Niamh testing cafe")
        #print(place_made.slug)
        response = self.client.get(reverse('suggestGlasgow:show_place', kwargs={'place_name_slug': "niamh-test"}))
        
        self.assertEqual(response.url, reverse('suggestGlasgow:show_place'), kwargs={'place_name_slug': "niamh-test"})

        
class ProfileViewTests(TestCase):
    def test_basic_view_not_logged_in(self):
        """
        Since the user is not logged in this page should not load
        """
        response = self.client.get(reverse('suggestGlasgow:profile'))
        
        self.assertEqual(response.status_code, 302)
        
    def test_basic_view_logged_in(self):
        """
        Since the user is logged in this page should load,
        tests ensure display is working properly
        """
        user = create_a_user()
        response = self.client.post(reverse('suggestGlasgow:login'), {'username' : 'Niamh', 'password' : '1234'})
        
        response = self.client.get(reverse('suggestGlasgow:profile'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My places")
        self.assertContains(response, "You have no saved places. Go to the home page and find some you like!")
        self.assertContains(response, "Not finding it?")
        self.assertContains(response, "Add new place")

