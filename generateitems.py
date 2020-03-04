"""
Generate Items
    Load JSON items and populate items in DB.
"""

import json
import os
import random
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adv_project.settings")
django.setup()

# Load models
from adventure.models import Item
from adventure.models import Room


#  Load items.json
items_path = os.path.join(os.getcwd(), 'mapgen', 'items.json')
with open(items_path, 'r') as file:
    items_raw = json.load(file)


#  Get all rooms
rooms = Room.objects.all()

def create_random_item(item_dict):
    r_category = random.choice(list(item_dict.keys()))
    r_item = random.choice(item_dict[r_category])
    item_name = list(r_item.keys())[0]
    item_desc = r_item[item_name]
    new_item = Item(
        name = item_name,
        description = item_desc,
        value = random.randint(100, 10000) 
    )
    new_item.save()
    return new_item


def place_item_in_room(room, item):
    room_items = room.items
    print(f'room: {room_items}; item_pk: {item.pk}; item_name: {item.name}')
    room.items.update({item.pk: item.name})
    room.save()

if __name__ == "__main__":
    for _ in range(400):
        try:
            place_item_in_room(
                room=random.choice(rooms),
                item=create_random_item(items_raw))
        except:
            print('missed')