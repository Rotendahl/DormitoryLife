""" Views for the cashier app """
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from cashier.models import Room, Dinnerclub, Transaction


@login_required
def all_rooms_overview(request):
    """ The view that shows the balance for all rooms """
    rooms = Room.objects.all().order_by("roomNr")
    rooms = map(dict, rooms)
    return render(request, "cashier/AllRoomsOverView.html", {"data": rooms})


@login_required
def room_overview(request, room_nr):
    """ View that shows all transactions for a room """
    room = Room.objects.filter(roomNr=room_nr)[0]
    trans = room.get_all_transactions()
    data = {"contactInfo": room.get_contact_info(), "transactions": trans}
    data["hasContactInfo"] = room.has_contact_info()
    data["balance"] = room.get_balance()
    rng = range(0, len(trans))[::-1]
    total = 0
    for i in rng:
        if trans[i]["type"] == "expense" or trans[i]["type"] == "pay":
            total += trans[i]["amount"]
        else:
            total -= trans[i]["amount"]
        trans[i]["total"] = total
    return render(request, "cashier/RoomOverView.html", {"data": data})


@login_required
def add_dinner(request):
    """ Page to add dinnerclub """
    if request.method == "POST":
        return handleDinnerClub(request)

    rooms = Room.objects.all().order_by("roomNr")
    data = {"roomNrs": [], "rooms": []}
    for room in rooms:
        data["roomNrs"].append(str(room.roomNr))
        data["rooms"].append(str(room))
    return render(request, "cashier/AddDinner.html", {"data": data})


def handleDinnerClub(request):
    """Takes a dinnerclub request and returns the probper template"""
    participants = request.POST.getlist("participants")
    fields = request.POST
    if len(participants) < 2:
        msg = {"status": "No participants added", "error": True}
        return render(request, "cashier/dinnerStatus.html", {"data": msg})

    for field in fields:
        if fields[field] == "":
            msg = {"status": "Field: " + field + " was empty", "error": True}
            return render(request, "cashier/dinnerStatus.html", {"data": msg})

    hostRoom = fields["Host"].split(":")[0].split(" ")[1]
    din_club = Dinnerclub(
        date="-".join(fields["Date"].split("/")[::-1]),  # Fuck date formats
        totalAmount=fields["Price"],
        host=Room.objects.get(pk=hostRoom),
        menu=fields["Menu"],
    )
    din_club.save()
    nr_participants = len(participants)
    price_per_room = int(din_club.totalAmount) / float(nr_participants)
    for room in participants:
        trans = Transaction(
            date=din_club.date,
            amount=price_per_room,
            description="Dinnerclub: " + str(din_club),
            room=Room.objects.get(pk=room),
            typeOfTransaction="debt",
            dinnerclub=din_club,
        )
        trans.save()
    # Host
    trans = Transaction(
        date=din_club.date,
        amount=din_club.totalAmount,
        typeOfTransaction="expense",
        description="Host Dinnerclub: " + str(din_club),
        room=din_club.host,
        dinnerclub=din_club,
    )
    trans.save()

    msg = {"status": str(din_club), "error": False}
    return render(request, "cashier/dinnerStatus.html", {"data": msg})
