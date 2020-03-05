from django.conf.urls import url
from . import api

urlpatterns = [
    url('init', api.initialize),
    url('move', api.move),
    url('say', api.say),
    url('map', api.map),
    url('drop', api.drop),
    url('grab', api.grab),
]