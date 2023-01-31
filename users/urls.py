from django.urls import path
from . views import *

urlpatterns = [

    path('user-login',user_login,name='user-login'),
    path('user-logout',user_logout,name='user-logout'),
    path('home-page',home_page,name='home-page'),
    path('create-userticket',create_userTicket,name='create-userticket'),
    path('delete-userticket/<int:id>',delete_userticket,name='delete-userticket')
    
]
