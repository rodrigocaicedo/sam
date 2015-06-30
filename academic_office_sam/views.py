from django.shortcuts import render, redirect
from django.template import RequestContext

from academic_office_sam.forms import GradeForm


def register_grade(request):
    context = RequestContext(request)
    if request.method == "POST":
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(disciplina)
    else:
        form = GradeForm()
        return render_to_response('academic_office_sam/registro',{'form':form},context)



# Create your views here.
