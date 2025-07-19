from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from Aplicaciones.pedidos.models import Pedido
from Aplicaciones.pedidoproductos.models import PedidoProducto
from Aplicaciones.pagos.models import Pago
from Aplicaciones.productos.models import Producto
import json
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from Aplicaciones.carrito.models import Carrito
from Aplicaciones.carritoproductos.models import CarritoProducto
from Aplicaciones.productos.models import Producto
from Aplicaciones.pedidos.models import Pedido
from Aplicaciones.pedidoproductos.models import PedidoProducto
from Aplicaciones.pagos.models import Pago

# Create your views here.

#Esta funcion hace que solo usuarios logueados pueden acceder
@login_required 
#Definimos la funcion para reciba el pedido_id como parámetro desde la URL.
def pago_paypal_simulado(request, pedido_id):
    #Busca el Pedido con ese ID y que pertenezca al usuario actual.
    pedido = Pedido.objects.get(id=pedido_id, usuario=request.user)
    pago = pedido.pago

    if request.method == 'POST':
        pago.estado_pago = 'completado'
        pago.fecha_pago = timezone.now()
        pago.save()

        pedido.estado_pedido = 'enviado'  # o pendiente de envío
        pedido.save()

     #Cambia el estado del pago a "completado" y registra la fecha actual.
    if request.method == 'POST':
        pago.estado_pago = 'completado'
        pago.fecha_pago = timezone.now()
        pago.save()

        pedido.estado_pedido = 'enviado'  # o pendiente de envío
        pedido.save()

        #redirigimos a la pagina de confirmacion
        return redirect('pedido_confirmado', pedido_id=pedido.id)
    #Si el método no es POST (es decir, cuando el usuario entra por primera vez a esta vista), se muestra la plantilla HTML de pago simulado.
    return render(request, 'pagos/paypal_simulado.html', {
        'pedido': pedido,
        'pago': pago
    })

#Permite que la función acepte solicitudes sin token CSRF
@csrf_exempt
#definimos la funcion 
def capture_order(request):