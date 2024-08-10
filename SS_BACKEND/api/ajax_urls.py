from django.urls import path
from api.ajax import *

urlpatterns = [
    path('get_error/', get_error, name='get_error'),
    path('get_success/', get_success, name='get_success'),
    path('connexion/', connexion, name='connexion'),
    path('deconnexion/', deconnexion, name='deconnexion'),
    path('utilisateur/', utilisateur, name='utilisateur'),
    path('inscription/', inscription, name='inscription'),
]