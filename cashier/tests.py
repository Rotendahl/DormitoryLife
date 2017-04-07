""" Tests the models """
from django.test import TestCase
from cashier.models import Room, Transaction

class RoomTestCase(TestCase):
    """ Tests the room model """
    def setUp(self):
        Room.objects.create(
            roomNr=114,
            name="Benjamin Rotendahl",
            nickName="Benne",
            tlfNumber=29866771,
            mail="Benjamin@Rotendahl.dk",
            EmergencyName="Simon Rotendahl",
            EmergencyRel="Brother",
            EmergencyTlfNumber=27586771
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

    def test_get_balance(self):
        """Tests that the getBalance method works as expected"""
        room = Room.objects.get(roomNr=114)
        self.assertEqual(50, room.getBalance())
