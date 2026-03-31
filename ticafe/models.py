from django.db import models
# from django.contrib.auth.models import AbstractUser


# Modelo Categoria, Producto, Cliente y Pedido


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to="img_categorias/")

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    stock = models.IntegerField()
    precio = models.IntegerField()
    descuento = models.IntegerField(null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


# Utiliza clase AbstractUser para extender el modelo de usuario predeterminado de Django
# y agregar campos personalizados para el cliente. Esto permite gestionar la autenticación y
# los datos del cliente de manera más eficiente y segura, aprovechando las funcionalidades integradas de Django para el manejo de usuarios.


class Cliente(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        txt = "Cliente: {0} - {1} {2} ({3})"
        return txt.format(self.rut, self.nombre, self.apellido, self.correo)


class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    cantidad = models.IntegerField()
    total = models.IntegerField()
    descuento = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Pedido de {self.cliente} - {self.producto} x {self.cantidad} - Total: {self.total}"
