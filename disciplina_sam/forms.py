from django.db import models
from django import forms
from disciplina_sam.models import Falta, Seguimiento_De_Falta, Categoria

class FaltaForma(forms.ModelForm):
    class Meta:
        model = Falta
        fields = ['fecha','carga_horario','matricula','categoria','detalle','activo']

class AccionForma(forms.ModelForm):
    class Meta:
        model = Seguimiento_De_Falta
	fields = ['falta','fecha','accion']
        
        widgets = {
            'falta':forms.HiddenInput(),
        }
        exclude = ['falta']

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
#    fields = ['nombre','valor']
        exclude = ['periodo_lectivo']

#    fields = ['nombre','valor','periodo_lectivo']
