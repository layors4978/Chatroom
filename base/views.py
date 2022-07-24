from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import HttpResponse
from .models import Message, Room, Topic
from .forms import Room_form
import datetime

# Create your views here.

def loginpage(request):
    page='login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request, '此使用者不存在')

        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, '帳號或密碼錯誤')

    context={'page':page}
    return render(request, 'base/login_register.html', context)

def logoutMe(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form=UserCreationForm()

    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, '註冊時發生錯誤')

    return render(request, 'base/login_register.html', {'form':form})

def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)|
        Q(description__icontains=q)
        )
    topics=Topic.objects.all()
    comments=Message.objects.all().filter(
        Q(room__topic__name__icontains=q)
    )
    room_num=rooms.count()

    context = {
        'rooms':rooms,
        'topics':topics,
        'comments':comments,
        'room_num':room_num,
    }
    return render(request, 'base/home.html', context)

def room(request, roomnum):
    room=Room.objects.get(id=roomnum) #得到id等於room的room
    comments=room.message_set.all().order_by('-created')#得到room的所有message，且照時間升序排序
    participants=room.participants.all()

    if request.method=='POST':
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', roomnum=room.id) 

    context={
        'room' : room,
        'comments' : comments,
        'participants' : participants
    }
    return render(request, 'base/room.html', context)

def profile(request, userid):
    user=User.objects.get(id=userid)
    rooms=user.room_set.all()
    comments=user.message_set.all()
    topics=Topic.objects.all()
    context={
        'user' : user,
        'rooms' : rooms,
        'comments' : comments,
        'topics' : topics,
    }
    return render(request, 'base/profile.html', context)

@login_required(login_url='/login')
def create_room(request):
    form=Room_form()
    if request.method=='POST':
        form=Room_form(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host=(request.user)
            room.save()
            room.participants.add(request.user)
            return redirect('home')

    context={'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def update_room(request, roomnum):
    room=Room.objects.get(id=roomnum)
    form=Room_form(instance=room)

    if request.user!=room.host:
        return HttpResponse('你不是原PO')

    if request.method=='POST':
        form=Room_form(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def delete_room(request, roomnum):
    room=Room.objects.get(id=roomnum)

    if request.user!=room.host:
        return HttpResponse('你不是原PO')

    if request.method=='POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url='/login')
def delete_message(request, messagenum):
    message=Message.objects.get(id=messagenum)

    if request.user!=message.user:
        return HttpResponse('你不是原PO')

    if request.method=='POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj':message})