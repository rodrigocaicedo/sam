from django.db import models
from configuracion_sam.models import Periodo_Lectivo, Subperiodo, Clase, Estudiante, Profesor, Matricula, Carga_Horario

class Patrones_Categoria(models.Model):
    cantidad = models.IntegerField()
    periodo = models.IntegerField()

    class Meta:
        unique_together = ("cantidad","periodo")

    def __unicode__(self):
        return "%d eventos - %d dias" %(self.cantidad, self.periodo)

class Patron(models.Model):
    fecha = models.DateField()
    categoria = models.ForeignKey("Categoria")
    cantidad = models.IntegerField()

    def __unicode__(self):
        return "%s, %s" % (self.fecha, self.categoria)

class Seguimiento_De_Patron(models.Model):
    patron = models.ForeignKey("Patron")
    fecha = models.DateField()
    accion = models.TextField()

    def __unicode__(self):
        return "%s, %s" % (self.fecha, self.patron)

class Categoria(models.Model):
    nombre = models.CharField(max_length=40)
    valor = models.IntegerField()
    notificar_profesor = models.BooleanField(default = False)
    notificar_representante = models.BooleanField(default = False)
    categoria_patron = models.ForeignKey("Patrones_categoria", null=True, blank=True, default = None)
    periodo_lectivo = models.ForeignKey('configuracion_sam.Periodo_Lectivo', related_name='config_periodo_lectivo')

    class Meta:
        unique_together = ('nombre','periodo_lectivo',)

    def __unicode__(self):
        return self.nombre

class Falta(models.Model):
    fecha = models.DateField()
    carga_horario = models.ForeignKey('configuracion_sam.Carga_Horario', related_name='config_profesor')
    matricula = models.ForeignKey('configuracion_sam.Matricula', related_name='config_matricula')
    categoria = models.ForeignKey('Categoria')
    detalle = models.TextField()
    activo = models.BooleanField(default = True)
    def __unicode__(self):
        return self.categoria.nombre

class Seguimiento_De_Falta(models.Model):
    falta = models.ForeignKey('Falta')
    fecha = models.DateField()
    accion = models.TextField()

    def __unicode__(self):
        return self.falta.categoria+" "+self.falta.matricula.estudiante.name


    


# Create your models here.