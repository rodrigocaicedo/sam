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
#        fields = ['nombre','valor', "notificar_profesor", "notificar_representante", "categoria_patron"]
        exclude = ["periodo_lectivo"]

    def clean_eventos_parcial(self):
        eventos_parcial = self.cleaned_data["eventos_parcial"]
        if eventos_parcial is not None:
            if eventos_parcial <=0:
                raise forms.ValidationError("Ingrese un numero mayor a 0")
        return eventos_parcial

    def clean_periodo_patron(self):
        periodo_patron = self.cleaned_data["periodo_patron"]
        if periodo_patron is not None:
            if periodo_patron <=0:
                raise forms.ValidationError("Ingrese un numero mayor a 0")
        return periodo_patron

    def clean_eventos_patron(self):
        eventos_patron = self.cleaned_data["eventos_patron"]
        if eventos_patron is not None:

            if eventos_patron <=0:
                raise forms.ValidationError("Ingrese un numero mayor a 0")
        return eventos_patron

#    fields = ['nombre','valor','periodo_lectivo']
