from django.forms import ModelForm
from .models import Room

class Room_form(ModelForm):
    class Meta:
        model=Room
        fields = '__all__'
        exclude = [
            'host',
            'participants'
        ]
        labels = {
            'topic':'主題',
            'name':'標題',
            'description':'內文'
        }