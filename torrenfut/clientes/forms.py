from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class ClienteRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, label='Nome')
    last_name = forms.CharField(max_length=50, required=True, label='Sobrenome')
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class EditarPerfilForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']  
