from django.newforms import ModelForm
from django.contrib.auth.models import User
from django import newforms as forms

class UserForm(ModelForm):
    password= forms.CharField(max_length=100, widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password')
