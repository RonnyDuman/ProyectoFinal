from django.shortcuts import render, redirect, get_object_or_404
from Aplicaciones.productos.models import Producto
from Aplicaciones.categorias.models import Categoria
from Aplicaciones.carrito.models import Carrito
from decimal import Decimal
from Aplicaciones.carritoproductos.models import CarritoProducto
from django.contrib import messages
from Aplicaciones.usuarios.models import Usuario
from decimal import Decimal
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
import uuid
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
import random
from Aplicaciones.descuentos.models import Descuento
from Aplicaciones.core.decorators import admin_required


