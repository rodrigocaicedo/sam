from django.shortcuts import render, render_to_response, redirect, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from datetime import date


from requisicion_sam.models import Pedido_Item, Aprobacion_Item
from requisicion_sam.forms import ItemForm, AprobacionForm
from configuracion_sam.models import Profesor, Pensum

def index(request):
    context = RequestContext(request)
    profesor = request.user.pk or None
    schoolyear = request.session["schoolyear"]
    pedidos = Aprobacion_Item.objects.filter(item__materia__grupo__periodo_lectivo__name__icontains=schoolyear,
                                             item__profesor__usuario__pk=profesor,
                                             fecha_entrega=None).order_by("pk") or None
    return render_to_response('requisicion_sam/index',{"pedidos":pedidos}, context)


def add_item(request):
    context = RequestContext(request)
    schoolyear = request.session["schoolyear"]
    user = request.user.pk
    profesor = Profesor.objects.get(usuario__pk = user)
    today = date.today()
    if request.method=="POST":
        form = ItemForm(request.POST, request.FILES)
        form.fields["materia"].queryset=Pensum.objects.filter(profesor__usuario__pk=user, grupo__periodo_lectivo__name__icontains=schoolyear)
        if form.is_valid():
            item=form.save(commit=False)
            item.profesor=profesor
            item.fecha=today
            item.save()
            nueva_aprobacion = Aprobacion_Item(item=item)
            nueva_aprobacion.save()
            return redirect(index)
        else:
            print form.errors
            return render_to_response("requisicion_sam/nuevo",{"form":form}, context)
    else:
        form=ItemForm()
        form.fields["materia"].queryset=Pensum.objects.filter(profesor__usuario__pk=user, grupo__periodo_lectivo__name__icontains=schoolyear)
        return render_to_response("requisicion_sam/nuevo",{"form":form}, context)


def add_another_item(request):
    context = RequestContext(request)
    schoolyear = request.session["schoolyear"]
    user = request.user.pk
    profesor = Profesor.objects.get(usuario__pk = user)
    today = date.today()
    if request.method=="POST":
        form = ItemForm(request.POST, request.FILES)
        form.fields["materia"].queryset=Pensum.objects.filter(profesor__usuario__pk=user, grupo__periodo_lectivo__name__icontains=schoolyear)
        if form.is_valid():
            item=form.save(commit=False)
            item.profesor=profesor
            item.fecha=today
            item.save()
            nueva_aprobacion = Aprobacion_Item(item=item)
            nueva_aprobacion.save()
            form_nueva=ItemForm()
            form_nueva.fields["materia"].queryset=Pensum.objects.filter(profesor__usuario__pk=user, grupo__periodo_lectivo__name__icontains=schoolyear)
            return render_to_response("requisicion_sam/nuevo",{"form":form_nueva}, context)
        else:
            print form.errors
            return render_to_response("requisicion_sam/nuevo",{"form":form}, context)
    else:
        form=ItemForm()
        form.fields["materia"].queryset=Pensum.objects.filter(profesor__usuario__pk=user, grupo__periodo_lectivo__name__icontains=schoolyear)
        return render_to_response("requisicion_sam/nuevo",{"form":form}, context)

def edit_item(request, item):
    context = RequestContext(request)
    schoolyear = request.session["schoolyear"]
    user = request.user.pk
    profesor = Profesor.objects.get(usuario__pk = user)
    today = date.today()
    item = Pedido_Item.objects.get(pk = item)
    if request.method=="POST":
        data = request.POST.copy()
        form = ItemForm(request.POST, request.FILES, instance=item)
        form.fields["materia"].queryset=Pensum.objects.filter(profesor__usuario__pk=user, grupo__periodo_lectivo__name__icontains=schoolyear)
        if form.is_valid():
            item2=form.save(commit=False)
            item2.profesor=profesor
            item2.fecha=today
            item2.save()
            return redirect(index)
        else:
            print form.errors
            return render_to_response("requisicion_sam/nuevo",{"form":form, "item":item}, context)
    else:
        form=ItemForm(instance = item)
        form.fields["materia"].queryset=Pensum.objects.filter(profesor__usuario__pk=user, grupo__periodo_lectivo__name__icontains=schoolyear)
        return render_to_response("requisicion_sam/editar",{"form":form, "item":item}, context)

def delete_item(request, item):
    item = Pedido_Item.objects.get(pk = item)
    aprobacion = Aprobacion_Item.objects.get(item = item)
    aprobacion.delete()
    item.delete()
    return redirect(index)

