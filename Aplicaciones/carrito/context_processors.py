from django.db.models import Sum
from Aplicaciones.carritoproductos.models import CarritoProducto
from Aplicaciones.carrito.models import Carrito

#Definimos la funcion 
def carrito_context(request):