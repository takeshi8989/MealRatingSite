from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import User
from .models import Meal, Tag


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


class NewMealForm(forms.Form):
    name = forms.CharField(max_length=30, 
        widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': 'mt-3 border border-2 rounded pl-1 p-1 ml-32'}))
    imgUrl = forms.URLField(
        label='URL',
        widget=forms.TextInput(attrs={'placeholder': 'Image url', 'class': 'mt-3 border border-2 rounded pl-1 p-1 ml-36'}))
    countryOfOrigin = forms.CharField(max_length=30, label='Country of Origin',
        widget=forms.TextInput(attrs={'placeholder': 'Country of Origin', 'class': 'mt-3 border border-2 rounded pl-1 p-1 ml-12'}))
    tags = forms.ModelMultipleChoiceField(
        label='Tags', required=False, queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': 'flex flex-wrap mx-8 text-center mt-2'})
    )
    description = forms.CharField(
        required=False,
        label='',
        widget=forms.Textarea(attrs={'rows': '4', 'placeholder': 'description', 'class': 'mt-3 border border-2 rounded pl-1 p-1 ml-8'}))
    
    class Meta:
        model = Meal
        fields = ('name', 'imgUrl', 'countryOfOrigin',  'tags', 'description')