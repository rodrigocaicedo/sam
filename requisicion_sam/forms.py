from django import forms
from requisicion_sam.models import Pedido_Item, Aprobacion_Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Pedido_Item
        #fields = ['profesor','item','cantidad','presentacion','detalle','descripcion_uso','materia']
        exclude=('profesor','fecha',)

class AprobacionForm(forms.Form):
    class Meta:
        model = Aprobacion_Item


