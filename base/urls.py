from django.urls import path
from . import views

urlpatterns=[
    path('login/', views.loginpage, name="login"),
    path('logout/', views.logoutMe, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('roompage/<str:roomnum>/', views.room, name="room"),

    path('create_room/', views.create_room, name="create_room"),
    path('update_room/<str:roomnum>/', views.update_room, name="update_room"),
    path('delete_room/<str:roomnum>/', views.delete_room, name="delete_room"),
    path('delete_message/<str:messagenum>/', views.delete_message, name="delete_message"),

    path('profile/<str:userid>', views.profile, name="profile"),
]