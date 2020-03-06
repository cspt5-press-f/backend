from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid



""" Player Class """

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coordinates = ArrayField(
                base_field=models.IntegerField(),
                size=2,
                default=list
            )
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    items = JSONField(
                    default=dict
    )
    def initialize(self):
        if self.coordinates == 0:
            self.coordinates = Room.objects.first().id
            self.save()
    def room(self):
        try:
            return Room.objects.get(coordinates=self.coordinates)
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
    items = JSONField(
                    default=dict
    )
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    _coordinates = [0,0]

    def __repr__(self):
        return self.name
    # Getter Methods
    @property
    def coordinates(self):
        if self.x is not None and self.y is not None:
            return [self.x, self.y]
        else:
            return self._coordinates
    # Setter Methods
    @coordinates.setter
    def coordinates(self):
        if self.x is not None and self.y is not None:
            self._coordinates = [self.x, self.y]




""" Generic Item Class """

class Item(models.Model):
    name = models.CharField(max_length=100, default='DEFAULT NAME')
    description = models.CharField(max_length=500, default='DEFAULT DESCRIPTION')
    value = models.IntegerField(default=0)

    def __repr__(self):
        return self.name