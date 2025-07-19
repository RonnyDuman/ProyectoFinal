from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from Aplicaciones.pedidos.models import Pedido
from Aplicaciones.pedidoproductos.models import PedidoProducto
from Aplicaciones.pagos.models import Pago
from Aplicaciones.productos.models import Producto

# Create your views here.

#Esta funcion hace que solo usuarios logueados pueden acceder
@login_required 
#Definimos la funcion para reciba el pedido_id como parámetro desde la URL.
def pago_paypal_simulado(request, pedido_id):
    #Busca el Pedido con ese ID y que pertenezca al usuario actual.
    pedido = Pedido.objects.get(id=pedido_id, usuario=request.user)
    pago = pedido.pago