""" Specifies the transaction model for the cashier app """
from __future__ import unicode_literals
from django.db import models


class Transaction(models.Model):
    """ Models a financial transaction that isn't a payment """

    class Meta:
        """ Required by the sphix documentation tool """
        app_label = 'cashier'

    date = models.DateField('Date', null=False)
    amount = models.DecimalField('amount', max_digits=8, decimal_places=2)
    description = models.CharField('Description', null=False, max_length=300)
    archived = models.BooleanField('Arkiveret', default=False)
    types = (('debt', 'Debt'), ('expense', 'Expense'), ('pay', 'Payment') )
    room = models.ForeignKey('Room', on_delete=models.PROTECT)
    typeOfTransaction = models.CharField('Type', max_length=7, choices=types,
    default='debt')

    dinnerclub = models.ForeignKey('dinnerclub', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.amount) + ": " + self.description

    def __iter__(self):
        """ returns the transaction as a dictionary """
        yield 'date', self.date
        yield 'room', self.room
        yield 'amount', self.amount
        yield 'type', self.typeOfTransaction
        yield 'description', self.description
        yield 'archived', self.archived
