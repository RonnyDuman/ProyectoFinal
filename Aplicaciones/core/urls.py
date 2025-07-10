from django.urls import path
from . import views

urlpatterns = [
    path('', views.General, name='General'),
    path('categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('ofertas/', views.productos_con_descuento, name='productos_con_descuento'),  # 👈 nueva ruta
    path('todos/', views.todos_productos, name='todos_productos'),
]