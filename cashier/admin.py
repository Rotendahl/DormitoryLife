""" Specifies which parts of the cashier models are visible in the admin UI """
from datetime import date
from django.contrib import admin
from cashier.models import Room, Transaction, Dinnerclub, Payment

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
                date=str(date.today()), amount=40, typeOfTransaction='debt',
                description='Køkkenskat for ' + month, room=room,
            )
            appliedtax.save()
        msg = "Køkkenskat for " + month + " tilføjet til valgte værelser"
        self.message_user(request, msg)
    add_tax.short_description = 'Tilføj køkkenskat'

admin.site.register(Room, RoomAdmin)


class TransactionAdmin(admin.ModelAdmin):
    """ Specifies how the Transaction model should appear """
    list_filter = ('room__roomNr','typeOfTransaction')
    fieldsets = [
        ('Transaction',
         {'fields': ('date', 'typeOfTransaction', 'amount', 'description', 'room', 'archived')}
        ),
    ]
    list_display = ('room', 'date','typeOfTransaction', 'amount', 'description')
    actions = ['mark_as_payment','mark_as_debt', 'mark_as_expense', 'mark_as_archived']

    def mark_as_payment(self, request, queryset):
        trans_updated = queryset.update(typeOfTransaction='pay')
        msg = str(trans_updated) + " transactions marked as payment"
        self.message_user(request, msg)
    mark_as_payment.short_description = 'Mark as payment'

    def mark_as_debt(self, request, queryset):
        trans_updated = queryset.update(typeOfTransaction='debt')
        msg = str(trans_updated) + " transactions marked as debt"
        self.message_user(request, msg)
    mark_as_debt.short_description = 'Mark as debt'

    def mark_as_expense(self, request, queryset):
        trans_updated = queryset.update(typeOfTransaction='expense')
        msg = str(trans_updated) + " transactions marked as expense"
        self.message_user(request, msg)
    mark_as_expense.short_description = 'Mark as expense'

    def mark_as_archived(self, request, queryset):
        trans_updated = queryset.update(archived=True)
        msg = str(trans_updated) + " marked as Archived"
        self.message_user(request, msg)
    mark_as_expense.short_description = 'Archive'

admin.site.register(Transaction, TransactionAdmin)


class PaymentAdmin(admin.ModelAdmin):
    list_filter = ('room__roomNr','refunded')
    fieldsets = [
        ('Payment',
         {'fields': (
                     'refunded', 'date', 'typeOfTransaction', 'amount',
                     'description','room'
                    ),
        }
        ),
    ]
    list_display = ('room', 'date','typeOfTransaction', 'amount', 'description')
    actions = ['mark_refunded']

    def mark_refunded(self, request, queryset):
        """ Marks a series of transactions as refunded """
        trans_updated = queryset.update(refunded=True)
        msg = str(trans_updated) + " transaktioner market som refunderet"
        self.message_user(request, msg)
    mark_refunded.short_description = 'Mærk transaktioner som refunderet'

admin.site.register(Payment, PaymentAdmin)


class TransactionInLine(admin.TabularInline):
    """ Used in the dinnerclub admin to easily add participants """
    model = Transaction
    extra = 0

class DinnerAdmin(admin.ModelAdmin):
    """ Specifies how the dinnerclub model should appear """
    list_filter = ('host', 'date',)
    fieldsets = [
        ('Dinnerclub',
         {'fields': ('date', 'host', 'totalAmount', 'menu')}
        ),
    ]
    list_display = ('date', 'host', 'totalAmount', 'menu')
    inlines = [TransactionInLine,]
admin.site.register(Dinnerclub, DinnerAdmin)
