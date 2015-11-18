from django import forms
from requisicion_sam.models import Requisicion, Item_Request

class RequisicionForm(forms.ModelForm):
    class Meta:
        model = Requisicion

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item_Request

