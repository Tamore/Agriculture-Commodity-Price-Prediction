
from django.contrib import admin
from django.urls import path
from app import views
urlpatterns = [
    path('', views.index, name='index'),
    path('registration', views.registration, name='registration'),
    path('log_in', views.log_in, name='log_in'),
    path('log_out', views.log_out, name='log_out'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('predict', views.predict, name='predict'),
    path('pre', views.pre, name='pre')
]
