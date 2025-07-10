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

def productos_con_descuento(request):
    descuentos = Descuento.objects.select_related('producto').all()
    productos = [d.producto for d in descuentos]

    descuentos_dict = {d.producto_id: d for d in descuentos}

    carrito = request.session.get('carrito', {})
    total_items = sum(item['cantidad'] for item in carrito.values())

    return render(request, 'Inicio/descuentos.html', {
        'productos': productos,
        'descuentos': descuentos_dict,
        'total_items': total_items,
    })



def sesionInicada(request):
    correo = request.POST.get('correoUsuario')
    password = request.POST.get('passwordUsuario')

    if correo == 'admin1234' and password == '1234admin':
        request.session['admin_token'] = True
        return redirect('admin_inicio')

    try:
        usuario = Usuario.objects.get(email=correo)
        if check_password(password, usuario.contraseña):
            request.session['usuario_id'] = usuario.id

            carrito_sesion = request.session.get('carrito', {})
            carrito_db, created = Carrito.objects.get_or_create(usuario=usuario, estado='activo')

            for prod_id, item in carrito_sesion.items():
                producto = Producto.objects.get(id=prod_id)

                precio_final = Decimal(item.get('precio_descuento', item['precio']))

                item_db, creado = CarritoProducto.objects.get_or_create(
                    carrito=carrito_db,
                    producto=producto,
                    defaults={
                        'cantidad': item['cantidad'],
                        'precio_unitario': precio_final
                    }
                )
                if not creado:
                    item_db.cantidad += item['cantidad']
                    item_db.save()

            request.session['carrito'] = {}

            return redirect('General')

        else:
            messages.error(request, 'Contraseña incorrecta')

    except Usuario.DoesNotExist:
        messages.error(request, 'Correo no registrado')

    return redirect('login')