""" Specifies the room model for the cashier app """
from __future__ import unicode_literals
from django.db import models

from cashier.models import Transaction


class Room(models.Model):
    """ Models a room in a dormitory.

    It is only required the it has a roomNr and a name. It can have nickname,
    contact info and an emergency contact.
    """
    class Meta:
        """ Required by the sphix documentation tool """
        app_label = 'cashier'

    roomNr = models.IntegerField(primary_key=True)
    name = models.CharField('Name', max_length=200)
    nickName = models.CharField('Nickname', max_length=200, blank=True)
    tlfNumber = models.IntegerField('Phone Number', blank=True, null=True)
    accountNr = models.CharField('Konto-nr', blank=True, max_length=20)
    hasMobilePay = models.BooleanField('MobilePay', default=False)
    mail = models.EmailField('Email', blank=True, null=True)
    emergencyName = models.CharField(
        'Emergency Name', max_length=200, blank=True
    )
    emergencyRel = models.CharField(
        'Emergency relationship type', max_length=200, blank=True
    )
    emergencyTlfNumber = models.CharField(
        'Emergency phone',max_length=50, blank=True, null=True
    )


    def __str__(self):
        """ Returns a string representing the room """
        if self.nickName != "":
            return "Room " + str(self.roomNr) + ": " + self.nickName
        else:
            return "Room " + str(self.roomNr) + ": " + self.name


    def __iter__(self):
        """ Returns the required room parameters as a dictionary """
        yield 'balance', self.get_balance()
        yield 'roomNr', self.roomNr
        yield 'name', self.name


    def get_balance(self):
        """ Returns the sum of all transactions tied to the room """
        trans = Transaction.objects.filter(room=self)
        balance = 0
        for entry in trans:
            balance += entry.amount
        return balance


    def has_contact_info(self):
        """ checks if any contact fields are blank """
        return len(self.get_contact_info()) == 4


    def get_all_transactions(self):
        """ Returns all transactions associated with the room as a list """
        transactions = Transaction.objects.filter(room=self).order_by('-date')
        return list(map(dict, transactions))


    def get_contact_info(self):
        """ Returns the contact information for the room """
        contact_info = {}
        contact_info['Name'] = self.name
        secondary_info = [
            self.tlfNumber,
            self.emergencyTlfNumber,
            self.emergencyRel,
            self.emergencyName
        ]
        if not(None or ""  in secondary_info):
            contact_info['Phone'] = self.tlfNumber
            contact_info['EmergencyPhone'] = self.emergencyTlfNumber
            contact_info['EmergencyContact'] = self.emergencyRel \
                                              + " (" + self.emergencyName + ")"
        return contact_info
