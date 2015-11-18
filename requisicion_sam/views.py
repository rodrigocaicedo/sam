from django.shortcuts import render, render_to_response, redirect, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse


from requisicion_sam.models import Requisicion, Item_Request
from requisicion_sam.forms import RequisicionForm, ItemForm

def create_request(request):
    context = RequestContext(request)
    schoolyear = request.session["schoolyear"]
    form = RequisicionForm()
    if request.method == "POST":
        form = RequisicionForm(request.POST)
        if form.is_valid():
            requisicion_object = form.save()
            requisiciones = Requisicion.objects.all().order_by("fecha")
            return HttpResponseRedirect(reverse(add_item, args=(requisicion_object.pk,)))

        else:
            print form.errors
            return render_to_response("requisicion_sam/create", {"form":form}, context)
    else:
        return render_to_response("requisicion_sam/create", {"form":form}, context)

def add_item(request, requisicion_id):
    context = RequestContext(request)
    items = Item_Request.objects.filter(Requisicion = requisicion_id)
    requisicion_object = Requisicion.objects.get(pk = requisicion_id)
    form = ItemForm()
    if request.method == "POST":
        data = request.POST.copy()
        data["Requisicion"] = requisicion_object.id
        form = ItemForm(data)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(add_item, args=(requisicion_object.pk,)))

        else:
            print form.errors
            return render_to_response("requisicion_sam/add_item", {"form":form, "requisicion_id":requisicion_object.pk }, context)
    else:
        return render_to_response("requisicion_sam/add_item", {"form":form, "requisicion_id":requisicion_object.pk }, context)

def index(request):
    context = RequestContext(request)
    requisiciones = Requisicion.objects.all().order_by("fecha")
    return render_to_response("requisicion_sam/index", {"requisiciones":requisiciones}, context)

# Create your views here.
