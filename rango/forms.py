from django import forms
from rango.models import Place
from django.contrib.auth.models import User
from rango.models import UserProfile
            
class PlaceForm(forms.ModelForm):
    place_name = forms.CharField(max_length = 128, help_text = "Place name")
    place_type = forms.CharField(max_length = 128, help_text = "Place type") #this will be a drop down menu
    place_map = forms.CharField(max_length = 128, help_text = "Approximate Location") # this will be a map interface
    url = forms.URLField(max_length = 200, help_text = "Website (optional)") #optional?
    likes = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)
    dislikes = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)
    
    class Meta:
        model = Place
        exclude = ('category',)
        
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
            
        return cleaned_data
        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        

#class UserProfileForm(forms.ModelForm):
 #   class Meta:
  #      model = UserProfile
   #     fields = ('picture',)