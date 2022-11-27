from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    username = forms.CharField(label='', 
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'mt-3 border border-2 rounded pl-1 p-2'}))
    password1 = forms.CharField(label='', 
        widget=forms.TextInput(attrs={'placeholder': 'Password', 'class': 'mt-3 border border-2 rounded pl-1 p-2'}))
    password2 = forms.CharField(label='', 
        widget=forms.TextInput(attrs={'placeholder': 'Password confirm', 'class': 'mt-3 border border-2 rounded pl-1 p-2'}))
    last_name = forms.CharField(
        label='',
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'mt-3 border border-2 rounded pl-1 p-2'})
    )
    first_name = forms.CharField(
        label='',
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'mt-3 border border-2 rounded pl-1 p-2'})
    )
    email = forms.EmailField(
        label='',
        max_length=254,
        widget=forms.TextInput(attrs={'placeholder': 'email address', 'class': 'mt-3 border border-2 rounded pl-1 p-2'})
    )

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name',  'email', 'password1')