from configuracion_sam.models import Periodo_Lectivo
from datetime import date

def schoolyear_list(request):

	if request.session.has_key("schoolyear"):
		pass
	else:

		today = date.today()
		if Periodo_Lectivo.objects.filter(inicio__lte=today, fin__gte=today).exists():
			current_schoolyear = Periodo_Lectivo.objects.get(inicio__lte=today, fin__gte=today)
			request.session['schoolyear'] = current_schoolyear.name
		else:
			request.session['schoolyear'] = "Seleccione..."

	return {'schoolyears':Periodo_Lectivo.objects.all()}

