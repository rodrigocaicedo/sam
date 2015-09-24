from django.db import models

class Grade_Type(models.Model):
    name = models.TextField(max_length = 30)

    def __unicode__(self):
        return self.name

class Grade(models.Model):

    parcial = models.ForeignKey("configuracion_sam.Estructura_Subperiodo")
    materia = models.ForeignKey("configuracion_sam.Materia")
    type = models.ForeignKey("Grade_Type")

    def __unicode__(self):
        return self.parcial.name + " " + self.materia.nombre + " " + self.materia.clase.clase_name


class Student_Grade(models.Model):
    assignment = models.ForeignKey("Grade")
    student = models.ForeignKey("configuracion_sam.Matricula")
    grade = models.FloatField()

    def __unicode__(self):
        return self.assignment.materia.nombre+" "+self.student.estudiante.usuario.name
# Create your models here.
