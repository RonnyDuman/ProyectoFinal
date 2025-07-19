from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from Aplicaciones.pedidos.models import Pedido
from Aplicaciones.pedidoproductos.models import PedidoProducto
from Aplicaciones.pagos.models import Pago
from Aplicaciones.productos.models import Producto


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Aplicaciones.carrito.models import Carrito
from Aplicaciones.productos.models import Producto
from Aplicaciones.usuarios.models import Usuario
# Create your views here.


#definimos la funcion
def realizar_compra(request):