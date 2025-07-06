from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from .models import Usuario
import uuid
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
import random

# Create your views here.
def registro(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombreUsuario')
        correo = request.POST.get('correoUsuario')
        password = request.POST.get('passwordUsuario')

        # Validar que el correo sea gmail
        if not correo.endswith('@gmail.com'):
            messages.error(request, 'Por favor utiliza un correo válido de Gmail.')
            return render(request, 'iniciarSesion/login.html', {'show_register': True})
