""" Specifies the models for the cashier app """
from __future__ import unicode_literals
from django.db import models



class Room(models.Model):
    """ Models a room in a dormitory """
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
    emergencyTlfNumber = models.IntegerField(
        'Emergency phone', blank=True, null=True
    )

    def get_balance(self):
        """ Returns the sum of all transactions tied to the room """
        trans = Transaction.objects.filter(room=self)
        balance = 0
        for entry in trans:
            balance += entry.amount
        return balance

    def __iter__(self):
        """ returns the required room parameters as a dictionary """
        yield 'balance', self.get_balance()
        yield 'roomNr', self.roomNr
        yield 'name', self.name

    def get_contact_info(self):
        """ returns the contact information for the room """
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

    def has_contact_info(self):
        """ checks if any contact fields are blank """
        return len(self.get_contact_info()) == 4


    def get_all_transactions(self):
        """ Returns all transactions associated with the room """
        transactions = []
        for trans in Transaction.objects.filter(room=self).order_by('-date'):
            transactions.append(trans.to_dict())
        return transactions

    def __str__(self):
        if self.nickName != "":
            return "Room: " + str(self.roomNr) + ": " + self.nickName
        else:
            return "Room: " + str(self.roomNr) + ": " + self.name



class Transaction(models.Model):
    """ Models a financial transaction """
    date = models.DateField('Date', null=False)
    room = models.ForeignKey('Room', Room, null=False)
    amount = models.IntegerField('Amount', null=False)
    refunded = models.BooleanField('Refunded', default=False)
    description = models.CharField('Description', null=False, max_length=300)

    def __str__(self):
        return str(self.amount) + ": " + self.description


    def to_dict(self):
        """ returns the transactions as a dictionary """
        trans = {}
        trans['date'] = self.date
        trans['room'] = self.room
        trans['amount'] = self.amount
        trans['description'] = self.description
        return trans
