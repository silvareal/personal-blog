from django import forms
from django.contrib.auth.models import User
from pagedown.widgets import PagedownWidget

from .models import Post, Profile


class PostForm(forms.ModelForm):
    publish = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = Post
        fields = [
            "title",
            "image",
            "image_info",
            "author",
            "content",
            "tags",
            "publish",
            "status"
        ]

class PostEmail(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False,
    widget=forms.Textarea)

class ResumeMail(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, required=False, help_text="optional")
    last_name = forms.CharField(max_length=20, required=False, help_text='optional')
    email     = forms.EmailField(max_length=200, help_text="Required, use a valid email")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
'''
from django.contrib.auth.models import User
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password",
                            widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Password",
                            widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('password don\'t match')
        return cd['password2']'''

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
