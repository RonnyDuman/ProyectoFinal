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
    #Convierte el contenido JSON recibido del frontend en un diccionario Python.
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            usuario_id = request.session.get('usuario_id')
            metodo_pago = data.get('metodo_pago', 'paypal')  # Captura del frontend

            
            if not usuario_id:
                return JsonResponse({'error': 'Usuario no autenticado'}, status=401)

            carrito = Carrito.objects.filter(usuario_id=usuario_id, estado='activo').first()
            if not carrito:
                return JsonResponse({'error': 'No hay carrito activo'}, status=404)

            productos_en_carrito = CarritoProducto.objects.filter(carrito=carrito).select_related('producto')
            if not productos_en_carrito.exists():
                return JsonResponse({'error': 'Carrito vacío'}, status=400)

            total = sum(item.cantidad * item.precio_unitario for item in productos_en_carrito)

         # Crear Pedido
            pedido = Pedido.objects.create(
                usuario_id=usuario_id,
                fecha_pedido=timezone.now(),
                total=total,
                estado_pedido='pendiente',
                direccion_envio=carrito.usuario.direccion or 'Dirección no registrada'
            )

             # Agregar productos al pedido y actualizar stock
            for item in productos_en_carrito:
                producto = item.producto
                producto.stock = max(producto.stock - item.cantidad, 0)
                producto.save()

                PedidoProducto.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=item.cantidad,
                    precio_unitario=item.precio_unitario
                )

            # Cambiar estado del carrito a pagado
            carrito.estado = 'pagado'
            carrito.save()
            productos_en_carrito.delete()