from django.urls import path
from api import ajax

urlpatterns = [
    path('connexion/', ajax.connexion, name='connexion'),
    path('utilisateur/', ajax.utilisateur, name='utilisateur'),
    path('inscription/', ajax.inscription, name='inscription'),
    path('add_home/', ajax.add_home, name='add_home'),
    path('alter_home/', ajax.alter_home, name='alter_home'),
    path('remove_home/', ajax.remove_home, name='remove_home'),
    path('read_home/', ajax.read_home, name='read_home'),
    path('add_camera/', ajax.add_camera, name='add_camera'),
    path('alter_camera/', ajax.alter_camera, name='alter_camera'),
    path('remove_camera/', ajax.remove_camera, name='remove_camera'),
    path('add_home_member/', ajax.add_home_member, name='add_home_member'),
    path('alter_home_member/', ajax.alter_home_member, name='alter_home_member'),
    path('remove_home_member/', ajax.remove_home_member, name='remove_home_member'),
    path('read_home_member/', ajax.read_home_member, name='read_home_member'),
    path('handle_video_feed/<int:camera_id>/', ajax.api_handle_video_feed, name='handle_video_feed'),
    
    path('twiml_response/', ajax.twiml_response, name='twiml_response'),
]
