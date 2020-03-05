from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json
import numpy as np

# instantiate pusher
# pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))



@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    request.user.player.coordinates = [0,0] # Set the starting coords at the beginning of the map
    request.user.player.save() # Save the update to the DB
    return JsonResponse({"message": f"Welcome {user.username}"})

  
@csrf_exempt
@api_view(["GET"])
def map(request):
    # Define map size
    map_size = 5
    # Get center coord (player coordinates)
    player_coords = request.user.player.coordinates 
    # Set bounding box for query
    x_max = player_coords[0] + map_size 
    x_min = player_coords[0] - map_size
    y_max = player_coords[1] + map_size
    y_min = player_coords[1] - map_size
    # Query for coordinates in database that are within bounding box
    map_rooms = Room.objects.filter(coordinates__0_1>[x_min]).filter(coordinates__0_1<[x_max])\
        .filter(coordinates__0_1>[y_min]).filter(coordinates__0_1<[y_max])

    # Drop coordinates and Shift to all positive
    x_coords = [room.coordinates[0] for room in map_rooms]
    x_min = np.amin(x_coords)
    if x_min < 0:
        x_coords = [x - x_min for x in x_coords]
    y_coords = [Room.coordinates[1] for room in map_rooms]
    y_min = np.amin(y_coords)
    if y_min < 0:
        y_coords = [y - y_min for y in y_coords]
    return JsonResponse({
        'player_coords': 'player_coords',
        'x_coords': x_coords,
        'y_coords': y_coords
    })
  
  
# @csrf_exempt
@api_view(["POST"])
def move(request):
    dirs={"n": "north", "s": "south", "e": "east", "w": "west"}
    data = json.loads(request.body)
    move_direction = data["direction"]
    player_coords = request.user.player.coordinates
    current_room = Room.objects.filter(coordinates=player_coords).first()
    # print(vars(request.user.player))  # DEBUG STATEMENT.  COMMENT OUT IN PROD.

    if move_direction == "n":
        player_coords[1] = player_coords[1] + 1
    elif move_direction == "e":
        player_coords[0] = player_coords[0] + 1
    elif move_direction == "s":
        player_coords[1] = player_coords[1] - 1        
    elif move_direction == "w":
        player_coords[0] = player_coords[0] - 1
        

    if Room.objects.filter(coordinates=player_coords).exists():
        new_room = Room.objects.filter(coordinates=player_coords).first()
        
        request.user.player.coordinates = player_coords
        request.user.player.save()
        return JsonResponse({"coord": new_room.coordinates, "title": new_room.name, "description": new_room.description, "items": new_room.items})
    else:
        
        return JsonResponse({"error": "Sorry, can't move in that direction.", "coord": current_room.coordinates, "title": current_room.name, "description": current_room.description, "items": current_room.items})


@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error':"Not yet implemented"}, safe=True, status=500)


@csrf_exempt
@api_view(["POST"])
def grab(request):
    data = json.loads(request.body)
    user = request.user
    player = user.player
    current_room = Room.objects.filter(coordinates=player.coordinates).first()
    item = Item.objects.filter(pk=int(data['item'])).first()

    # Remove item from player inventory
    del current_room.items[str(item.pk)]
    current_room.save()

    player.items.update({str(item.pk): item.name})
    player.save()

    return JsonResponse({"Picked Up": f"Item {item.name} from {current_room.name} to {user.username}"})


@csrf_exempt
@api_view(["POST"])
def drop(request):
    data = json.loads(request.body)
    user = request.user
    player = user.player
    current_room = Room.objects.filter(coordinates=player.coordinates).first()
    item = Item.objects.filter(pk=int(data['item'])).first()

    # Remove item from player inventory
    del player.items[str(item.pk)]
    player.save()

    # Place item into current room
    current_room.items.update({str(item.pk): item.name})
    current_room.save()

    return JsonResponse({"Dropped": f"Item {item.name} from {user.username} to {current_room.name}"})