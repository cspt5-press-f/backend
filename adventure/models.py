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
    _map = []

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

    # Getter Methods
    @property
    def map(self):
        return get_map_coord(center_coord=self.coordinates, size=5)

    # Setter Methods
    @map.setter
    def map(self):
        self._map = get_map_coord(center_coord=self.coordinates, size=5)


    

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



########################
### Helper Functions ###
########################

def get_map_coord(center_coord, size):
    if size % 2 > 0:
        dist = int((size - 1) / 2)
    else:
        dist = int(size / 2)
    # Set boundaries
    min_x = center_coord[0] - dist
    max_x = center_coord[0] + dist
    min_y = center_coord[1] - dist
    max_y = center_coord[1] + dist

    # Query for rooms within boundary
    rooms = Room.objects.filter(
        x__gte = min_x, 
        x__lte = max_x,
        y__gte = min_y,
        y__lte = max_y)
    # Get coordinates for all rooms
    map_coords = [room.coordinates for room in rooms]
    # print('DEBUG TF MAP:', draw_tf_map(center_coord = center_coord, available_coord=map_coords,size=size))
    return draw_tf_map(center_coord = center_coord, available_coord=map_coords,size=size)

def draw_tf_map(center_coord, available_coord, size):
    if size % 2 > 0:
        dist = int((size - 1) / 2)
    else:
        dist = int(size / 2)

    def build_grid(center_coord: int, available_coord: list, dist: int):
        grid = []
        def in_available(test_coord, available_coord):
            return (test_coord in available_coord)

        for y in range(center_coord[1] - dist - 1, center_coord[1] + dist):
            temp_row = []
            for x in range(center_coord[0] - dist, center_coord[0] + dist + 1):
                temp_row.append(
                    in_available([x, y], available_coord))
            grid.append(temp_row)
        return grid
                
    return build_grid(
        center_coord=center_coord, 
        available_coord=available_coord, 
        dist=dist)