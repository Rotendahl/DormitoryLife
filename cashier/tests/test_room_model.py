""" Tests the models """
from django.test import TestCase
from cashier.models import Room, Transaction
from . import sharedSetup


class RoomTestCase(TestCase):
    """ Tests the room model """
    def setUp(self):
        sharedSetup(self)

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
            'EmergencyPhone' : "87654321",
            'EmergencyContact' : 'Brother (Simon Rotendahl)'
        }
        self.assertTrue(room114.has_contact_info())
        self.assertEqual(expected, room114.get_contact_info())
        expected = {'Name' : 'Preben Mogensen'}
        self.assertFalse(room113.has_contact_info())
        self.assertEqual(expected, room113.get_contact_info())

    def test_get_transactions(self):
        """Tests that we get excatly all transactions that fit the room """
        room114 = Room.objects.get(roomNr=114).get_all_transactions()
        room113 = Room.objects.get(roomNr=113).get_all_transactions()

        msg = "Gave a transaction that didn't belong to room"
        self.assertEqual(0, len(room113), msg)

        msg = "Gave a wrong number of transactions"
        self.assertEqual(2, len(room114), msg)

        trans114 = Transaction.objects.filter(room=Room.objects.get(roomNr=114))
        trans114 = list(map(dict, trans114))
        msg = "Gave a transaction for a wrong room"
        for trans in room114:
            self.assertTrue(trans in trans114, msg)

    def test_str_cast(self):
        """ Test the string cast of the object """
        room114 = str(Room.objects.get(roomNr=114))
        room113 = str(Room.objects.get(roomNr=113))
        self.assertEqual('Room 114: Benne', str(room114))
        self.assertEqual('Room 113: Preben Mogensen', str(room113))
