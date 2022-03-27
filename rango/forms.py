from django import forms
from rango.models import Place, UserProfile
from django.contrib.auth.models import User


# creates the place form likes, dislikes and slug are hiddenInput
# used for adding a place
class PlaceForm(forms.ModelForm):
    place_name = forms.CharField(max_length=128, help_text="Place name", required=True)
    place_type = forms.ChoiceField(choices=(("Restaurant", "Restaurant"),
                                            ("Cafe", "Cafe"),
                                            ("Fast Food", "Fast Food"),
                                            ("Nightlife", "Nightlife")), help_text="Category ", required=True)
    place_image = forms.ImageField(required=False)
    latitude = forms.CharField(max_length=25, help_text="Latitude of place", required=True)
    longitude = forms.CharField(max_length=25, help_text="Longitude of place", required=True)
    url = forms.CharField(max_length=200, help_text="Website (optional)", required=False)  # optional?
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0, required=False)
    dislikes = forms.IntegerField(widget=forms.HiddenInput(), initial=0, required=False)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Place
        fields = ('place_name', 'place_type', 'place_image', 'latitude', 'longitude', 'url')

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = f'https://{url}'
            cleaned_data['url'] = url

        return cleaned_data


# signup form
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


# used in the home page for redirecting
class SuggestForm(forms.ModelForm):
    place_types = (("Restaurant", "Restaurant"),
                   ("Cafe", "Cafe"),
                   ("Fast Food", "Fast Food"),
                   ("Nightlife", "Nightlife"),
                   ("Anywhere", "Anywhere"))
    place_type = forms.ChoiceField(choices=place_types, help_text="Category ")

    class Meta:
        model = Place
        fields = ('place_type',)
