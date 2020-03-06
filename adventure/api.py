from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json
import numpy as np
import copy

# instantiate pusher
# pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))



@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    request.user.player.coordinates = [0,0] # Set the starting coords at the beginning of the map
    request.user.player.save() # Save the update to the DB
    return JsonResponse(
        {
            "message": f"Welcome {user.username}",
            "map": player.map,
            }
            )
  
# @csrf_exempt
@api_view(["POST"])
def move(request):
    data = json.loads(request.body)
    move_direction = data["direction"]
    player_coords = copy.copy(request.user.player.coordinates)
    current_room = Room.objects.filter(x=player_coords[0], y=player_coords[1]).first()
    print(f'DEBUG: current_room {current_room}, coords {current_room.coordinates}')
    # print(vars(request.user.player))  # DEBUG STATEMENT.  COMMENT OUT IN PROD.

    if move_direction == "n":
        player_coords[1] = player_coords[1] + 1
    elif move_direction == "e":
        player_coords[0] = player_coords[0] + 1
    elif move_direction == "s":
        player_coords[1] = player_coords[1] - 1        
    elif move_direction == "w":
        player_coords[0] = player_coords[0] - 1
        
    # print(f'DEBUG: player_map: {request.user.player.map}')
    print(f'DEBUG: player_coord: {request.user.player.coordinates}')

    if Room.objects.filter(x=player_coords[0], y=player_coords[1]).exists():
        new_room = Room.objects.filter(x=player_coords[0], y=player_coords[1]).first()
        request.user.player.coordinates = player_coords
        request.user.player.save()
        return JsonResponse(
            {"coord": new_room.coordinates, 
            "title": new_room.name, 
            "description": new_room.description, 
            "items": new_room.items, 
            "map": request.user.player.map,
            }
            )
    else:
        
        return JsonResponse(
            {
                "error": "Sorry, can't move in that direction.", 
                "coord": current_room.coordinates, 
                "title": current_room.name, 
                "description": current_room.description, 
                "items": current_room.items,
                "map": request.user.player.map,
                }
            )


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
    player_coords = player.coordinates
    current_room = Room.objects.filter(x=player_coords[0], y=player_coords[1]).first()
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
    player_coords = player.coordinates
    current_room = Room.objects.filter(x=player_coords[0], y=player_coords[1]).first()
    item = Item.objects.filter(pk=int(data['item'])).first()

    # Remove item from player inventory
    del player.items[str(item.pk)]
    player.save()

    # Place item into current room
    current_room.items.update({str(item.pk): item.name})
    current_room.save()

    return JsonResponse({"Dropped": f"Item {item.name} from {user.username} to {current_room.name}"})