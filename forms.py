from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms

class UserForm(ModelForm):
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        self.password = kwargs.pop('password') if kwargs.has_key('password') else None
        super(UserForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.password)
        if commit:
            user.save()
        return user

    def clean_username(self):
        """ Username must be unique
        """
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).count():
            raise forms.ValidationError("That username is taken.  Please choose a different one.")
        return username
        
