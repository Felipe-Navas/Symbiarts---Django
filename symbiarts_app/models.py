from django.db import models
from django.utils import timezone


class Obra(models.Model):
    # Debe ser no nulo y único.
    nombre = models.CharField(max_length=50, unique=True)

    # Debe ser no nulo.
    #usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    # Debe ser no nulo y seleccionarse de las cargadas en el sistema.
    #categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    descripcion = models.CharField(max_length=200, blank=True)

    stock = models.IntegerField(default=0, null=True, blank=True)

    # Debe ser no nulo y tener el formato DD/MM/AAAA
    fecha_publicacion = models.DateField(default=timezone.now)

    # Debe ser no nulo.
    estados_obra = [
        ('D', 'Denunciada'),
        ('N', 'Normal'),
    ]
    estado = models.CharField(
        max_length=15,
        choices=estados_obra,
        default='N')

    dimensiones = models.CharField(max_length=200, blank=True)

    precio = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True)

    # Debe ser no nulo y seleccionarse de los cargados en el sistema.
    tipos_obra = [
        ('AS', 'ArtSale'),
        ('AW', 'ArtWork'),
    ]
    tipo = models.CharField(
        max_length=15,
        choices=tipos_obra,
        default='AW')

    # tags

    def __str__(self):
        return self.nombre


class ObraArchivo(models.Model):
    # Debe ser no nulo y pude ser mas de uno
    obra = models.ForeignKey(
        Obra, on_delete=models.CASCADE, related_name='archivos')
    archivo = models.FileField(upload_to='archivos/')
