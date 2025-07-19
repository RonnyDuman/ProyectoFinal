from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from Aplicaciones.productos.models import Producto
from Aplicaciones.descuentos.models import Descuento
from django.utils import timezone

# Create your views here.

def nuevo_descuento(request):
    productos = Producto.objects.all()
    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        porcentaje = request.POST.get('porcentaje_descuento')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        #Verificamos si ya existe un descuento activo
        hoy = timezone.now().date()
        descuento_activo = Descuento.objects.filter(
            producto_id=producto_id,
            fecha_inicio__lte=hoy,
            fecha_fin__gte=hoy
        ).first()

        #Actualizamos el descuento si ya existe
        if descuento_activo:
            descuento_activo.porcentaje_descuento = porcentaje
            descuento_activo.fecha_inicio = fecha_inicio
            descuento_activo.fecha_fin = fecha_fin
            descuento_activo.save()
            messages.success(request, 'Descuento actualizado correctamente')

