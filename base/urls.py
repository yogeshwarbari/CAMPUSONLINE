from unicodedata import name
from django.urls import path
from django.views import View
from . import views


urlpatterns = [
    path('login/',views.login_page,name='login'),
    path('register/',views.register_page,name='register'),
    path('logout/',views.logout_user,name='logout'),
    path('', views.home, name='home'),
    path('room/<int:id>', views.room, name='room'),
    path('create-room/',views.create_room,name='create-room'),
    path('update-room/<int:id>',views.update_room,name='update-room'),
    path('delete-room/<int:id>',views.delete_room,name='delete-room'),
    path('delete-message/<int:msg_id>',views.delete_message,name='delete-message'),
    path('profile/<int:id>',views.userProfile,name='user-profile'),
]