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

]