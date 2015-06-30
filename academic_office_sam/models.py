from django.db import models

from configuracion_sam.models import Subperiodo

Materia

class Grade_Type(models):
    name = models.TextField(max_length = 30)

class Grade(models):

    subperiodo = models.ForeignKey("Subperiodo")
    materia = models.ForeignKey("Materia")
    type = models.ForeignKey("Grade_Type")
    grade = models.FloatField()


# Create your models here.
