from django.shortcuts import render
from cashier.models import Room
from django.shortcuts import render, get_object_or_404
# Create your views here.
def RoomOverview(request):
    rooms = Room.objects.all()
    data = []
    for room in rooms:
        data.append(room.toDict())
    rooms = data
    return render(request, "cashier/roomOverView.html", {'data': rooms})
