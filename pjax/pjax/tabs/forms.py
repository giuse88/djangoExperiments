from django import forms
from models import UserName

class NameForm(forms.ModelForm):
  name = forms.CharField(label="your name", max_length=100)
  class Meta:
     model = UserName 
     fields = ['name']



