"""
Generate World
    The world generator.  Create all maps, items, npc's, etc in the world and populate database.


--MapGen--
Combine coordinate, name, description, layout, generation
and make a django model object that can be saved to db.
"""
# Django Setup
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adv_project.settings")
django.setup()

# Load models
from adventure.models import Room

# Load generators
from mapgen import RandomWalk, random_desc


def make_save_room(room_name, room_desc, x, y, items={}):
    new_room = Room(
        name=room_name,
        description=room_desc,
        x=x,
        y=y,
        items=items
    )
    new_room.save()

def get_room_name(room_desc):
    """TEMPORARY NAME SPLITTING"""
    return ' '.join(room_desc.split(' ')[1:4])


def build_world(size):
    path = RandomWalk(size=size)
    path_coords = path.coordinates
    for room_coord in path_coords:
        temp_desc = next(random_desc())
        make_save_room(
            room_name = get_room_name(temp_desc),
            room_desc = temp_desc,
            x = room_coord[0],
            y = room_coord[1]
        )


if __name__ == "__main__":
    build_world(500)