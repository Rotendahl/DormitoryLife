from django.test import TestCase
from django.http import HttpRequest
from cashier.models import Room, Transaction, Payment
from cashier.admin import RoomAdmin, TransactionAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.options import ModelAdmin


def sharedSetup(testSite):
    pass
    Room.objects.create(
        roomNr=114,
        name="Benjamin Rotendahl",
        nickName="Benne",
        tlfNumber=12345678,
        mail="Benjamin@dormitorydollars.com",
        emergencyName="Simon Rotendahl",
        emergencyRel="Brother",
        emergencyTlfNumber="87654321"
    )
    Room.objects.create(
        roomNr=113,
        name="Preben Mogensen",
    )
    Transaction.objects.create(
        date="2016-11-27",
        amount=100,
        description="Beers",
        room=Room.objects.get(roomNr=114),
        typeOfTransaction = 'debt'
    )
    Payment.objects.create(
        date="2016-11-30",
        amount=150,
        description="Bank Transfer",
        room=Room.objects.get(roomNr=114),
        typeOfTransaction='pay',
        refunded=False
    )
    Transaction.objects.create(
        date="2016-11-30",
        amount=150,
        description="Bank Transfer",
        room=Room.objects.get(roomNr=114),
        typeOfTransaction='expense'
    )
