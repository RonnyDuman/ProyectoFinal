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
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')
    
     # Traer usuario desde sesión del manual
    usuario = Usuario.objects.get(id=usuario_id)

    # Luego continua igual y busca el carrito de la BDD
    carrito_db = Carrito.objects.filter(usuario=usuario, estado='activo').first()

    print(carrito_db)
    if carrito_db:
        # Obtener los productos y cantidades del carrito en BD
        items = carrito_db.productos_en_carrito.select_related('producto').all()

     # Armar un diccionario tipo sesión para reutilizar lógica o templates
        carrito = {}
        for item in items:
            carrito[str(item.producto.id)] = {
                'nombre': item.producto.nombre,
                'precio_descuento': float(item.precio_unitario),  # ajusta si tienes campo descuento
                'cantidad': item.cantidad,
                'total': float(item.subtotal()),
            }
        else:
        # Si no hay carrito en BD, intentar obtener de sesión
            carrito = request.session.get('carrito', {})
        if not carrito:
              # Si sigue vacío, redirigir al detalle carrito o página principal
             return redirect('detalle_carrito')