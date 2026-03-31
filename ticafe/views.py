from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

# Modelo y Formularios
from .models import Categoria, Producto, Cliente, Pedido
from .forms import ClienteForm, ProductoForm, PedidoForm, UserCreationForm


# Create your views here.

# Vistas para todos los usuarios, no requieren autenticación


def inicio(request):
    return render(request, "inicio.html")


def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("inicio")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("inicio")


def cafeteria(request):
    es_usuario = False
    productos = Producto.objects.all()
    if request.user.is_authenticated:
        es_usuario = True
    contexto = {"productos": productos, "es_usuario": es_usuario}
    return render(request, "cafeteria.html", contexto)


def contacto_msg(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        mensaje = request.POST.get("mensaje")
        # Aquí puedes guardar el mensaje en la base de datos o enviarlo por correo

        texto = "Contactenos: {0} - {1} {2} ({3})"
        print(texto.format(nombre, email, mensaje))
        return redirect("inicio")
    return render(request, "contacto.html")


def agregar_pedido(request, producto_id):
    # Lógica para agregar el producto al carrito
    producto = get_object_or_404(Producto, id=producto_id)
    cantidad = int(request.POST.get("cantidad"))
    # variable de sesion carrito con diccionario vacio o con el carrito existente en la sesión
    carrito = request.session.get("carrito", {})

    if str(producto_id) in carrito:
        carrito[str(producto_id)] += cantidad
    else:
        carrito[str(producto_id)] = cantidad

    # contexto = {"producto": producto, "cantidad": cantidad}
    request.session["carrito"] = carrito

    return redirect("cafeteria")


def carrito_pedido(request):
    carrito = request.session.get("carrito", {})
    productos = []
    total = 0
    for producto_id, cantidad in carrito.items():
        # variable producto que obtiene el producto de la base de datos usando el id del producto
        producto = Producto.objects.get(id=producto_id)
        descuento = Producto.objects.get(id=producto_id).descuento
        subtotal = producto.precio * cantidad * (1 - (int(descuento) / 100))
        total += subtotal

        # Esta es la lista productos
        productos.append(
            {
                "producto": producto,
                "cantidad": cantidad,
                "subtotal": subtotal,
                "descuento": descuento,
            }
        )

    return render(request, "carrito.html", {"productos": productos, "total": total})


def procesar_pedido(request):
    carrito = request.session.get("carrito", {})

    if not carrito:
        messages.warning(request, "El carrito está vacío")
        return redirect("carrito")

    # Obtener el cliente por defecto "cafeteria"
    try:
        # Buscar cliente con nombre "cafeteria"
        cliente = Cliente.objects.get(nombre="cafeteria")
    except Cliente.DoesNotExist:
        # Si no existe, crear el cliente cafeteria
        try:
            cliente = Cliente.objects.create(
                rut="99999999-9",
                nombre="cafeteria",
                apellido="Cliente",
                direccion="Casa Central",
                correo="cafeteria@ticafe.cl",
                telefono="+56912345678",
                email="cafeteria@ticafe.cl",
            )
            messages.info(request, "Cliente cafeteria creado automáticamente")
        except Exception as e:
            messages.error(request, f"Error al crear cliente por defecto: {str(e)}")
            return redirect("carrito")

    # Crear un pedido por cada producto en el carrito
    pedidos_creados = []

    for producto_id, cantidad in carrito.items():
        try:
            # Asegurar que producto_id es entero
            producto = Producto.objects.get(id=int(producto_id))

            # Validar stock
            if producto.stock < cantidad:
                messages.warning(
                    request,
                    f"No hay suficiente stock para {producto.nombre}. "
                    f"Stock disponible: {producto.stock}",
                )
                continue

            # Calcular total con descuento
            descuento = producto.descuento or 0
            total = producto.precio * cantidad * (1 - (descuento / 100))

            # Crear el pedido
            pedido = Pedido.objects.create(
                cliente=cliente,
                producto=producto,
                cantidad=cantidad,
                total=int(total),
                descuento=descuento,
            )

            # Actualizar stock
            producto.stock -= cantidad
            producto.save()

            pedidos_creados.append(pedido)

        except Producto.DoesNotExist:
            messages.warning(request, f"Producto no encontrado: {producto_id}")
            continue
        except ValueError:
            messages.warning(request, f"ID de producto inválido: {producto_id}")
            continue

    if pedidos_creados:
        # Limpiar el carrito después de procesar
        request.session["carrito"] = {}
        request.session.modified = True

        # Calcular total del pedido
        total_pedido = sum(p.total for p in pedidos_creados)

        messages.success(
            request,
            f"¡Pedido realizado con éxito! Se crearon {len(pedidos_creados)} pedido(s). "
            f"Total: ${total_pedido}",
        )
        return redirect("carrito_pedido")
    else:
        messages.error(
            request, "No se pudo procesar el pedido. Verifica el stock disponible."
        )
        return redirect("carrito")


def eliminar_producto_carrito(request, producto_id):
    carrito = request.session.get("carrito", {})
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session["carrito"] = carrito
        request.session.modified = True
        messages.success(request, "Producto eliminado del carrito")
    return redirect("carrito")


def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, "cliente.html", {"clientes": clientes})


def contacto(request):
    return render(request, "contacto.html")


def quienes_somos(request):
    return render(request, "quienes.html")


def registrar(request):
    form = ClienteForm()
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inicio")
    return render(request, "registrar.html", {"form": form})


@login_required
def productos(request):
    productos = Producto.objects.all()
    return render(request, "crud/admin_producto.html", {"productos": productos})


@login_required
def listar_productos(request):

    query = request.GET.get("buscar")
    productos_lista = Producto.objects.select_related("categoria").all()

    # Aplicar filtro si existe búsqueda
    if query:
        productos_lista = productos_lista.filter(
            Q(nombre__icontains=query)
            | Q(descripcion__icontains=query)
            | Q(categoria__nombre__icontains=query)
        )
    # Opcional: ordenar por relevancia
    productos_lista = productos_lista.order_by("nombre")

    # Paginación
    paginator = Paginator(productos_lista, 10)
    page_number = request.GET.get("page")
    productos = paginator.get_page(page_number)

    contexto = {"productos": productos, "buscar": query}

    return render(request, "crud/admin_producto.html", contexto)


# vista requiere autienticación y que el usuario sea parte del grupo "admin"


@login_required
def crear_producto(request):
    form = ProductoForm()
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("productos")
    return render(request, "crud/form.html", {"form": form})


@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    form = ProductoForm(instance=producto)
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("productos")
    return render(request, "crud/form.html", {"form": form, "producto": producto})


@login_required
def eliminar_producto(request, producto_id):

    try:
        producto = get_object_or_404(Producto, id=producto_id)
        producto.delete()
        return redirect("productos")

    except Exception as e:
        error_message = f"No se pudo eliminar el producto: {str(e)}"
        return render(request, "crud/error.html", {"error_message": error_message})


@login_required
def pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, "pedido.html", {"pedidos": pedidos})
