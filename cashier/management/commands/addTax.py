from django.core.management.base import BaseCommand, CommandError


from cashier.models import Transaction, Room

from datetime import date


class Command(BaseCommand):

    help = 'Adds the specified amount to all rooms'

    def add_arguments(self, parser):
        parser.add_argument('Amount', nargs='+', type=int)
        parser.add_argument('Description', nargs='+')


    def handle(self, *args, **options):
        print(options)
        rooms = Room.objects.all()
        for room in rooms:
            Appliedtax = Transaction(
                                    date=str(date.today()),
                                    amount=options['Amount'][0],
                                    description=options['Description'][0],
                                    room=room,
                                    refunded=True,
                        )
            Appliedtax.save()
