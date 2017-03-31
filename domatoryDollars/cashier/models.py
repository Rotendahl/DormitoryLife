from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Room(models.Model):
    roomNr = models.IntegerField(null=False, primary_key=True)
    name = models.CharField('Name', max_length=200)
    nickName = models.CharField('Nickname', max_length=200, default="")
    tlfNumber = models.IntegerField('Phone Number', null=False)
    mail = models.EmailField(null=False)
    EmergencyName = models.CharField('Emergency Name', max_length=200)
    EmergencyRel  = models.CharField('Emergency relationship type', max_length=200)
    EmergencyTlfNumber = models.IntegerField('Emergency phone', null=False)



    def __str__(self):
        if self.nickName != "":
            return "Room: " + str(self.roomNr) + ": " + self.nickName
        else:
            return "Room: " + str(self.roomNr) + ": " + self.name
