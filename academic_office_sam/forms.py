__author__ = 'Rodrigo'
from django import forms
from academic_office_sam.models import Grade

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade

