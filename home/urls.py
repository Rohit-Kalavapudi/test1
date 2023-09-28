
from django.contrib import admin
from django.urls import path,include
from home import views

urlpatterns = [
    path('',views.land,name='land'),
    path('home',views.index,name='home'),
    path('contact',views.contact,name='contact'),
    path('start',views.start,name='start'),
    path('land',views.land,name='land'),
    path('doctors',views.doctors,name='doctors'),
    path('signin',views.signin,name="signin"),
    path('signup',views.signup,name="signup"),
    path('signout',views.signout,name="signout"),
    path('display',views.display,name="display"),
    path('update/<str:id>',views.update,name="update"),
    path('delete/<str:id>',views.delete,name="delete") ,
    path('search',views.search,name="search"),

]
