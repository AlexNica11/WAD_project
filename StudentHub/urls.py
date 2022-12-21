from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from StudentHub import views


urlpatterns = [
    path('', views.hub, name='hub'),
    path('auth/login/', LoginView.as_view(template_name='StudentHub/LoginPage.html'), name='login-user'),
    path('auth/login/signup/', views.signup, name='sign-up'),
    path('auth/login/signup/user/', views.signupuser, name='sign-up-user'),
    path('auth/logout', LogoutView.as_view(), name='logout-user'),
    # path('news/', views.party, name='news'),
    # path('jobs/', views.jobs, name='jobs'),
    # path('parties/', views.parties, name='parties'),
    # path('meets/', views.meets, name='meets'),
    # path('events/', views.events, name='events'),
    # path('ideas/', views.ideas, name='ideas'),
    path('<slug:slug>/', views.activity, name='activity'),
    path('<slug:slug>/addpost/', views.addpost, name='addpost'),
    path('<slug:slug>/addpost/save/', views.addpost_save, name='addpost_save'),
    path('<slug:slug>/delete/<int:id>/', views.deletedata, name='deletedata'),
    path('<slug:slug>/chat/<int:id>/', views.chat, name='chat'),
    path('<slug:slug>/edit/<int:id>/', views.editpost, name='editpost'),
    path('<slug:slug>/edit/<int:id>/save/', views.editpost_save, name='editpost_save'),
    path('search/bar/', views.search_bar, name='search'),
    path('contact/dev/', views.contact_dev, name='contact_dev'),
    path('contact/dev/save/', views.contact_dev_save, name='contact_dev_save'),
    # path('contact/messages', views.dev_messages, name='dev_messages'),
]
