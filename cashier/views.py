""" Views for the cashier app """
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from cashier.models import Room, Dinnerclub, Transaction

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
        print(trans[i]['type'])
        if trans[i]['type'] == 'expense':
            total += trans[i]['amount']
        else:
            total -= trans[i]['amount']
        trans[i]['total'] = total
    return render(request, "cashier/RoomOverView.html", {'data': data})


@login_required
def add_dinner(request):
    """ Page to add dinnerclub """
    if request.method == 'POST':
        return handleDinnerClub(request)

    rooms = Room.objects.all()
    data = {'roomNrs': []}
    for room in rooms:
        data['roomNrs'].append(room.roomNr)
    return render(request, "cashier/AddDinner.html", {'data': data})


def handleDinnerClub(request):
    """Takes a dinnerclub request and returns the probper template"""
    participants = request.POST.getlist('participants')
    print(participants)
    fields = request.POST
    if len(participants) < 2:
        msg = {'status': "No participants added", 'error': True}
        return render(request, "cashier/dinnerStatus.html", {'data' : msg})

    for field in fields:
        if fields[field] == '':
            msg = {'status': "Field: " + field + " was empty", 'error': True}
            return render(request, "cashier/dinnerStatus.html", {'data' : msg})

    din_club = Dinnerclub(
        date='-'.join(fields['Date'].split('-')[::-1]), # Fuck date formats
        totalAmount=fields['Price'],
        host=Room.objects.get(pk=fields['Host']),
        menu=fields['Menu'],
        )
    din_club.save()
    nr_participants = len(participants)
    price_per_room = (int(din_club.totalAmount) / float(nr_participants)) * -1
    for room in participants:
        trans = Transaction(
            date=din_club.date,
            amount=price_per_room,
            refunded=True,
            dateOfRefund=din_club.date,
            description="Dinnerclub: " + str(din_club),
            room=Room.objects.get(pk=room),
            dinnerclub=din_club
        )
        trans.save()
    #Host
    trans = Transaction(
        date=din_club.date,
        amount=din_club.totalAmount,
        refunded=True,
        dateOfRefund=din_club.date,
        description="Host Dinnerclub: " + str(din_club),
        room=din_club.host,
        dinnerclub=din_club
    )
    trans.save()

    msg = {'status': str(din_club), 'error': False}
    return render(request, "cashier/dinnerStatus.html", {'data' : msg})
