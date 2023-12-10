from django.shortcuts import render, redirect
from .models import Room, Message

# def rooms(request):
#     rooms = Room.objects.all()
#     context = {
#         'rooms': rooms
#     }
#     return render(request, 'pages/index.html', context)

def room(request, pk):
    room = Room.objects.get(pk=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
            message = Message.objects.create(
                user = request.user,
                room = room,
                body = request.POST.get('body')
            )
            room.participants.add(request.user)
            return redirect('room', pk=room.id)
    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants,
    }
    return render(request, 'rooms/room.html', context)