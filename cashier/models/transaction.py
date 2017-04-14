""" Specifies the transaction model for the cashier app """
from __future__ import unicode_literals
from django.db import models


class Transaction(models.Model):
    """ Models a financial transaction """

    class Meta:
        """ Required by the sphix documentation tool """
        app_label = 'cashier'

    date = models.DateField('Date', null=False)
    amount = models.IntegerField('Amount', null=False)
    refunded = models.BooleanField('Refunded', default=False)
    description = models.CharField('Description', null=False, max_length=300)
    room = models.ForeignKey('Room')

    def __str__(self):
        return str(self.amount) + ": " + self.description

    def __iter__(self):
        """ returns the transaction as a dictionary """
        yield 'date', self.date
        yield 'room', self.room
        yield 'amount', self.amount
        yield 'description', self.description
