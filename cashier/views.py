""" Views for the cashier app """
from django.shortcuts import render
from cashier.models import Room



def all_rooms_overview(request):
    """ The view that shows the balance for all rooms """
    rooms = Room.objects.all().order_by('roomNr')
    rooms = map(dict, rooms)
    return render(request, "cashier/AllRoomsOverView.html", {'data': rooms})


def room_overview(request, room_nr):
    """ View that shows all transactions for a room """
    room = Room.objects.filter(roomNr=room_nr)[0]
    trans = room.get_all_transactions()
    data = {'contactInfo' : room.get_contact_info(), 'transactions' : trans}
    data['hasContactInfo'] = room.has_contact_info()
    data['balance'] = room.get_balance()
    rng = range(0, len(trans))[::-1]
    total = 0
    for i in rng:
        total += trans[i]['amount']
        trans[i]['total'] = total
    return render(request, "cashier/RoomOverView.html", {'data': data})
