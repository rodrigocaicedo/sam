from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.template.loader import render_to_string

from datetime import date, timedelta

from configuracion_sam.models import Matricula, Carga_Horario, Clase, Periodo_Lectivo, Estructura_Subperiodo

from disciplina_sam.models import Falta, Seguimiento_De_Falta, Categoria
from disciplina_sam.forms import FaltaForma, AccionForma, CategoriaForm

import json

def ac_estudiante(request):
    schoolyear = request.session['schoolyear']
    if request.is_ajax():
        q = request.GET.get('term', '')
        drugs = Matricula.objects.filter(estudiante__usuario__name__icontains=q, estudiante__usuario__is_active=True,
                                         clase__periodo_lectivo__name__icontains=schoolyear)[:20]
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
    schoolyear = request.session['schoolyear']
    if request.is_ajax():
        q = request.GET.get('term', '')
        drugs = Carga_Horario.objects.filter(profesor__usuario__name__icontains=q, activo=True,
                                             materia__clase__periodo_lectivo__name__icontains=schoolyear)[:20]
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
    schoolyear = request.session['schoolyear']
    if request.is_ajax():
        q = request.GET.get('term', '')
        drugs = Categoria.objects.filter(nombre__icontains=q, periodo_lectivo__name__icontains=schoolyear)[:20]
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
    context = {'clases': clases}
    return render(request, 'disciplina_sam/index', context)

def disciplina(request):
    schoolyear = request.session["schoolyear"]
    ultimos_registros = Falta.objects.filter(activo=True,
                                             matricula__clase__periodo_lectivo__name__icontains=schoolyear).order_by(
        '-fecha')
    context = {'ultimos_registros': ultimos_registros}
    return render(request, 'disciplina_sam/disciplina', context)

def busqueda_disciplina(request):
    schoolyear = request.session["schoolyear"]
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
                    reportes = Falta.objects.filter(matricula__clase__periodo_lectivo__name=schoolyear, fecha=q_fecha,
                                                    activo=True,
                                                    matricula__estudiante__usuario__name__icontains=q_estudiante,
                                                    carga_horario__profesor__usuario__name__icontains=q_profesor).order_by(
                        "-fecha")
                    return render_to_response('disciplina_sam/reportes',
                                              {"nuevo": False, "results": reportes, "debug": q_estudiante}, context)
                elif q_estado == "No activo":
                    reportes = Falta.objects.filter(matricula__clase__periodo_lectivo__name=schoolyear, fecha=q_fecha,
                                                    activo=False,
                                                    matricula__estudiante__usuario__name__icontains=q_estudiante,
                                                    carga_horario__profesor__usuario__name__icontains=q_profesor).order_by(
                        "-fecha")
                    return render_to_response('disciplina_sam/reportes',
                                              {"nuevo": False, "results": reportes, "debug": q_estudiante}, context)
            else:
                reportes = Falta.objects.filter(matricula__clase__periodo_lectivo__name=schoolyear, fecha=q_fecha,
                                                matricula__estudiante__usuario__name__icontains=q_estudiante,
                                                carga_horario__profesor__usuario__name__icontains=q_profesor).order_by(
                    "-fecha")
                return render_to_response('disciplina_sam/reportes',
                                          {"nuevo": False, "results": reportes, "debug": q_estudiante}, context)
        else:
            if "q_estado" in request.GET:
                q_estado = request.GET["q_estado"]
                if q_estado == "Activo":
                    reportes = Falta.objects.filter(matricula__clase__periodo_lectivo__name=schoolyear, activo=True,
                                                    matricula__estudiante__usuario__name__icontains=q_estudiante,
                                                    carga_horario__profesor__usuario__name__icontains=q_profesor).order_by(
                        "-fecha")
                    return render_to_response('disciplina_sam/reportes',
                                              {"nuevo": False, "results": reportes, "debug": q_estudiante}, context)
                elif q_estado == "No activo":
                    reportes = Falta.objects.filter(matricula__clase__periodo_lectivo__name=schoolyear, activo=False,
                                                    matricula__estudiante__usuario__name__icontains=q_estudiante,
                                                    carga_horario__profesor__usuario__name__icontains=q_profesor).order_by(
                        "-fecha")
                    return render_to_response('disciplina_sam/reportes',
                                              {"nuevo": False, "results": reportes, "debug": q_estudiante}, context)
            else:
                reportes = Falta.objects.filter(matricula__clase__periodo_lectivo__name=schoolyear,
                                                matricula__estudiante__usuario__name__icontains=q_estudiante,
                                                carga_horario__profesor__usuario__name__icontains=q_profesor).order_by(
                    "-fecha")
                return render_to_response('disciplina_sam/reportes',
                                          {"nuevo": False, "results": reportes, "debug": q_estudiante}, context)

    return render_to_response('disciplina_sam/reportes', {}, context)
    pass

def crear(request):
    schoolyear = request.session['schoolyear']
    context = RequestContext(request)
    if request.method == 'POST':
        data = request.POST.copy()
        nombre_estudiante = data["matricula"]
        nombre_profesor = data["carga_horario"]
        nombre_categoria = data["categoria"]
        id_estudiante = Matricula.objects.get(estudiante__usuario__name__icontains=nombre_estudiante,
                                              clase__periodo_lectivo__name=schoolyear)
        id_profesor = Carga_Horario.objects.get(profesor__usuario__name__icontains=nombre_profesor,
                                                materia__clase__periodo_lectivo__name=schoolyear)
        id_categoria = Categoria.objects.get(pk=nombre_categoria, periodo_lectivo__name=schoolyear)
        data["matricula"] = id_estudiante.id
        data["carga_horario"] = id_profesor.id

        form = FaltaForma(data)
        if form.is_valid():
            falta = form.save()
            falta.save()
            usar_parcial = falta.categoria.patrones_en_parcial
            usar_periodo = falta.categoria.patrones_en_periodo
            if id_categoria.notificar_profesor:
                email_title_profesor = render_to_string('disciplina_sam/email_title_profesor.txt',
                                                        {'categoria': id_categoria.nombre,
                                                         "estudiante": nombre_estudiante})
                email_body_profesor = render_to_string('disciplina_sam/email_profesor.txt',
                                                       {'profesor': nombre_profesor, "fecha": falta.fecha,
                                                        "categoria": falta.categoria.nombre,
                                                        "estudiante": nombre_estudiante, "detalle": falta.detalle})
                email_body_profesor_html = render_to_string('disciplina_sam/email_profesor.html',
                                                            {'profesor': nombre_profesor, "fecha": falta.fecha,
                                                             "categoria": falta.categoria.nombre,
                                                             "estudiante": nombre_estudiante, "detalle": falta.detalle})
                send_mail(email_title_profesor, email_body_profesor, 'from@example.com',
                          [id_profesor.profesor.usuario.email], html_message=email_body_profesor_html,
                          fail_silently=True)

                email_title_representante = render_to_string('disciplina_sam/email_title_representante.txt',
                                                             {'categoria': id_categoria.nombre,
                                                              "estudiante": nombre_estudiante,
                                                              "profesor": nombre_profesor})
                email_body_representante = render_to_string('disciplina_sam/email_representante.txt', {
                    "representante": falta.matricula.estudiante.representante.usuario.name, 'profesor': nombre_profesor,
                    "fecha": falta.fecha, "categoria": falta.categoria.nombre, "estudiante": nombre_estudiante,
                    "detalle": falta.detalle})
                email_body_representante_html = render_to_string('disciplina_sam/email_representante.html', {
                    "representante": falta.matricula.estudiante.representante.usuario.name, 'profesor': nombre_profesor,
                    "fecha": falta.fecha, "categoria": falta.categoria.nombre, "estudiante": nombre_estudiante,
                    "detalle": falta.detalle})

                try:
                    send_mail(email_title_representante, email_body_representante, 'from@example.com',
                              [id_estudiante.estudiante.representante.usuario.email],
                              html_message=email_body_representante_html, fail_silently=True)
                except:
                    pass
            if id_categoria.notificar_representante:
                email_title_representante = render_to_string('disciplina_sam/email_title_representante.txt',
                                                             {'categoria': id_categoria.nombre,
                                                              "estudiante": nombre_estudiante,
                                                              "profesor": nombre_profesor})
                email_body_representante = render_to_string('disciplina_sam/email_representante_2.txt', {
                    "representante": falta.matricula.estudiante.representante.usuario.name, 'profesor': nombre_profesor,
                    "fecha": falta.fecha, "categoria": falta.categoria.nombre, "estudiante": nombre_estudiante,
                    "detalle": falta.detalle})
                email_body_representante_html = render_to_string('disciplina_sam/email_representante_2.html', {
                    "representante": falta.matricula.estudiante.representante.usuario.name, 'profesor': nombre_profesor,
                    "fecha": falta.fecha, "categoria": falta.categoria.nombre, "estudiante": nombre_estudiante,
                    "detalle": falta.detalle})

                try:
                    send_mail(email_title_representante, email_body_representante, 'from@example.com',
                              [id_estudiante.estudiante.representante.usuario.email],
                              html_message=email_body_representante_html, fail_silently=True)
                except:
                    pass

            if usar_parcial == True:
                parcial_actual = Estructura_Subperiodo.objects.get(inicio__lte=date.today(), fin__gte=date.today())
                eventos_parcial = falta.categoria.eventos_parcial
                eventos_cantidad_parcial = Falta.objects.filter(matricula=falta.matricula, categoria=falta.categoria,
                                                                fecha__range=[parcial_actual.inicio,
                                                                             parcial_actual.fin])
                if eventos_cantidad_parcial.count() >= eventos_parcial:
                    email_title_dcce = render_to_string("disciplina_sam/email_title_dcce.txt",
                                                        {"categoria": id_categoria.nombre,
                                                         "estudiante": nombre_estudiante})
                    email_body_dcce = render_to_string("disciplina_sam/email_dcce.txt",
                                                       {"parcial": parcial_actual.name,
                                                        "estudiante": nombre_estudiante,
                                                        "eventos": eventos_cantidad_parcial.count(),
                                                        "categoria": falta.categoria.nombre})
                    email_body_dcce_html = render_to_string("disciplina_sam/email_dcce.html",
                                                            {"parcial": parcial_actual.name,
                                                             "subperiodo": parcial_actual.subperiodo.name,
                                                             "estudiante": nombre_estudiante,
                                                             "eventos": eventos_cantidad_parcial.count(),
                                                             "categoria": falta.categoria.nombre})
                    try:
                        send_mail(email_title_dcce, email_body_dcce, 'dcce@montebelloacademy.org',
                                  ["rodrigo@montebelloacademy.org"], html_message=email_body_dcce_html,
                                  fail_silently=False)
                    except:
                        pass
                else:
                    pass
            else:
                pass

            if usar_periodo == True:
                periodo_patron = falta.categoria.periodo_patron
                eventos_patron = falta.categoria.eventos_patron
                end_date = date.today()
                start_date = end_date - timedelta(days=periodo_patron)
                eventos_cantidad = Falta.objects.filter(matricula=falta.matricula, categoria=falta.categoria,
                                                        fecha__range=[start_date, end_date])

                if eventos_cantidad.count() >= eventos_patron:
                    email_title_dcce = render_to_string('disciplina_sam/email_title_dcce.txt',
                                                        {'categoria': id_categoria.nombre,
                                                         "estudiante": nombre_estudiante})
                    email_body_dcce = render_to_string('disciplina_sam/email_dcce_2.txt',
                                                       {"eventos": eventos_cantidad.count(), "periodo": periodo_patron,
                                                        "categoria": falta.categoria.nombre,
                                                        "estudiante": nombre_estudiante})
                    email_body_dcce_html = render_to_string('disciplina_sam/email_dcce_2.html',
                                                            {"eventos": eventos_cantidad.count(),
                                                             "periodo": periodo_patron,
                                                             "categoria": falta.categoria.nombre,
                                                             "estudiante": nombre_estudiante})
                    try:
                        send_mail(email_title_dcce, email_body_dcce, 'from@example.com',
                                  ["rodrigo@montebelloacademy.org"], html_message=email_body_dcce_html,
                                  fail_silently=False)
                    except:
                        pass
                else:
                    pass
            else:
                pass

            return redirect(disciplina)

        else:
            print form.errors
            return render_to_response('disciplina_sam/registro', {'form': form}, context)
    else:
        form = FaltaForma()
        form.fields["categoria"].queryset = Categoria.objects.filter(periodo_lectivo__name__icontains=schoolyear)
        return render_to_response('disciplina_sam/registro', {'form': form}, context)

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
    return render(request, 'disciplina_sam/reportes', {'text': text})

def detalle_falta(request, falta_id):
    context = RequestContext(request)
    falta = Falta.objects.get(pk=falta_id)
    detalle_falta = Seguimiento_De_Falta.objects.filter(falta=falta_id)
    return render_to_response('disciplina_sam/detalle', {'falta': falta, 'detalle_falta': detalle_falta}, context)

def crear_detalle(request, falta_id):
    falta = Falta.objects.get(pk=falta_id)
    context = RequestContext(request)
    if request.method == 'POST':
        blank_form = AccionForma()
        form = AccionForma(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.falta_id = falta_id
            new_form.save()
            detalle_falta = Seguimiento_De_Falta.objects.filter(falta=falta_id)
            return render_to_response('disciplina_sam/crear_detalle',
                                      {'form': blank_form, 'falta_id': falta_id, 'falta': falta,
                                       "detalle_falta": detalle_falta}, context)
        else:
            print form.errors
            detalle_falta = Seguimiento_De_Falta.objects.filter(falta=falta_id)
            return render_to_response('disciplina_sam/crear_detalle',
                                      {'form': form, 'falta_id': falta_id, 'falta': falta,
                                       "detalle_falta": detalle_falta}, context)
    else:
        form = AccionForma()
        detalle_falta = Seguimiento_De_Falta.objects.filter(falta=falta_id)
        return render_to_response('disciplina_sam/crear_detalle',
                                  {'form': form, 'falta_id': falta_id, 'falta': falta, "detalle_falta": detalle_falta},
                                  context)

def categorias(request):
    context = RequestContext(request)
    schoolyear = request.session["schoolyear"]
    categorias = Categoria.objects.filter(periodo_lectivo__name=schoolyear)

    if request.method == "POST":
        data = request.POST.copy()
        periodo_lectivo_actual = Periodo_Lectivo.objects.get(name=schoolyear)
        # data["periodo_lectivo"] = periodo_lectivo_actual.id
        #form = CategoriaForm(data)
        form = CategoriaForm(request.POST)
        if form.is_valid():
            nueva_categoria = form.save(commit=False)
            nueva_categoria.periodo_lectivo = periodo_lectivo_actual
            if nueva_categoria.patrones_en_parcial ==True:
                if nueva_categoria.eventos_parcial <=0:

                    print form.errors
                    return render_to_response("disciplina_sam/categoria", {"categorias": categorias, "form": form}, context)
                else:
                    pass
            else:
                pass

            if nueva_categoria.patrones_en_periodo ==True:
                if nueva_categoria.eventos_patron <=0:

                    print form.errors
                    return render_to_response("disciplina_sam/categoria", {"categorias": categorias, "form": form}, context)
                else:
                    pass
                if nueva_categoria.periodo_patron <=0:

                    print form.errors
                    return render_to_response("disciplina_sam/categoria", {"categorias": categorias, "form": form}, context)
                else:
                    pass

            else:
                pass

            nueva_categoria.save()
            form = CategoriaForm()

            return render_to_response("disciplina_sam/categoria", {"categorias": categorias, "form": form}, context)
        else:
            print form.errors
            return render_to_response("disciplina_sam/categoria", {"categorias": categorias, "form": form}, context)
    else:
        form = CategoriaForm()
        return render_to_response("disciplina_sam/categoria", {"categorias": categorias, "form": form}, context)


# Create your views here.
