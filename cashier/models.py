from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Room(models.Model):
    roomNr = models.IntegerField(primary_key=True)
    name = models.CharField('Name', max_length=200)
    nickName = models.CharField('Nickname', max_length=200, blank=True)
    tlfNumber = models.IntegerField('Phone Number', blank=True, null=True)
    mail = models.EmailField('Email', blank=True, null=True)
    EmergencyName = models.CharField('Emergency Name', max_length=200, blank=True)
    EmergencyRel  = models.CharField('Emergency relationship type', max_length=200, blank=True)
    EmergencyTlfNumber = models.IntegerField('Emergency phone', blank=True, null=True)

    def getBalance(self):
        trans = Transaction.objects.filter(room=self)
        balance = 0
        for entry in trans:
            balance += entry.amount
        return balance

    def toDict(self):
        dicto = {}
        dicto['roomNr'] = self.roomNr
        dicto['name']   = self.name
        dicto['balance']   = self.getBalance()
        return dicto

    def getContactInfo(self):
        contactInfo = {}
        contactInfo['Name'] = self.name
        contactInfo['Phone'] = self.tlfNumber
        contactInfo['EmergencyContact'] = self.EmergencyRel \
                                          + " (" + self.EmergencyName + ")"
        contactInfo['EmergencyPhone'] = self.EmergencyTlfNumber
        return contactInfo

    def hasContactInfo(self):
        info = self.getContactInfo()
        for field in info:
            if info[field] == None:
                return False
        return True

    def getAllTransactions(self):
        transactions = []
        for trans in Transaction.objects.filter(room=self).order_by('-date'):
            transactions.append(trans.toDict())
        return transactions

    def __str__(self):
        if self.nickName != "":
            return "Room: " + str(self.roomNr) + ": " + self.nickName
        else:
            return "Room: " + str(self.roomNr) + ": " + self.name




class Transaction(models.Model):
    date   = models.DateField('Date', null=False)
    amount = models.IntegerField('Amount', null=False)
    description = models.CharField('Description', null=False, max_length=300)
    room = models.ForeignKey('Room', Room, null=False)
    refunded = models.BooleanField('Refunded', default=True)

    def __str__(self):
        return str(self.amount) + ": " + self.description


    def toDict(self):
        trans  = {}
        trans['date'] = self.date
        trans['amount'] = self.amount
        trans['description'] = self.description
        trans['room'] = self.room
        return trans
