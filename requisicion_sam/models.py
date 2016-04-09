from django.db import models
from configuracion_sam.models import Profesor, Pensum

PRES_TYPES = (
    ('U', "Unidades"),
    ('P', 'Paquetes'),
)

class Pedido_Item(models.Model):
    profesor = models.ForeignKey("configuracion_sam.Profesor")
    fecha = models.DateField()
    item = models.CharField(max_length = 20)
    cantidad = models.PositiveSmallIntegerField()
    presentacion = models.CharField(max_length = 1, choices = PRES_TYPES)
    detalle = models.TextField()
    descripcion_uso = models.TextField()
    materia = models.ForeignKey("configuracion_sam.Pensum")
    foto = models.ImageField(upload_to="pedidos/")

class Aprobacion_Item(models.Model):
    item = models.ForeignKey("Pedido_Item")
    fecha_aprobacion = models.DateField(blank=True, null=True)
    fecha_entrega = models.DateField(blank=True, null=True)

# Create your models here.