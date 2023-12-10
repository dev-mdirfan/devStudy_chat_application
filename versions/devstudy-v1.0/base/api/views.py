
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RoomSerializer
from base.models import Room

'''
from django.http import JsonResponse
def getRoutes(request):
    routes = [
        'GET /api',
        # API for jason array that contains all the rooms
        'GET /api/rooms/',
        'GET /api/rooms/:id',
    ]
    return JsonResponse(routes, safe=False)
'''


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms/',
        'GET /api/rooms/:id',
    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    # Object can not be directory covert into json, we need to use serializer
    serializer = RoomSerializer(rooms, many=True)   # many=True means we have multiple rooms
    # Serializer converts the python object into json
    return Response(serializer.data)


@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)
