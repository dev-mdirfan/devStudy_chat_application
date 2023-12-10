from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rooms.models import Topic
from django.contrib import messages
from .models import Profile

# @login_required
def profile(request, pk):
    profile = Profile.objects.get(id=pk)
    rooms = profile.user.room_set.all()
    room_messages = profile.user.message_set.all()
    topics = Topic.objects.all()
    context = {
        'profile': profile,
        'rooms': rooms,
        'room_messages': room_messages,
        'topics': topics,
    }
    return render(request, 'users/profile.html', context)