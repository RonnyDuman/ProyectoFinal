from Aplicaciones.productos.models import Producto
from Aplicaciones.descuentos.models import Descuento
from Aplicaciones.carrito.models import Carrito
from Aplicaciones.usuarios.models import Usuario
from Aplicaciones.carritoproductos.models import CarritoProducto
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect

#Definimos nuestra funcion
def agregar_al_carrito(request, id):
    producto = get_object_or_404(Producto, id=id)

    #Verificar si tiene descuento
    descuento_obj = Descuento.objects.filter(producto=producto).first()
    porcentaje_descuento = descuento_obj.porcentaje_descuento if descuento_obj else Decimal('0')
