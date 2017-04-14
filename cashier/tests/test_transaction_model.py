""" Tests the models """
from django.test import TestCase
from cashier.models import Room, Transaction
from datetime import date

class TransactionTestCase(TestCase):
    """ Tests the room model """
    def setUp(self):
        Room.objects.create(
            roomNr=114,
            name="Benjamin Rotendahl",
            nickName="Benne",
            tlfNumber=12345678,
            mail="Benjamin@dormitorydollars.com",
            emergencyName="Simon Rotendahl",
            emergencyRel="Brother",
            emergencyTlfNumber=87654321
        )
        Room.objects.create(
            roomNr=113,
            name="Preben Mogensen",
        )
        Transaction.objects.create(
            date="2016-11-27",
            amount=-100,
            description="Beers",
            room=Room.objects.get(roomNr=114),
            refunded=True
        )
        Transaction.objects.create(
            date="2016-11-30",
            amount=150,
            description="Bank Transfer",
            room=Room.objects.get(roomNr=114),
            refunded=False
        )


    def test_dict_cast(self):
        """ Test the dict cast of the object """
        trans = dict(Transaction.objects.all().order_by('-date')[0])
        expected = {
            'date' : date(year=2016, month=11, day=30),
            'room' : Room.objects.get(roomNr=114),
            'amount' : 150,
            'description' : "Bank Transfer"
        }
        self.assertEqual(len(trans), len(expected))
        for key in trans:
            self.assertEqual(expected[key], trans[key])


    def test_str_cast(self):
        """ Test the string cast of the object """
        transP = Transaction.objects.all().order_by('-date')[0]
        transM = Transaction.objects.all().order_by('-date')[1]
        self.assertEqual("150.00: Bank Transfer", str(transP))
        self.assertEqual("-100.00: Beers", str(transM))
