from django.shortcuts import render, redirect
from Aplicaciones.productos.models import Producto
from Aplicaciones.categorias.models import Categoria
from django.shortcuts import get_object_or_404, render
from .models import Producto

# Create your views here.

def nuevo_producto(request):
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio').replace(",",".")
        stock = request.POST.get('stock')
        categoria_id = request.POST.get('categoria')
        imagen = request.FILES.get('imagen')

        if all([nombre, descripcion, precio, stock, categoria_id]):
            Producto.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,
                stock=stock,
                imagen=imagen,
                categoria_id=categoria_id
            )
            return redirect('General')

    return render(request, 'productos/nuevo.html', {'categorias': categorias})


def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    reseñas = producto.reseñas.select_related('usuario').order_by('-fecha')

