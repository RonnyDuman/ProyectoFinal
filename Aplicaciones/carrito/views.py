from Aplicaciones.productos.models import Producto
from Aplicaciones.descuentos.models import Descuento
from Aplicaciones.carrito.models import Carrito
from Aplicaciones.usuarios.models import Usuario
from Aplicaciones.carritoproductos.models import CarritoProducto
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
