import datetime
import re
import django.forms.widgets

from django.db.models import Q, Count
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.template import loader
from django.contrib import messages
from .models import HubPageDataModel, ChatMessages, Contacts, Questions
import datetime
from django.forms.widgets import DateTimeInput
# Create your views here.


def checkUserPermission(request):
    return request.user.groups.filter(name='Moderators').exists() or request.user.is_superuser


def signup(request):
    template = loader.get_template('StudentHub/SignUpPage.html')
    return HttpResponse(template.render({}, request))


def signupuser(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    first_name = request.POST['firstname']
    last_name = request.POST['lastname']
    err_mess = ''

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.fullmatch(regex, email) and email != '':
        err_mess += 'Email is not the right format.'

    if not (username.isidentifier()
            and first_name.isalpha()
            and last_name.isalpha()
            and (not password.isspace())):
        err_mess += 'Please complete all the fields with the right values.'

    if request.POST['password'] != request.POST['confirm_password']:
        err_mess += 'Please match your password.'

    if err_mess != '':
        messages.error(request,  err_mess)
        return HttpResponseRedirect(reverse('sign-up'))

    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        # if request.POST['password'] != request.POST['confirm_password']:
        #     messages.error(request,  'Please match your password.')
        #     return HttpResponseRedirect(reverse('sign-up'))

        user.save()
    except Exception as excep:
        messages.error(request, 'Please complete all the fields.')
        print('SignUp error: ' + str(excep))
        return HttpResponseRedirect(reverse('sign-up'))

    return HttpResponseRedirect(reverse('login-user'))


def hub(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('login-user')
    context= {}
    return render(request, 'StudentHub/Lobby.html', context)


def addpost(request, slug):
    if not request.user.is_authenticated:
        return redirect('login-user')
    template = loader.get_template('StudentHub/AddPost.html')
    return HttpResponse(template.render({}, request))


def addpost_save(request, slug):
    if not request.user.is_authenticated:
        return redirect('login-user')
    title = request.POST['title']
    date_now = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
    date_end = (request.POST['date_end'].replace('T', ' '))
    description = request.POST['description']

    if (not title.isidentifier()) or date_end == '' or description.isspace() or description == '' or date_end < date_now:
        err_mess = ''
        if date_end < date_now and date_end != '':
            err_mess = ' End date must have a value grater than today.'
        messages.error(request, 'Please complete all the fields with the right values.' + err_mess)
        return HttpResponseRedirect(reverse('addpost', args=(slug,)))

    try:
        post = HubPageDataModel(
            title=title,
            subject=slug,
            author=request.user,
            date=date_now,
            date_end=date_end,
            description=description,
            )
        post.save()
    except Exception as excep:
        messages.error(request, 'Please complete all the fields.')
        print('AddPost error: ' + str(excep))
        return HttpResponseRedirect(reverse('addpost', args=(slug,)))

    return HttpResponseRedirect(reverse('activity', args=(slug,)))


def editpost(request, slug, id):
    if not request.user.is_authenticated:
        return redirect('login-user')
    post = HubPageDataModel.objects.get(subject=slug, id=id)
    if not request.user.is_authenticated:
        return redirect('login-user')
    if checkUserPermission(request) is False and post.author != str(request.user):
        return HttpResponseRedirect(reverse('activity', args=(slug, )))

    date_end = post.date_end.strftime('%Y-%m-%dT%H:%M')
    template = loader.get_template('StudentHub/EditPost.html')
    context = {
        'post': post,
        'date_end': date_end,
    }
    return HttpResponse(template.render(context, request))


def editpost_save(request, slug, id):
    if not request.user.is_authenticated:
        return redirect('login-user')
    title = request.POST['title']
    date_now = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
    date_end = (request.POST['date_end'].replace('T', ' '))
    description = request.POST['description']
    post = HubPageDataModel.objects.get(subject=slug, id=id)
    if checkUserPermission(request) is False and post.author != str(request.user):
        return HttpResponseRedirect(reverse('activity', args=(slug, )))

    if (not title.isidentifier()) or date_end == '' or description.isspace() or description == '' or date_end < date_now:
        err_mess = ''
        if date_end < date_now and date_end != '':
            err_mess = ' End date must have a value grater than today.'
        messages.error(request, 'Please complete all the fields with the right values.' + err_mess)
        return HttpResponseRedirect(reverse('editpost', args=(slug, id,)))

    try:
        post.title = title
        post.date = date_now
        post.date_end = date_end
        post.description = description
        post.save()
    except Exception as excep:
        messages.error(request, 'Please complete all the fields.')
        print('AddPost error: ' + str(excep))
        return HttpResponseRedirect(reverse('editpost', args=(slug, id,)))

    return HttpResponseRedirect(reverse('activity', args=(slug,)))


def deletedata(request, id, slug):
    if not request.user.is_authenticated:
        return redirect('login-user')
    data = HubPageDataModel.objects.get(id=id)
    print(checkUserPermission(request) is False)
    if checkUserPermission(request) is False and data.author != str(request.user):
        return HttpResponseRedirect(reverse('activity', args=(slug, )))
    messg = ChatMessages.objects.all().filter(subject=slug, room_id=id)
    data.delete()
    messg.delete()
    return HttpResponseRedirect(reverse('activity', args=(slug,)))


def activity(request, slug):
    if not request.user.is_authenticated:
        return redirect('login-user')

    template = loader.get_template('StudentHub/ActivityBlueprint.html')

    data = HubPageDataModel.objects.all()
    date_now = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')

    for x in data:
        if x.date_end.strftime('%Y-%m-%d %H:%M') < date_now:
            x.delete()
    data = HubPageDataModel.objects.all().values()

    try:
        questionList = Questions.objects.select_related('contact_id__dev_id').filter(contact_id__dev_id__username=request.user)
        # for x1 in questionList:
        #     print(x1.title)
    except Exception as excep:
        print('Contact error: ' + str(excep))

    devList = Contacts.objects.all()

    totalUsers = User.objects.all().count()

    context = {
        'activity': slug,
        'dataList': data.filter(subject=slug),
        'slug': slug,
        'checkPermission': checkUserPermission(request),
        'devList': devList,
        'questionList': questionList,
        'user': (User.objects.get(username=request.user).first_name + ' ' + User.objects.get(username=request.user).last_name),
        'totalUsers': totalUsers,
    }

    return HttpResponse(template.render(context, request))


def chat(request, slug, id):
    if not request.user.is_authenticated:
        return redirect('login-user')
    template = loader.get_template('StudentHub/ChatRoom.html')

    messageList = ChatMessages.objects.filter(subject=slug, room_id=id).values()

    title = HubPageDataModel.objects.get(subject=slug, id=id).title

    context = {
        'messageList': messageList,
        'section': slug,
        'room_id': id,
        'activity': slug,
        'title': title,
    }
    return HttpResponse(template.render(context, request))


def search_bar(request):
    slug = 'search'
    if not request.user.is_authenticated:
        return redirect('login-user')
    # checkPermission = False
    # if request.user.groups.filter(name='Moderators').exists():
    #     checkPermission = True
    template = loader.get_template('StudentHub/ActivityBlueprint.html')
    data = HubPageDataModel.objects.all()
    date_now = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')

    for x in data:
        if x.date_end.strftime('%Y-%m-%d %H:%M') < date_now:
            x.delete()

    search_value = request.POST['search_bar']
    data = HubPageDataModel.objects.all().values().filter(
        Q(title__icontains=search_value) |
        Q(subject__icontains=search_value) |
        Q(description__icontains=search_value) |
        Q(author__icontains=search_value)
    )
    if search_value == '' or search_value.isspace():
        data = None 

    context = {
        'activity': slug,
        'dataList': data,
        'slug': slug,
        'checkPermission': checkUserPermission(request),
    }
    return HttpResponse(template.render(context, request))


def contact_dev(request):
    if not request.user.is_authenticated:
        return redirect('login-user')
    template = loader.get_template('StudentHub/ContactDev.html')
    devList = Contacts.objects.values()  # this has to be replaced with contacts
    context = {
        'activity': 'contact_dev',
        'devList': devList,
    }
    return HttpResponse(template.render(context, request))


def contact_dev_save(request):
    if not request.user.is_authenticated:
        return redirect('login-user')
    title = request.POST['title']
    date_now = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
    message = request.POST['message']
    developer = request.POST['developer']

    if (not title.isidentifier()) or message.isspace() or message == '':
        messages.error(request, 'Please complete all the fields with the right values.')
        return HttpResponseRedirect(reverse('contact_dev'))

    try:
        post = Questions(
            title=title,
            message=message,
            date=date_now,
            user_id=User.objects.get(username=request.user),
            contact_id=Contacts.objects.get(full_name=developer),
        )
        post.save()
    except Exception as excep:
        messages.error(request, 'Please complete all the fields.')
        return HttpResponseRedirect(reverse('contact_dev'))

    # return HttpResponseRedirect(reverse('contact'))
    return HttpResponseRedirect(reverse('activity', args=('contact',)))






