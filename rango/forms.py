from django import forms
from rango.models import Place, Ratings
from django.contrib.auth.models import User

place_types = (("Restaurant", "Restaurant"),
               ("Cafe", "Cafe"),
               ("Fast Food", "Fast Food"),
               ("Nightlife", "Nightlife"))


class PlaceForm(forms.ModelForm):
    place_name = forms.CharField(max_length=128, help_text="Place name", required=True)
    place_type = forms.ChoiceField(choices=place_types, help_text="Category ", required=True)
    latitude = forms.CharField(max_length=25, help_text="Latitude of place", required=True)
    longitude = forms.CharField(max_length=25, help_text="Longitude of place", required=True)  
    url = forms.CharField(max_length=200, help_text="Website (optional)", required=False)  # optional?
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    dislikes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Place
        # exclude = ('category',)
        fields = ('place_name', 'place_type', 'place_image', 'latitude', 'longitude', 'url')

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = f'https://{url}'
            cleaned_data['url'] = url

        return cleaned_data


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class SuggestForm(forms.ModelForm):
    place_type = forms.ChoiceField(choices=place_types, help_text="Category ")

    class Meta:
        model = Place
        fields = ('place_type',)


"""
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',) """
