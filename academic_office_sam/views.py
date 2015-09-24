from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from django.forms.models import inlineformset_factory
from django.views.generic import CreateView
from django.core.urlresolvers import reverse

from configuracion_sam.models import Matricula

from academic_office_sam.models import Grade, Student_Grade
from academic_office_sam.forms import GradeForm


class register_grade(CreateView):
    form_class = GradeForm
    template_name = 'academic_office_sam/registro'

    def get_success_url(self):
        return reverse("create_grade", args=(self.object.id,))

    def form_valid(self, form):
        response = super(register_grade, self).form_valid(form)
        periodo_lectivo = self.request.session["schoolyear"]
        assignment_id = self.object.id
        materia = self.object.materia
        students = Matricula.objects.filter(clase__id = materia.clase_id).order_by("estudiante__usuario__last_name")
        for x in students:
            student_grade = Student_Grade.objects.create(assignment = self.object, student = x, grade = 0)
            student_grade.save()
        return response


def create_grade(request, grade_id):
    grade = Grade.objects.get(pk = grade_id)
    students = Matricula.objects.filter(clase__id = grade.materia.clase_id).order_by("estudiante__usuario__last_name")
    Student_Grade_FormSet = inlineformset_factory(Grade, Student_Grade, extra = 0)
    context = RequestContext(request)
    formset = Student_Grade_FormSet(instance = grade)
    if request.method == "POST":
        formset = Student_Grade_FormSet(request.POST, instance = grade)
        if formset.is_valid():
            formset.save()
            return redirect("/faltas/disciplina/")
        else:
            for form in formset:
                print form.errors
                return render_to_response("academic_office_sam/students_grades",
                                  {"students":students, "formset":formset},
                                  context)
    else:
        return render_to_response("academic_office_sam/students_grades",
                                  {"students":students, "formset": formset},
                                  context)