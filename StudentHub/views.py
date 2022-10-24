import datetime

import django.forms.widgets
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.template import loader
from django.contrib import messages
from .models import HubPageDataModel, ChatMessages
from django.forms.widgets import DateTimeInput
# Create your views here.


def signup(request):
    template = loader.get_template('StudentHub/SignUpPage.html')
    return HttpResponse(template.render({}, request))


def signupuser(request):
    try:
        user = User.objects.create_user(
            request.POST['username'],
            request.POST['email'],
            request.POST['password'],
            first_name=request.POST['firstname'],
            last_name=request.POST['lastname']
        )
        user.save()
    except Exception:
        messages.error(request, 'Please complete all the fields.')
        return HttpResponseRedirect(reverse('sign-up'))

    if request.POST['password'] != request.POST['confirm_password']:
        messages.error(request,  'Please match your password.')
        return HttpResponseRedirect(reverse('sign-up'))

    return HttpResponseRedirect(reverse('login-user'))


def hub(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('login-user')

    context= {}
    return render(request, 'StudentHub/Lobby.html', context)


def addpost(request, slug):
    template = loader.get_template('StudentHub/AddPost.html')
    return HttpResponse(template.render({}, request))


def addpost_save(request, slug):
    try:
        post = HubPageDataModel(
            title=request.POST['title'],
            subject=request.POST['subject'],
            author=request.user,
            date=request.POST['date_now'],
            date_end=request.POST['date'],
            description=request.POST['description'],
            text=request.POST['text']
            )
        post.save()
    except Exception as excep:
        messages.error(request, 'Please complete all the fields.')
        print(excep)
        return HttpResponseRedirect(reverse('addpost', args=(slug,)))

    return HttpResponseRedirect(reverse('activity', args=(slug,)))


def deletedata(request, id, slug):
    data = HubPageDataModel.objects.get(id=id)
    data.delete()
    return HttpResponseRedirect(reverse('activity', args=(slug,)))


def activity(request, slug):
    template = loader.get_template('StudentHub/ActivityBlueprint.html')
    data = HubPageDataModel.objects.all().values()
    context = {
        'activity': slug,
        'dataList': data.filter(subject=slug),
        'slug': slug,
    }
    return HttpResponse(template.render(context, request))


def chat(request, slug, id):
    template = loader.get_template('StudentHub/ChatRoom.html')

    messageList = ChatMessages.objects.filter(subject=slug, room_id=id).values()

    context = {
        'messageList': messageList,
        'section': slug,
        'room_id': id,
    }
    return HttpResponse(template.render(context, request))


