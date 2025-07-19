from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from Aplicaciones.pedidos.models import Pedido
from Aplicaciones.pedidoproductos.models import PedidoProducto
from Aplicaciones.pagos.models import Pago
from Aplicaciones.productos.models import Producto

# Create your views here.
