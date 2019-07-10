"""DormitoryDollars URL Configuration"""
from django.conf.urls import url
from cashier.views import room_overview, all_rooms_overview, add_dinner, add_drinks

urlpatterns = [
    url(r"^$", all_rooms_overview, name="AllRooms"),
    url(r"^room/(?P<room_nr>[0-9]+)$", room_overview, name="Room"),
    url(r"^addDinner/", add_dinner, name="AddDinner"),
    url(r"^addDrinks/", add_drinks, name="AddDrinks"),
]
