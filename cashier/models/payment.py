from __future__ import unicode_literals
from django.db import models

from cashier.models import Transaction
from django.utils.timezone import now
from datetime import date


class Payment(Transaction):
    refunded = models.BooleanField('Moved to Chashier account', default=False)
