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