# """ Tests the models """
# from datetime import date
# from django.test import TestCase
# from cashier.models import Room, Transaction
# from . import sharedSetup
#
# class TransactionTestCase(TestCase):
#     """ Tests the room model """
#     def setUp(self):
#         sharedSetup(self)
#
#     def test_dict_cast(self):
#         """ Test the dict cast of the object """
#         trans = dict(Transaction.objects.all().order_by('-date')[0])
#         expected = {
#             'date' : date(year=2016, month=11, day=30),
#             'room' : Room.objects.get(roomNr=114),
#             'amount' : 150,
#             'description' : "Bank Transfer"
#         }
#         self.assertEqual(len(trans), len(expected))
#         for key in trans:
#             self.assertEqual(expected[key], trans[key])
#
#
#     def test_str_cast(self):
#         """ Test the string cast of the object """
#         trans_p = Transaction.objects.all().order_by('-date')[0]
#         trans_m = Transaction.objects.all().order_by('-date')[1]
#         self.assertEqual("150.00: Bank Transfer", str(trans_p))
#         self.assertEqual("-100.00: Beers", str(trans_m))
