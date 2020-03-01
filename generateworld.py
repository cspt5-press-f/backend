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


def make_room():
    pass

def save_room():
    pass

if __name__ == "__main__":
    print('complete')