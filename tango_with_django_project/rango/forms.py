from django import forms
from django.contrib.auth.models import User
from rango.models import Page, Category, UserProfile

class CategoryForm(forms.ModelForm):
  name = forms.CharField(max_length=128, help_text="Please enter the category name.")
  views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
  likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

  class Meta:
    model = Category

class PageForm(forms.ModelForm):
  categories_values = Category.objects.all()
  categories_values_as_tuple = ()
  # this may be quite slow  
  for category in categories_values:
    new =  (category.name, category.name), 
    categories_values_as_tuple += new

  title= forms.CharField(max_length=128, help_text="Please enter the title of the page")
  url = forms.URLField(max_length=200, help_text="Please enter the URL of page")
  views = forms.IntegerField(widget= forms.HiddenInput(), initial=0)
  categories = forms.ChoiceField(choices=categories_values_as_tuple, required=True, label='Select Category')

  def clean(self):
    cleaned_data  = self.cleaned_data
    url = cleaned_data.get('url')
    if url and not url.startswith('http://'):
      url = 'http://' + url
      cleaned_date['url'] = url
    return cleaned_data
  
  class Meta:
    model=Page
    fields = ('title', 'url', 'views')

class UserForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput())

  class Meta:
    model = User 
    fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
  class Meta:
    model= UserProfile
    fields = ('website', 'picture')
