from django.urls import path
from . import views

urlpatterns = [
    path('', views.General, name='General'),
    path('categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('ofertas/', views.productos_con_descuento, name='productos_con_descuento'), 
    path('todos/', views.todos_productos, name='todos_productos'),


    path('login/', views.IniciarSesion, name='login'),

    path('pasarela/', views.sesionInicada, name='loginIn'),

    path('registro/', views.registro, name='registro'),
    path('verify_email/', views.verify_email, name='verify_email'),
    path('cerrar_sesion/', views.cerrar_sesion, name='logout'),



    
    path('panel/productos/', views.admin_productos, name='admin_productos'),
    path('panel/categorias/', views.admin_categorias, name='admin_categorias'),
    #path('admin/usuarios/', views.admin_usuarios, name='admin_usuarios'),
    #path('admin/pedidos/', views.admin_pedidos, name='admin_pedidos'),
    #path('admin/pagos/', views.admin_pagos, name='admin_pagos'),
    #path('admin/carrito/', views.admin_carrito, name='admin_carrito'),
    path('panel/descuentos/', views.admin_descuentos, name='admin_descuentos'),
    #path('admin/reseñas/', views.admin_reseñas, name='admin_reseñas'),
    #path('admin/inventario/', views.admin_inventario, name='admin_inventario'),

]