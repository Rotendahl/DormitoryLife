"""Command line utility to add a specified amount to each room"""
from datetime import date
from django.core.management.base import BaseCommand
from cashier.models import Transaction, Room



class Command(BaseCommand):
    """ Extending the basecommand """
    help = 'Adds the specified amount to all rooms'

    def add_arguments(self, parser):
        parser.add_argument('Amount', nargs='+', type=int)
        parser.add_argument('Description', nargs='+')


    def handle(self, *args, **options):
        rooms = Room.objects.all()
        for room in rooms:
            refund = True if options['Amount'][0] > 0 else False
            appliedtax = Transaction(
                date=str(date.today()), amount=options['Amount'][0],
                description=options['Description'][0], room=room, refunded=refund
            )
            appliedtax.save()
