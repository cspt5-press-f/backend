from django.contrib import admin
from .models import Room, Player, Item


# Register your models here.


@admin.register(Room, Player, Item)
class GameAdmin(admin.ModelAdmin):
    pass