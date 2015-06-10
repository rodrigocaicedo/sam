from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from configuracion_sam.models import Matricula, Carga_Horario, Clase

from disciplina_sam.models import Falta, Seguimiento_De_Falta, Categoria
from disciplina_sam.forms import FaltaForma, AccionForma

import json

def ac_estudiante(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        drugs = Matricula.objects.filter(estudiante__usuario__name__icontains = q )[:20]
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
        drugs = Carga_Horario.objects.filter(profesor__usuario__name__icontains = q )[:20]
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
    ultimas_faltas = Falta.objects.all().order_by('fecha')
    context = {'ultimas_faltas':ultimas_faltas}
    return render(request,'disciplina_sam/disciplina',context)

def busqueda_disciplina(request):
    pass


def crear(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = FaltaForma(request.POST)
        if form.is_valid():
            falta = form.save()
            falta.save()
            return redirect(index)    
        else:
            print form.errors
            return render_to_response('disciplina_sam/registro',{'form':form},context)
    else:
        form=FaltaForma()
        return render_to_response('disciplina_sam/registro',{'form':form},context)

def reportes(request):
    context = RequestContext(request)
    text = "Hello world"
    return render(request,'configuracion_sam/reportes',{'text':text})    

def detalle_falta(request, falta_id):
    context = RequestContext(request)
    falta = Falta.objects.get(pk = falta_id)
#    detalle_falta = Seguimiento_De_Falta.objects.get(falta = falta_id)
    detalle_falta = Seguimiento_De_Falta.objects.filter(falta = falta_id)
    return render_to_response('configuracion_sam/detalle',{'falta':falta, 'detalle_falta':detalle_falta},context)

def crear_detalle(request, falta_id):
    falta = Falta.objects.get(pk = falta_id)
    context = RequestContext(request)
    if request.method=='POST':
        form = AccionForma(request.POST)
        if form.is_valid():
            accion =  Falta.objects.get(pk = falta_id)
            form = AccionForma(request.POST,instance=accion)
            form.save()
            return render_to_response('configuracion_sam/crear_detalle',{'form':form,'falta_id':falta_id,'falta':falta},context)
        else:
            print form.errors
            return render_to_response('configuracion_sam/crear_detalle',{'form':form,'falta_id':falta_id,'falta':falta},context)
    else:
        form=AccionForma()
        return render_to_response('configuracion_sam/crear_detalle',{'form':form,'falta_id':falta_id,'falta':falta}, context)
# Create your views here.
