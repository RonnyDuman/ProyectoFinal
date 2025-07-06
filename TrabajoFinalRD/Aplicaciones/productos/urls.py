from django.urls import path
from . import views

urlpatterns = [
    path('nuevo/', views.nuevo_producto, name='nuevo_producto'),


]