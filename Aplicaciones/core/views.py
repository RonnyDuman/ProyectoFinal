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



def General(request):
    productos = Producto.objects.all()
    descuentos = {d.producto_id: d for d in Descuento.objects.all()} 

    carrito = request.session.get('carrito', {})
    total_items = sum(item['cantidad'] for item in carrito.values())

    return render(request, 'Inicio/inicio.html', {
        'productos': productos,
        'descuentos': descuentos,
        'total_items': total_items,
    })

def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = Producto.objects.filter(categoria=categoria)
    descuentos = {d.producto_id: d for d in Descuento.objects.all()}

    carrito = request.session.get('carrito', {})
    total_items = sum(item['cantidad'] for item in carrito.values())

    return render(request, 'Inicio/categoria.html', {
        'categoria': categoria,
        'productos': productos,
        'descuentos': descuentos,
        'total_items': total_items,
    })
