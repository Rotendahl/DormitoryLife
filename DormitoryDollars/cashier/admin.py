from django.contrib import admin
from DormitoryDollars.cashier.models import Room, Transaction

# Register your models here.
admin.site.site_header="Østervold 1. sal money"
admin.site.index_title="Benjamin er sej!"


class RoomAdmin(admin.ModelAdmin):
    list_filter = ('roomNr',)
    fieldsets = [
        ('Room number', {'fields':('name', 'roomNr', 'nickName')}),
        ('Contact Info', {'fields':('mail', 'tlfNumber')}),
        ('Emergency contacts', {
            'fields':('EmergencyName', 'EmergencyRel', 'EmergencyTlfNumber'),
        }),
    ]
    list_display = ('roomNr', 'name')
admin.site.register(Room, RoomAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_filter = ('room__roomNr',)
    fieldsets = [
        ('Transaction', {'fields':('date', 'amount', 'description', 'room')}),

    ]
    list_display = ('room', 'date', 'amount', 'description')
admin.site.register(Transaction, TransactionAdmin)
