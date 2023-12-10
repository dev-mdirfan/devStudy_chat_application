from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Room, User

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']
    
    # def __init__(self, *args, **kwargs):
    #     super(MyUserCreationForm, self).__init__(*args, **kwargs)
        
    #     self.fields['password1'].widget.attrs['placeholder'] = '••••••••'
    #     self.fields['password2'].widget.attrs['placeholder'] = '••••••••'

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    # date_joined = forms.DateTimeField(disabled=True)
    class Meta:
        model = User
        # fields = ['username', 'email']
        fields = ['avatar', 'name', 'username', 'email', 'bio']

    # def __init__(self, *args, **kwargs):
    #     super(UserForm, self).__init__(*args, **kwargs)
        
    #     self.fields['name'].widget.attrs['placeholder'] = 'Enter Your Name'
    #     self.fields['username'].widget.attrs['placeholder'] = 'Enter User Name'
    #     self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'
