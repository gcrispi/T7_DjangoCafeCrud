from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("cafeteria/", views.cafeteria, name="cafeteria"),
    path("productos/", views.productos, name="productos"),
    path("listar_productos/", views.listar_productos, name="listar_productos"),
    path("clientes/", views.clientes, name="clientes"),
    path("contacto/", views.contacto, name="contacto"),
    path("registrar/", views.registrar, name="registrar"),
    path("pedidos/", views.pedidos, name="pedidos"),
    path("carrito_pedido/", views.carrito_pedido, name="carrito_pedido"),
    path("procesar_pedido/", views.procesar_pedido, name="procesar_pedido"),
    path("quienes_somos/", views.quienes_somos, name="quienes_somos"),
    path("crear_producto/", views.crear_producto, name="crear_producto"),
    path(
        "agregar_pedido/<int:producto_id>/", views.agregar_pedido, name="agregar_pedido"
    ),
    path(
        "eliminar_producto/<int:producto_id>/",
        views.eliminar_producto,
        name="eliminar_producto",
    ),
    path(
        "editar_producto/<int:producto_id>/",
        views.editar_producto,
        name="editar_producto",
    ),
    path("login_view/", views.login_view, name="login_view"),
    path("logout_view/", views.logout_view, name="logout_view"),
]
