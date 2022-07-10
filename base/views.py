from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import RoomForm
from .models import Room,Topic,Message


# Create your views here.
# rooms = [
#     {'id':1, 'name':'Learn Python'},
#     {'id':2, 'name':'Learn Node JS'},
#     {'id':3, 'name':'Learn Spring Boot'},
# ]

def login_page(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request,username=username, password=password)

        if user :
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist.')
    context = {"page":page}
    return render(request,'base/login_register.html',context)

def register_page(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Error while user registration.')
    return render(request,'base/login_register.html', {"form": form})

def logout_user(request):
    logout(request)
    return redirect('login')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
   
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains= q) |
        Q(description__icontains=q)
        )
    topics = Topic.objects.all()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {
        'rooms': rooms,
        'topics':topics,
        'room_count': rooms.count(),
        "room_messages": room_messages
    }
    return render(request,'base/home.html',context)

def room(request,id):

    room = Room.objects.get(id=id)
    if request.method=="POST":
        room_message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('comment')
        )
        room.participants.add(request.user)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    context = {'room' : room , 'room_messages':room_messages, 'participants': participants}
    return render(request,'base/room.html', context)

@login_required(login_url='login')
def create_room(request):
    if request.method =="POST":
        # print(request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            room  = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')

    form = RoomForm()
    context = {"form" : form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def update_room(request,id):
    room = Room.objects.get(id=id)
    # print(type(room.host),type(request.user))
    # print(request.user.username==str(room.host))
    if request.user == room.host:
        form = RoomForm(instance=room)
        if request.method == "POST":
            form = RoomForm(request.POST, instance=room)
            if form.is_valid():
                form.save()
                return redirect('home')
        context = {"form" : form}
        return render(request,'base/room_form.html',context)
    else:
        return HttpResponse("You are not authorised to update this room.")


@login_required(login_url='login')
def delete_room(request,id):
    room = Room.objects.get(id=id)
    if request.user == room.host:
        if request.method == "POST":
            room.delete()
            return redirect('home')
        return render(request,'base/delete.html',{"obj": room})
    else:
        return HttpResponse("You are not authorised to delete this room.")


@login_required(login_url='login')
def delete_message(request,msg_id):
    message = Message.objects.get(id=msg_id)
    # print(request.headers['Referer'])
    if request.user == message.user:
        if request.method == "POST":
            message.delete()
            return redirect('home')
        return render(request,'base/delete.html',{"obj": message})
    else:
        return HttpResponse("You are not authorised to delete this message.")

def userProfile(request,id):
    user = User.objects.get(id=id)
    topics = Topic.objects.all()
    rooms = user.room_set.all()
    room_messages = Message.objects.filter(user = user)
    context = {"user" : user, "topics":topics, "rooms":rooms, "room_messages":room_messages}
    return render(request,'base/profile.html',context)