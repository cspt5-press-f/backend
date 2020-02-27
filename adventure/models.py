from django.contrib.postgres.fields import JSONField
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid




class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    def initialize(self):
        if self.currentRoom == 0:
            self.currentRoom = Room.objects.first().id
            self.save()
    def room(self):
        try:
            return Room.objects.get(id=self.currentRoom)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()

@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()


""" Room Class """

class Room(models.Model):
    name = models.CharField(max_length=100, default='DEFAULT NAME')
    description = models.CharField(max_length=500, default='DEFAULT DESCRIPTION')
    connections = JSONField()
    items = JSONField()

    def connect(self, room_id, direction):
        connections = self.connections
        connections[direction] = room_id
        self.connections = connections
        self.save()

    def __repr__(self):
        return self.name
    
    # # Features: Get players in room
    # def playerNames(self, currentPlayerID):
    #     return [p.user.username for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]
    # def playerUUIDs(self, currentPlayerID):
    #     return [p.uuid for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]


""" Generic Item Class """

class Item():
    def __init__(self, id, name, description=None):
        self.id = id
        self.name = name
        self.description = description

class ItemHandler():
    def __init__(self):
        pass
    
    def move_item(self, object_1, object_2, item: Item):
        """Move item from object_1 to object_2"""
        del object_1.items[item.id]
        object_2.items.update({item.id: item})

    def place_item(self, item, receiver):
        receiver.items.update({item.id: item})


# Write a class to hold player information, e.g. what room they are in
# currently.

class Player():
    def __init__(self, current_room=None):
        self.current_room = current_room
        self.items = {}

    def look(self):
        print(self.current_room.name)
        print(self.current_room.description, "\n")
        print('In The Room: ', self.scan_items(self.current_room.items))
        print('Inventory: ', self.scan_items())

    def scan_items(self, inventory=None):
        scan_list = []
        if inventory is None:
            inventory = self.items
            
        for key in inventory.keys():
            scan_list.append(inventory[key].name)
        return scan_list

    def move(self, direction):
        if direction in self.current_room.connections.keys():
            self.current_room = self.current_room.connections[direction]
        else:
            print('Cannot go that way!')
