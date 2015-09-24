__author__ = 'Rodrigo'
from django import forms
from academic_office_sam.models import Grade, Student_Grade
from configuracion_sam.models import Estructura_Subperiodo, Materia

class GradeForm(forms.ModelForm):
    """
    def __init__(self, schoolyear, *args,**kargs):
        super (GradeForm, self).__init__(*args,**kargs)
        self.fields["parcial"].queryset = Estructura_Subperiodo.objects.filter(subperiodo__periodo_lectivo = schoolyear)
        self.fields["materia"].queryset = Materia.objects.filter(clase__periodo_lectivo = schoolyear)
    """
    class Meta:
        model = Grade


class StudentGradeForm(forms.ModelForm):
    class Meta:
        model = Student_Grade

