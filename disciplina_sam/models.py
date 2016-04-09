from django.db import models
from configuracion_sam.models import Periodo_Lectivo, Subperiodo, Clase, Grupo, Estudiante, Profesor, Matricula, Pensum, Malla_Curricular


class Patrones_Categoria(models.Model):
    cantidad = models.IntegerField()
    periodo = models.IntegerField()

    class Meta:
        unique_together = ("cantidad","periodo")

    def __unicode__(self):
        return "%d eventos - %d dias" %(self.cantidad, self.periodo)

class Categoria(models.Model):
    nombre = models.CharField(max_length=40)
    notificar_profesor = models.BooleanField(default = False) # envia mensajes al profesor y representante por falta seria
    notificar_representante = models.BooleanField(default = False) # envia mensaje al representante pidiendo conversar con alumno
    notificar_profesor2 = models.BooleanField(default = False) #envia mensaje al profesor pidiendo seguir protocolo
    patrones_en_parcial = models.BooleanField(default = False)
    eventos_parcial = models.IntegerField(blank = True, null = True)
    patrones_en_periodo = models.BooleanField(default = False)
    periodo_patron = models.IntegerField(blank = True, null = True)
    eventos_patron = models.IntegerField(blank = True, null= True)
    periodo_lectivo = models.ForeignKey('configuracion_sam.Periodo_Lectivo', related_name='config_periodo_lectivo')

    class Meta:
        unique_together = ('nombre','periodo_lectivo',)

    def __unicode__(self):
        return self.nombre

class Falta(models.Model):
    fecha = models.DateField()
    carga_horario = models.ForeignKey('configuracion_sam.Pensum', related_name='config_profesor')
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
        return self.falta.categoria.nombre+" "+self.falta.matricula.estudiante.usuario.name


    


# Create your models here.