from Aplicaciones.productos.models import Producto
from Aplicaciones.descuentos.models import Descuento
from Aplicaciones.carrito.models import Carrito
from Aplicaciones.usuarios.models import Usuario
from Aplicaciones.carritoproductos.models import CarritoProducto
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect

#Definimos nuestra funcion
def agregar_al_carrito(request, id):
    producto = get_object_or_404(Producto, id=id)

    #Verificar si tiene descuento
    descuento_obj = Descuento.objects.filter(producto=producto).first()
    porcentaje_descuento = descuento_obj.porcentaje_descuento if descuento_obj else Decimal('0')

    #Calcular el precio con descuento
    precio = Decimal(producto.precio)
    porcentaje_descuento = Decimal(porcentaje_descuento)

    if porcentaje_descuento > 0:
        precio_descuento = precio * (Decimal('1') - porcentaje_descuento / Decimal('100'))
    else:
        precio_descuento = precio

    #Verificamos si el usuario esta logeado
    usuario_id = request.session.get('usuario_id')

    
    #Si el usuario esta logeado se guarda en la BDD
    if usuario_id:
        usuario = Usuario.objects.get(id=usuario_id)
        carrito_db, created = Carrito.objects.get_or_create(usuario=usuario, estado='activo')

        #Busca un carrito activo o lo crea si no existe.
        item_db, creado = CarritoProducto.objects.get_or_create(
            carrito=carrito_db,
            producto=producto,
            defaults={
                'cantidad': 1,
                'precio_unitario': precio_descuento
            }
        )
        #Añade el producto con cantidad 1 si no existe,si ya existe, le aumenta 1 en la cantidad:
        if not creado:
            item_db.cantidad += 1
            item_db.save()

    #Si el usuario no esta logeado igual se refleja el carrito 
    else:
        carrito = request.session.get('carrito', {})
        prod_id = str(producto.id)

        #Usa un diccionario llamado 'carrito' en la sesión del navegador.
        if prod_id in carrito:
            carrito[prod_id]['cantidad'] += 1
        else:
            carrito[prod_id] = {
                'nombre': producto.nombre,
                'precio': float(precio),
                'precio_descuento': float(round(precio_descuento, 2)),
                'porcentaje_descuento': float(porcentaje_descuento),
                'cantidad': 1,
                'imagen': producto.imagen.url if producto.imagen else '',
            }
        #Si ya está en el carrito, suma 1 cantidad, si no está, lo agrega con todos los datos.
        carrito[prod_id]['total'] = round(
            carrito[prod_id]['precio_descuento'] * carrito[prod_id]['cantidad'], 2
        )
        request.session['carrito'] = carrito
        request.session.modified = True  

    return redirect('detalle_producto', producto_id=id)

#Creamos la función
def detalle_carrito(request):
    #Obtenemos los datos del carrito
    usuario_id = request.session.get('usuario_id')
    carrito_db = None
    items_db = None
    carrito_sesion = request.session.get('carrito', {})

    #Si el usuario esta logeado busca un carrito activo de la BDD y obtiene todos los datos
    if usuario_id:
        carrito_db = Carrito.objects.filter(usuario_id=usuario_id, estado='activo').first()
        if carrito_db:
            items_db = carrito_db.productos_en_carrito.select_related('producto')

    
    #Se crea un diccionario context que se enviará a la plantilla HTML (detalleCarrito.html)
    context = {
        'items_db': None,
        'carrito': carrito_sesion,
        'subtotal': 0,
        'total': 0,
    }

    #Si hay items_db,para cada producto del carrito:
    if items_db:
        items_con_descuento = []
        subtotal = 0
        for item in items_db:
            precio_original = item.producto.precio
            precio_unitario = item.precio_unitario

              #Se calcula el porcentaje de descuento aplicado y luego se calcula el subtotal de cada producto
            if precio_original > precio_unitario:
                porcentaje_descuento = round(float((precio_original - precio_unitario) / precio_original * 100), 2)
            else:
                porcentaje_descuento = 0
            subtotal_item = item.subtotal()
            subtotal += subtotal_item

            #Se guarda en una lista todos los detalles del producto
            items_con_descuento.append({
                'id': item.id,
                'producto': item.producto,
                'cantidad': item.cantidad,
                'precio_unitario': precio_unitario,
                'precio_original': precio_original,
                'subtotal': subtotal_item,
                'porcentaje_descuento': porcentaje_descuento,
            })

        #Actualizamos el metodo context
        context['items_db'] = items_con_descuento
        context['subtotal'] = subtotal
        context['total'] = subtotal

           #Si no hay items_db pero sí hay carrito_sesion, se actualiza también el context
    elif carrito_sesion:
        subtotal = 0
        for key, item in carrito_sesion.items():
            if 'total' not in item:
                item['total'] = item['precio_descuento'] * item['cantidad']
            subtotal += item['total']
        context['subtotal'] = subtotal
        context['total'] = subtotal
        context['carrito'] = carrito_sesion

    return render(request, 'carrito/detalleCarrito.html', context)

#Definimos la funcion
def eliminar_del_carrito(request, id):
    #Elimina un producto del carrito guardado en sesión (es decir, para usuarios que no han iniciado sesión).
    carrito = request.session.get('carrito', {})
    if id in carrito:
        del carrito[id]
        request.session['carrito'] = carrito

    return redirect('detalle_carrito')

#Definimos la funcion
def eliminar_del_carrito_db(request, item_id):
    #Elimina un producto del carrito guardado en la base de datos, es decir, de un usuario autenticado.
    item = get_object_or_404(CarritoProducto, id=item_id)
    item.delete()
    return redirect('detalle_carrito')

#Creamos la funcion
def vaciar_carrito(request):
     #Elimina todos los productos del carrito, tanto en la sesión como en la base de datos (si el usuario está autenticado).
    request.session['carrito'] = {}

    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        carrito = Carrito.objects.filter(usuario_id=usuario_id, estado='activo').first()
        if carrito:
            CarritoProducto.objects.filter(carrito=carrito).delete()

    return redirect('detalle_carrito')