from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    # path('room/', views.room, name="room"),
    path('signin/', views.signin, name="signin"),
    path('signup/', views.signup, name="signup"),
    path('signout/', views.signout, name='signout'),
]