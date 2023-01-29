from django.urls import path
from . views import *

urlpatterns = [

    path('admin-login',admin_login,name='admin-login'),
    path('admin-logout',admin_logout,name='admin-logout'),
    path('users-list',users_list,name='users-list'),
    path('create-user',create_user,name='create-user'),
    path('department-list',department_list,name='department-list'),
    path('create-department',create_department,name='create-department'),
    path("edit-department/<int:id>",edit_department,name='edit-department'),
    path('delete-department/<int:id>',delete_department,name='delete-department')
    
]
