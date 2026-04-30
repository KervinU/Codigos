from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from .models import Producto
from .forms import ProductoForm, RegistroForm, LoginForm


def es_admin(user):
    return user.is_authenticated and user.is_staff


def obtener_carrito(request):
    return request.session.get('carrito', {})


def guardar_carrito(request, carrito):
    request.session['carrito'] = carrito
    request.session.modified = True


def inicio(request):
    q = request.GET.get('q', '')
    productos = Producto.objects.all().order_by('nombre')

    if q:
        productos = productos.filter(
            Q(nombre__icontains=q) | Q(descripcion__icontains=q)
        )

    return render(request, 'productos/inicio.html', {
        'productos': productos,
        'q': q,
    })


def login_usuario(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    destino = request.GET.get('next') or request.POST.get('next') or reverse('inicio')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(destino)
    else:
        form = LoginForm()

    return render(request, 'usuarios/login.html', {
        'form': form,
        'next': destino,
    })


def logout_usuario(request):
    logout(request)
    return redirect('inicio')


def registro(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    destino = request.GET.get('next') or request.POST.get('next') or reverse('inicio')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(destino)
    else:
        form = RegistroForm()

    return render(request, 'usuarios/registro.html', {
        'form': form,
        'next': destino,
    })


def carrito(request):
    carrito_session = obtener_carrito(request)
    items = []
    total = Decimal('0.00')

    for producto_id, cantidad in carrito_session.items():
        producto = get_object_or_404(Producto, id=producto_id)
        subtotal = producto.precio * cantidad
        total += subtotal
        items.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal,
        })

    return render(request, 'productos/carrito.html', {
        'items': items,
        'total': total,
    })


def agregar_al_carrito(request, id):
    producto = get_object_or_404(Producto, id=id)
    carrito_session = obtener_carrito(request)

    producto_id = str(producto.id)
    if producto_id in carrito_session:
        carrito_session[producto_id] += 1
    else:
        carrito_session[producto_id] = 1

    guardar_carrito(request, carrito_session)
    return redirect('carrito')


def quitar_del_carrito(request, id):
    carrito_session = obtener_carrito(request)
    producto_id = str(id)

    if producto_id in carrito_session:
        del carrito_session[producto_id]

    guardar_carrito(request, carrito_session)
    return redirect('carrito')


def checkout(request):
    carrito_session = obtener_carrito(request)

    if not request.user.is_authenticated:
        return redirect(f"{reverse('registro')}?next={reverse('checkout')}")

    items = []
    total = Decimal('0.00')

    for producto_id, cantidad in carrito_session.items():
        producto = get_object_or_404(Producto, id=producto_id)
        subtotal = producto.precio * cantidad
        total += subtotal
        items.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal,
        })

    if request.method == 'POST':
        request.session['carrito'] = {}
        request.session.modified = True
        return render(request, 'productos/checkout.html', {
            'items': items,
            'total': total,
            'compra_realizada': True,
        })

    return render(request, 'productos/checkout.html', {
        'items': items,
        'total': total,
        'compra_realizada': False,
    })


@user_passes_test(es_admin, login_url='login')
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = ProductoForm()

    return render(request, 'productos/producto_form.html', {
        'form': form,
        'titulo': 'Agregar producto',
        'boton': 'Guardar producto'
    })


@user_passes_test(es_admin, login_url='login')
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'productos/producto_form.html', {
        'form': form,
        'titulo': 'Editar producto',
        'boton': 'Actualizar producto'
    })


@user_passes_test(es_admin, login_url='login')
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        producto.delete()
        return redirect('inicio')

    return render(request, 'productos/eliminar_producto.html', {'producto': producto})