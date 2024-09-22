from django.urls import path
from app.views import *

urlpatterns = [
    path('', home, name='home'),
    path('login', login, name='login'),
    path('users', users, name='users'),
    path('logout', logout, name='logout'),
    path('add_user', add_user, name='add_user'),
    path('edit_user/<str:slug>', edit_user, name='edit_user'),
    path('delete_user/<str:slug>', remove_user, name='remove_user'),
]