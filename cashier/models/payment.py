class Payment(Transaction):
    """ Hello """
    room = models.ForeignKey('Room')
    refunded = models.BooleanField('Moved to Chashier account', default=False)
    dateOfRefund = models.DateField('Date of transfer', null=True, blank=True)
