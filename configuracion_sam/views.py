from configuracion_sam.models import Periodo_Lectivo
from django.http import HttpResponseRedirect
from django.contrib.auth import logout

def set_schoolyear(request,schoolyear):
    current_schoolyear = Periodo_Lectivo.objects.get(name = schoolyear)
    request.session['schoolyear'] = current_schoolyear.name
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))