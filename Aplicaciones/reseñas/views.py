from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from Aplicaciones.productos.models import Producto
from Aplicaciones.reseñas.models import Reseña
from Aplicaciones.usuarios.models import Usuario
from django.contrib import messages
# Create your views here.

#Definimos la funcion
def agregar_reseña(request, producto_id):
     #Verifica si el usuario está autenticado mediante session. Si no lo está, lo redirige al login y muestra un mensaje de error.
    if not request.session.get('usuario_id'):
        messages.error(request, "Debes iniciar sesión para dejar una reseña.")
        return redirect('login')