""" Tests the admin actions """
from django.test import TestCase
from django.http import HttpRequest
from cashier.models import Room, Transaction, Payment
from cashier.admin import RoomAdmin, TransactionAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.options import ModelAdmin
from . import sharedSetup

class MockRequest(HttpRequest):
    """ Mock object to test the admin models """
    pass



class AdminTestCase(TestCase):
    """ Tests the room model """
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
    #sharedSetup(self)
    self.site = AdminSite()



    def test_add_balance(self):
        """Tests that add_tax adds -40 to each room with todays date """
        request = MockRequest()
        admin = RoomAdmin(Room, self.site)
        admin.add_tax(request, Room.objects.all())
        room114 = Room.objects.get(roomNr=114)
        self.assertEqual(10, room114.get_balance())
        room113 = Room.objects.get(roomNr=113)
        self.assertEqual(-40, room113.get_balance())



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
