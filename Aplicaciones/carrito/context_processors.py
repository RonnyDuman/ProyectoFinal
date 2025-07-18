from django.db.models import Sum
from Aplicaciones.carritoproductos.models import CarritoProducto
from Aplicaciones.carrito.models import Carrito

#Definimos la funcion 
def carrito_context(request):
    #Obtiene el carrito guardado en la sesión del usuario y suma todas las cantidades de productos en el carrito.
    carrito = request.session.get('carrito', {})
    total_items = sum(item['cantidad'] for item in carrito.values())
    return {'total_items_carrito': total_items}

#Definimos la funcion 
def carrito_total_items(request):
    #Obtenemos el ID del usuario desde la sesión
    usuario_id = request.session.get('usuario_id')
    total_items = 0

    #Busca el carrito activo del usuario en la base de datos
    if usuario_id:
        carrito = Carrito.objects.filter(usuario_id=usuario_id, estado='activo').first()

        if carrito:
            total_items = CarritoProducto.objects.filter(carrito=carrito).aggregate(
                total=Sum('cantidad')
            )['total'] or 0

    else:
        carrito_sesion = request.session.get('carrito', {})
        total_items = sum(item['cantidad'] for item in carrito_sesion.values())

    return {'total_items_carrito': total_items}