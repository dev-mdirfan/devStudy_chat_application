from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        # It takes all the fields from the Room model
        fields = '__all__'
        # We do not want to include the host and participants fields in the form
        # Because when we create a room, we want the host to be the current user and the participants to be empty
        exclude = ['host', 'participants']
