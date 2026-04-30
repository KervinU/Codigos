from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('registro/', views.registro, name='registro'),

    path('carrito/', views.carrito, name='carrito'),
    path('carrito/agregar/<int:id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/quitar/<int:id>/', views.quitar_del_carrito, name='quitar_del_carrito'),
    path('checkout/', views.checkout, name='checkout'),

    path('agregar/', views.agregar_producto, name='agregar_producto'),
    path('editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
]