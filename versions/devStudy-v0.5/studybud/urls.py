from django.contrib import admin
from django.urls import path, include

'''
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, Django!")

def room(request, room_name):
    return HttpResponse(f"Hello, {room_name}!"

urlpatterns = [
    path('', home),
    path('<str:room_name>/', room),
]
'''

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
]
