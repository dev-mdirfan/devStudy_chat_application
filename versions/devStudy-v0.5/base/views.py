from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
# login_required is decorator that used to restrict access to certain pages
from django.contrib.auth.decorators import login_required
# User authentication imports
from django.contrib.auth import authenticate, login, logout
# User registration imports allows us to create a new user
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# filter Q is used for searching
from django.db.models import Q
from .models import Room, Topic, Message
from .forms import RoomForm

'''
rooms = [
    {'id':1, 'name':'Lets Learn Python!'},
    {'id':2, 'name':'Design with me'},
    {'id':3, 'name':'Frontend Developers'},
]

def home(request):
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)
'''

# Do not use login as function name because it is a built-in function that confilcts.
def loginPage(request):
    page = 'login'
    
    # If the user is already logged in, redirect to home page
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exists!')
        user = authenticate(request, username=username, password=password) 
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR Password is incorrect!')
    
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the user and commit=False means that it will not save to the database yet until we do some changes
            user = form.save(commit = False)
            # Clean the data
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error has occurred during registration!')
    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        # You can also search by username
        # Q(host__username__icontains=q)
        )
    
    topics = Topic.objects.all()
    # Count the number of rooms like len(rooms)
    room_count = rooms.count()
    # Recent Activity Feed. Get the messages that contain the search query
    # We also want to get ordered by the most recently updated that handled in the model
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages': room_messages,
    }
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    # Get all the messages in the room. Child class can be accessed by using the parent class name in lowercase + _set
    # room_messages = room.message_set.all().order_by('-created') # ordering handled in the model
    room_messages = room.message_set.all()
    # Get all the participants in the room
    participants = room.participants.all()
    
    # created a message and add it to the room
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        # Add the user to the participants list
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    
    context = {
        'room': room,
        'room_messages': room_messages, 
        'participants': participants,
            }
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    # Get all the rooms that the user is hosting
    rooms = user.room_set.all()
    # Get all the messages that the user has sent
    room_messages = user.message_set.all()
    # Get all the topics
    topics = Topic.objects.all()
    context = {
        'user': user,
        'rooms': rooms,
        'room_messages': room_messages,
        'topics': topics,
    }
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            # commit=False means that it will not save to the database yet until we do some changes
            room = form.save(commit=False)
            # Set the host to the current user of the room
            room.host = request.user
            room.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    # Only the host can update the room
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    # Only the host can delete the room
    if request.user != room.host:
        return HttpResponse('You are not allowed here!')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse('You are not allowed here!')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})

