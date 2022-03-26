from django.test import TestCase
from rango.models import Place, User, UserProfile
from django.urls import reverse

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
        Example: likes should be ???.
        """
        place = Place(place_name = "Random Place String")
        place.save()
        self.assertEqual(place.number_of_likes(), 0)
        
        
    def test_number_of_dislikes_method(self):
        """
        Checks to make sure that when a place is created, an
        default number of likes is created.
        Example: likes should be ???.
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
        response = self.client.get(reverse('suggestGlasgow:home'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'suggestGlasgow')
        
    def test_if_footer_works(self):
        """
        Check if the footer is displaying properly
        """
        response = self.client.get(reverse('suggestGlasgow:home'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contact us!')
        
class LogInViewTests(TestCase):
    def test_login_box_working(self):
        """
        Check if the log in box is working
        """
        response = self.client.get(reverse('suggestGlasgow:login'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Log in to SuggestGlasgow')
        self.assertContains(response, 'Username')
        self.assertContains(response, 'Password')
        self.assertContains(response, 'Log in')
        self.assertContains(response, 'Go back')
        self.assertContains(response, "Don't have an account? Sign up now!")
        
class SignUpViewTests(TestCase):
    def test_signup_box_working(self):
        """
        Check if the log in box is working
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
        
class PlacesViewTests(TestCase):
    def test_basic_view(self):
        """
        Check if the log in box is working
        """
        place = Place(place_name = "Niamh testing cafe", place_type = "Cafe", place_image = "Testing.png", latitude = '55.46', longitude = '4.46', url= 'https://moodle.gla.ac.uk/course/view.php?id=29970')
        place.save()
        response = self.client.get(reverse('suggestGlasgow:show_place', kwargs={'place_name_slug': place.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Niamh testing cafe")
        self.assertContains(response, 'Cafe')
        self.assertContains(response, 'Testing.png')
        self.assertContains(response, '55.46')
        self.assertContains(response, '4.46')
        self.assertContains(response, 'https://moodle.gla.ac.uk/course/view.php?id=29970')
        self.assertContains(response,  "Click here to visit their website")
        
    def test_basic_view_restaurant(self):
        """
        Check if the log in box is working
        """
        place = Place(place_name = "Niamh testing restaurant", place_type = "Restaurant", place_image = "Testing.png", latitude = '55.46', longitude = '4.46', url= 'https://moodle.gla.ac.uk/course/view.php?id=29970')
        place.save()
        response = self.client.get(reverse('suggestGlasgow:show_place', kwargs={'place_name_slug': place.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Niamh testing restaurant")
        self.assertContains(response, 'Restaurant')
        self.assertContains(response, 'Testing.png')
        self.assertContains(response, '55.46')
        self.assertContains(response, '4.46')
        self.assertContains(response, 'https://moodle.gla.ac.uk/course/view.php?id=29970')
        self.assertContains(response,  "Click here to visit their website")
        
    def test_basic_view_fast_food(self):
        """
        Check if the log in box is working
        """
        place = Place(place_name = "Niamh testing fast food", place_type = "Fast Food", place_image = "Testing.png", latitude = '55.46', longitude = '4.46', url= 'https://moodle.gla.ac.uk/course/view.php?id=29970')
        place.save()
        response = self.client.get(reverse('suggestGlasgow:show_place', kwargs={'place_name_slug': place.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Niamh testing fast food")
        self.assertContains(response, 'Fast Food')
        self.assertContains(response, 'Testing.png')
        self.assertContains(response, '55.46')
        self.assertContains(response, '4.46')
        self.assertContains(response, 'https://moodle.gla.ac.uk/course/view.php?id=29970')
        self.assertContains(response,  "Click here to visit their website")
        
    def test_basic_view_nightlife(self):
        """
        Check if the log in box is working
        """
        place = Place(place_name = "Niamh testing bar", place_type = "Nightlife", place_image = "Testing.png", latitude = '55.46', longitude = '4.46', url= 'https://moodle.gla.ac.uk/course/view.php?id=29970')
        place.save()
        response = self.client.get(reverse('suggestGlasgow:show_place', kwargs={'place_name_slug': place.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Niamh testing bar")
        self.assertContains(response, 'Nightlife')
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
   
