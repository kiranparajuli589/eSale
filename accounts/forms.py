from .models import User, UserProfile
from django import forms
from django.contrib.auth.forms import UserCreationForm as UserForm


class UserCreationForm(UserForm):
    email = forms.EmailField

    class Meta:
        model = User
        fields = ['f_name', 'l_name', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'f_name', 'l_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'image']


class ChangePassword(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_pass1 = forms.CharField(widget=forms.PasswordInput)
    new_pass2 = forms.CharField(widget=forms.PasswordInput)
