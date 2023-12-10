from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile

class UserForm(ModelForm):
    # date_joined = forms.DateTimeField(disabled=True)
    class Meta:
        model = User
        # fields = ['username', 'email']
        fields = ['avatar', 'name', 'username', 'email', 'bio']