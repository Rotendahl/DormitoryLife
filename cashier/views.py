from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from cashier.models import Room
from django.shortcuts import render, get_object_or_404
# Create your views here.
def AllRoomsOverview(request):
    rooms = Room.objects.all().order_by('roomNr')
    data = []
    for room in rooms:
        data.append(room.toDict())
    rooms = data
    return render(request, "cashier/AllRoomsOverView.html", {'data': rooms})


def RoomOverview(request, roomNr):
    room = Room.objects.filter(roomNr=roomNr)[0]
    trans = room.getAllTransactions()
    data = {'contactInfo' : room.getContactInfo(), 'transactions' : trans}
    data['hasContactInfo'] = room.hasContactInfo()
    data['balance'] = room.getBalance()
    return render(request, "cashier/RoomOverView.html", {'data': data})
