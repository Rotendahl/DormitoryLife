""" Specifies which parts of the cashier models are visible in the admin UI """
from datetime import date
from django.contrib import admin
from cashier.models import Room, Transaction

admin.site.site_header = "Oestervold 1. sal money"
admin.site.index_title = "Benjamin er sej!"


class RoomAdmin(admin.ModelAdmin):
    """ Specifies how the room model should appear """
    list_filter = ('roomNr',)
    fieldsets = [
        ('Room number', {'fields':('name', 'roomNr', 'nickName')}),
        ('Contact Info', {'fields':('mail', 'tlfNumber')}),
        ('Konto:', {'fields':('accountNr', 'hasMobilePay')}),
        ('Emergency contacts', {
            'fields':('emergencyName', 'emergencyRel', 'emergencyTlfNumber'),
        }),
    ]
    list_display = ('roomNr', 'name')
    actions = ['add_tax']

    def add_tax(self, request, queryset):
        """ Adds a transaction of -40 to each room """
        month = str(date.today().strftime("%B"))
        for room in queryset:
            appliedtax = Transaction(
                date=str(date.today()), amount=-40,
                description='Køkkenskat for ' + month, room=room, refunded=True
            )
            appliedtax.save()
        msg = "Køkkenskat for " + month + " tilføjet til valgte værelser"
        self.message_user(request, msg)
    add_tax.short_description = 'Tilføj køkkenskat'

admin.site.register(Room, RoomAdmin)


class TransactionAdmin(admin.ModelAdmin):
    """ Specifies how the Transaction model should appear """
    list_filter = ('room__roomNr', 'refunded')
    fieldsets = [
        ('Transaction',
         {'fields': ('date', 'amount', 'description', 'room', 'refunded')}
        ),
    ]
    list_display = ('room', 'date', 'amount', 'description', 'refunded')
    actions = ['mark_refunded']

    def mark_refunded(self, request, queryset):
        """ Marks a series of transactions as refunded """
        trans_updated = queryset.update(refunded=True)
        msg = str(trans_updated) + " transaktioner market som refunderet"
        self.message_user(request, msg)
    mark_refunded.short_description = 'Mærk transaktioner som refunderet'

admin.site.register(Transaction, TransactionAdmin)
