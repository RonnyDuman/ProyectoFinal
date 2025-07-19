from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from Aplicaciones.productos.models import Producto
from Aplicaciones.descuentos.models import Descuento
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from Aplicaciones.descuentos.models import Descuento

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

        #Crear nuevo descuento si no hay uno activo
        else:
            Descuento.objects.create(
                producto_id=producto_id,
                porcentaje_descuento=porcentaje,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )

            messages.success(request, 'Descuento creado correctamente')

        return redirect('admin_descuentos')

    return render(request, 'descuentos/nuevo.html', {'productos': productos})

#Creamos la nueva funcion
def editar_descuento(request, descuento_id):
    descuento = get_object_or_404(Descuento, id=descuento_id)

    #obtenemos los nuevos datos del formulario
    if request.method == 'POST':
        porcentaje = request.POST.get('porcentaje_descuento')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
