from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse, HttpResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json

# instantiate pusher
# pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))

from adventure.models import Room
import numpy as np

@csrf_exempt
@api_view(["GET"])
def map(request):
    generated_rooms = Room.objects.all()
    x_coords = [room.coordinates[0] for room in generated_rooms]
    x_min = np.amin(x_coords)
    if x_min < 0:
        x_coords = [x - x_min for x in x_coords]
    y_coords = [room.coordinates[1] for room in generated_rooms]
    y_min = np.amin(y_coords)
    if y_min < 0:
        y_coords = [y - y_min for y in y_coords]
    return JsonResponse({
        'player_coords': 'player_coords',
        'x_coords': x_coords,
        'y_coords': y_coords
    })

@csrf_exempt
@api_view(["POST"])
def coord(request):
    generated_rooms = Room.objects.all()

    x_coords = [room.coordinates[0] for room in generated_rooms[:7]]
    x_min = np.amin(x_coords)
    if x_min < 0:
        x_coords = [x - x_min for x in x_coords]
    y_coords = [room.coordinates[1] for room in generated_rooms[:7]]
    y_min = np.amin(y_coords)
    if y_min < 0:
        y_coords = [y - y_min for y in y_coords]

    flag = False
    for idx in range(len(x_coords)):
        if request.data[0] == x_coords[idx] and request.data[1] == y_coords[idx]:
            flag = True
            break

    if flag:
        # print(request.data[0], request.data[1], 'True')
        return JsonResponse({
            'coord_exist': True,
        })
    else:
        # print(request.data[0], request.data[1], 'False')
        return JsonResponse({
            'coord_exist': False,
        })

@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    players = room.playerNames(player_id)
    return JsonResponse({'uuid': uuid, 'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players}, safe=True)


# @csrf_exempt
@api_view(["POST"])
def move(request):
    dirs={"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data['direction']
    room = player.room()
    nextRoomID = None
    if direction == "n":
        nextRoomID = room.n_to
    elif direction == "s":
        nextRoomID = room.s_to
    elif direction == "e":
        nextRoomID = room.e_to
    elif direction == "w":
        nextRoomID = room.w_to
    if nextRoomID is not None and nextRoomID > 0:
        nextRoom = Room.objects.get(id=nextRoomID)
        player.currentRoom=nextRoomID
        player.save()
        players = nextRoom.playerNames(player_id)
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
        # for p_uuid in currentPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        # for p_uuid in nextPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
        return JsonResponse({'name':player.user.username, 'title':nextRoom.title, 'description':nextRoom.description, 'players':players, 'error_msg':""}, safe=True)
    else:
        players = room.playerNames(player_id)
        return JsonResponse({'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'error_msg':"You cannot move that way."}, safe=True)


@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error':"Not yet implemented"}, safe=True, status=500)
