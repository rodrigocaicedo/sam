from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.template.loader import render_to_string

from configuracion_sam.models import Matricula, Carga_Horario, Clase

from disciplina_sam.models import Falta, Seguimiento_De_Falta, Categoria
from disciplina_sam.forms import FaltaForma, AccionForma

import json

def ac_estudiante(request):
    schoolyear = request.session['schoolyear']
    if request.is_ajax():
        q = request.GET.get('term', '')
        drugs = Matricula.objects.filter(estudiante__usuario__name__icontains = q , estudiante__usuario__is_active = True)[:20]
        results = []
        for drug in drugs:
            drug_json = {}
            drug_json['value'] = drug.estudiante.usuario.name
            results.append(drug_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def ac_profesor(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        drugs = Carga_Horario.objects.filter(profesor__usuario__name__icontains = q , activo = True)[:20]
        results = []
        for drug in drugs:
            drug_json = {}
            drug_json['value'] = drug.profesor.usuario.name
            results.append(drug_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def ac_categoria(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        drugs = Categoria.objects.filter(nombre__icontains = q )[:20]
        results = []
        for drug in drugs:
            drug_json = {}
            drug_json['value'] = drug.nombre
            results.append(drug_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def index(request):
    clases = Clase.objects.all().order_by('nivel')
    context = {'clases':clases}
    return render(request,'disciplina_sam/index',context)

def disciplina(request):
    ultimos_registros = Falta.objects.filter(activo = True).order_by('-fecha')
    context = {'ultimos_registros':ultimos_registros}
    return render(request,'disciplina_sam/disciplina',context)

def busqueda_disciplina(request):
    context = RequestContext(request)
    if "q" in request.GET:
        q_estudiante = request.GET["q_estudiante"]
        q_profesor = request.GET["q_profesor"]
        q_categoria = request.GET["q_categoria"]
        q_fecha = request.GET["q"]
        if q_fecha != "":
            if "q_estado" in request.GET:
                q_estado = request.GET["q_estado"]
                if q_estado == "Activo":
                    reportes = Falta.objects.filter(fecha = q_fecha, activo = True, matricula__estudiante__usuario__name__icontains = q_estudiante, carga_horario__profesor__usuario__name__icontains = q_profesor).order_by("-fecha")
                    return render_to_response('disciplina_sam/reportes',{"nuevo":False, "results":reportes, "debug":q_estudiante},context)
                elif q_estado == "No activo":
                    reportes = Falta.objects.filter(fecha = q_fecha, activo = False, matricula__estudiante__usuario__name__icontains = q_estudiante, carga_horario__profesor__usuario__name__icontains = q_profesor).order_by("-fecha")
                    return render_to_response('disciplina_sam/reportes',{"nuevo":False, "results":reportes, "debug":q_estudiante},context)
            else:
                reportes = Falta.objects.filter(fecha = q_fecha, matricula__estudiante__usuario__name__icontains = q_estudiante, carga_horario__profesor__usuario__name__icontains = q_profesor).order_by("-fecha")
                return render_to_response('disciplina_sam/reportes',{"nuevo":False, "results":reportes, "debug":q_estudiante},context)
        else:
            if "q_estado" in request.GET:
                q_estado = request.GET["q_estado"]
                if q_estado == "Activo":
                    reportes = Falta.objects.filter(activo = True, matricula__estudiante__usuario__name__icontains = q_estudiante, carga_horario__profesor__usuario__name__icontains = q_profesor).order_by("-fecha")
                    return render_to_response('disciplina_sam/reportes',{"nuevo":False, "results":reportes, "debug":q_estudiante},context)
                elif q_estado == "No activo":
                    reportes = Falta.objects.filter(activo = False, matricula__estudiante__usuario__name__icontains = q_estudiante, carga_horario__profesor__usuario__name__icontains = q_profesor).order_by("-fecha")
                    return render_to_response('disciplina_sam/reportes',{"nuevo":False, "results":reportes, "debug":q_estudiante},context)
            else:
                reportes = Falta.objects.filter(matricula__estudiante__usuario__name__icontains = q_estudiante, carga_horario__profesor__usuario__name__icontains = q_profesor).order_by("-fecha")
                return render_to_response('disciplina_sam/reportes',{"nuevo":False, "results":reportes, "debug":q_estudiante},context)

    return render_to_response('disciplina_sam/reportes',{},context)
    pass


def crear(request):
    context = RequestContext(request)
    if request.method == 'POST':
        data = request.POST.copy()
        nombre_estudiante = data["matricula"]
        nombre_profesor = data["carga_horario"]
        nombre_categoria = data["categoria"]
        id_estudiante = Matricula.objects.get(estudiante__usuario__name__icontains = nombre_estudiante)
        id_profesor = Carga_Horario.objects.get(profesor__usuario__name__icontains = nombre_profesor)
        id_categoria = Categoria.objects.get(pk = nombre_categoria)
        data["matricula"] = id_estudiante.id
        data["carga_horario"] = id_profesor.id

        form = FaltaForma(data)
        if form.is_valid():
            falta = form.save()
            falta.save()
            if id_categoria.notificar_profesor:
                email_title_profesor = render_to_string('disciplina_sam/email_title_profesor.txt', {'categoria': id_categoria.nombre, "estudiante":nombre_estudiante})
                email_body_profesor = render_to_string('disciplina_sam/email_profesor.txt', {'profesor':nombre_profesor, "fecha":falta.fecha, "categoria": falta.categoria.nombre, "estudiante":nombre_estudiante, "detalle":falta.detalle})
                email_body_profesor_html = render_to_string('disciplina_sam/email_profesor.html', {'profesor':nombre_profesor, "fecha":falta.fecha, "categoria": falta.categoria.nombre, "estudiante":nombre_estudiante, "detalle":falta.detalle})
                send_mail(email_title_profesor, email_body_profesor, 'from@example.com', [id_profesor.profesor.usuario.email], html_message = email_body_profesor_html, fail_silently=True)

                email_title_representante = render_to_string('disciplina_sam/email_title_representante.txt', {'categoria': id_categoria.nombre, "estudiante":nombre_estudiante, "profesor":nombre_profesor})
                email_body_representante = render_to_string('disciplina_sam/email_representante.txt', {"representante":falta.matricula.estudiante.representante.usuario.name , 'profesor':nombre_profesor, "fecha":falta.fecha, "categoria": falta.categoria.nombre, "estudiante":nombre_estudiante, "detalle":falta.detalle})
                email_body_representante_html = render_to_string('disciplina_sam/email_representante.html', {"representante":falta.matricula.estudiante.representante.usuario.name, 'profesor':nombre_profesor, "fecha":falta.fecha, "categoria": falta.categoria.nombre, "estudiante":nombre_estudiante, "detalle":falta.detalle})
                try:
                    send_mail(email_title_representante, email_body_representante, 'from@example.com', [id_estudiante.estudiante.representante.usuario.email], html_message = email_body_representante_html, fail_silently=True)
                except:
                    pass
            if id_categoria.notificar_representante:
                email_title_representante = render_to_string('disciplina_sam/email_title_representante.txt', {'categoria': id_categoria.nombre, "estudiante":nombre_estudiante, "profesor":nombre_profesor})
                email_body_representante = render_to_string('disciplina_sam/email_representante_2.txt', {"representante":falta.matricula.estudiante.representante.usuario.name , 'profesor':nombre_profesor, "fecha":falta.fecha, "categoria": falta.categoria.nombre, "estudiante":nombre_estudiante, "detalle":falta.detalle})
                email_body_representante_html = render_to_string('disciplina_sam/email_representante_2.html', {"representante":falta.matricula.estudiante.representante.usuario.name, 'profesor':nombre_profesor, "fecha":falta.fecha, "categoria": falta.categoria.nombre, "estudiante":nombre_estudiante, "detalle":falta.detalle})
                try:
                    send_mail(email_title_representante, email_body_representante, 'from@example.com', [id_estudiante.estudiante.representante.usuario.email], html_message = email_body_representante_html, fail_silently=True)
                except:
                    pass
            return redirect(disciplina)
        else:
            print form.errors
            return render_to_response('disciplina_sam/registro',{'form':form},context)
    else:
        form=FaltaForma()
        return render_to_response('disciplina_sam/registro',{'form':form},context)

def cambiar_estado_disciplina(request, registro_id):
        registro = Falta.objects.get(pk=registro_id)
        if registro.activo is True:
            registro.activo = False
            registro.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif registro.activo is False:
            registro.activo = True
            registro.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def reportes(request):
    context = RequestContext(request)
    text = "Hello world"
    return render(request,'disciplina_sam/reportes',{'text':text})

def detalle_falta(request, falta_id):
    context = RequestContext(request)
    falta = Falta.objects.get(pk = falta_id)
    detalle_falta = Seguimiento_De_Falta.objects.filter(falta = falta_id)
    return render_to_response('disciplina_sam/detalle',{'falta':falta, 'detalle_falta':detalle_falta},context)

def crear_detalle(request, falta_id):
    falta = Falta.objects.get(pk = falta_id)
    context = RequestContext(request)
    if request.method=='POST':
        blank_form = AccionForma()
        form = AccionForma(request.POST)
        if form.is_valid():
            new_form = form.save(commit = False)
            new_form.falta_id = falta_id
            new_form.save()
            detalle_falta = Seguimiento_De_Falta.objects.filter(falta = falta_id)
            return render_to_response('disciplina_sam/crear_detalle',{'form':blank_form,'falta_id':falta_id,'falta':falta},context)
        else:
            print form.errors
            return render_to_response('disciplina_sam/crear_detalle',{'form':form,'falta_id':falta_id,'falta':falta},context)
    else:
        form=AccionForma()
        return render_to_response('disciplina_sam/crear_detalle',{'form':form,'falta_id':falta_id,'falta':falta}, context)
# Create your views here.
