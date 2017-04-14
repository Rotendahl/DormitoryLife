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


    def test_get_balance(self):
        """Tests that the getBalance method works as expected"""
        room = Room.objects.get(roomNr=114)
        self.assertEqual(50, room.get_balance())


    def test_dict_cast(self):
        """ Tests that the required fields for the room is obtained by dict """
        room114 = dict(Room.objects.get(roomNr=114))
        room113 = dict(Room.objects.get(roomNr=113))
        self.assertEqual(3, len(room114))
        self.assertEqual(3, len(room113))
        self.assertEqual(114, room114['roomNr'])
        self.assertEqual(113, room113['roomNr'])
        self.assertEqual(50, room114['balance'])
        self.assertEqual(0, room113['balance'])
        self.assertEqual("Benjamin Rotendahl", room114['name'])
        self.assertEqual("Preben Mogensen", room113['name'])


    def test_get_contact_info(self):
        """Tests that the contact info is returned if it exists """
        room114 = Room.objects.get(roomNr=114)
        room113 = Room.objects.get(roomNr=113)
        expected = {
            'Name' : 'Benjamin Rotendahl',
            'Phone' : 12345678,
            'EmergencyPhone' : 87654321,
            'EmergencyContact' : 'Brother (Simon Rotendahl)'
        }
        self.assertTrue(room114.has_contact_info())
        self.assertEqual(expected, room114.get_contact_info())
        expected = {'Name' : 'Preben Mogensen'}
        self.assertFalse(room113.has_contact_info())
        self.assertEqual(expected, room113.get_contact_info())

    def test_get_transactions(self):
        """Tests that we get excatly all transactions that fit the room """
        room114 = Room.objects.get(roomNr=114)
        room113 = Room.objects.get(roomNr=113)
