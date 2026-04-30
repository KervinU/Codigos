from django.db import models

class Producto(models.Model):
    CATEGORIAS = [
        ('reloj', 'Reloj'),
        ('accesorio', 'Accesorio'),
        ('edicion', 'Edición limitada'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='reloj')
    stock = models.PositiveIntegerField(default=1)
    destacado = models.BooleanField(default=False)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre