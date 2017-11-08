"""
Specifies a dinnerclub model for the cashier app, a dinner club is when a person
makes dinner for the floor. They pay for the food and the kicthen reimburses
them and charges each room the total cost of dinner divided by the number of
participants.
"""
from __future__ import unicode_literals
from django.db import models

from cashier.models import Transaction

class Dinnerclub(models.Model):
    """ Dinnerclub """

    class Meta:
        """ Required by the sphix documentation tool """
        app_label = 'cashier'

    date = models.DateField('Date', null=False)
    totalAmount = models.DecimalField('Total Amount', max_digits=8,
                                      decimal_places=2)
    host = models.ForeignKey('Room')
    menu = models.CharField('Menu', null=False, max_length=300)


    def getparticipants(self):
        """ Returns all participants for the dinnerclub """
        return Transaction.objects.filter(dinnerclub=self)


    def __str__(self):
        return str(self.date) + " -- Host " + str(self.host)


    def __iter__(self):
        """ returns the dinnerclub as a dictionary """
        participants = self.getparticipants()
        yield 'date', self.date
        yield 'host', self.room
        yield 'TotalAmount', self.totalAmount
        yield 'participants', participants
        yield 'nrParticipants', len(participants)
        yield 'PricePerPerson', self.totalAmount / len(participants)
        yield 'Menu', self.description
