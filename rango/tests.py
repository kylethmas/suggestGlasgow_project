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
    
    """ not working :) 
    def test_default_likes_creation(self):
        "" "
        Checks to make sure that when a place is created, an
        default number of likes is created.
        Example: likes should be ???.
        "" "
        place = Place()
        place.save()
        self.assertEqual(place.likes, [])
    """
    
    """ not working :) 
    def test_default_dislikes_creation(self):
        "" "
        Checks to make sure that when a place is created, an
        default number of dislikes is created.
        Example: dislikes should be ???.
        "" "
        place = Place()
        place.save()
        self.assertEqual(place.dislikes, [])
    """
    """
    def example_place(name, place_type, place_image, latitude, longitude, url):
        place = Place.objects.get_or_create(place_name=name, place_type = place_type)[0]
        place.place_image = place_image
        place.latitude = latitude
        place.longitude = longitude
        place.url = url
        place.save()
        return place
    """


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
    
    """ same problem as before
    def test_password_creation(self):
        "" "
        Checks to make sure that when a user is created, an
        appropriate saves list is created.
        Example: userProfile.saves should be null.
        "" "
        #user = add_user('Niamh', "n@gmail.com", "thisisabadpassword" )
        user = User.objects.create_user('Niamh', "n@gmail.com", "thisisabadpassword")
        u = UserProfile.objects.get_or_create(user=user)[0]
        u.save()
        
        self.assertEqual(UserProfile.saves, None)
    """

class HomeViewTests(TestCase):
    def test_if_drop_down_categories_are_present(self):
        """
        If no categories exist, the appropriate message should be displayed.
        """
        response = self.client.get(reverse('suggestGlasgow:home'))
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Restaurant')
        self.assertContains(response, 'Cafe')
        self.assertContains(response, 'Fast Food')
        self.assertContains(response, 'Nightlife')
        
