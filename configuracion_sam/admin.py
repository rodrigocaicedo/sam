from django.contrib import admin
from configuracion_sam.models import *

from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from configuracion_sam.forms import CustomUserChangeForm, CustomUserCreationForm

class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name','last_name','name','password1', 'password2')}
        ),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Periodo_Lectivo)
admin.site.register(Subperiodo)
admin.site.register(Estructura_Subperiodo)
admin.site.register(Clase)
admin.site.register(Representante)
admin.site.register(Estudiante)
admin.site.register(Coordinador_Area_Academica)
admin.site.register(Coordinador_Seccion)
admin.site.register(Coordinadores_De_Area_Academica)
admin.site.register(Coordinadores_De_Seccion)
admin.site.register(Area_Academica)
admin.site.register(Seccion)
admin.site.register(Profesor)
admin.site.register(Matricula)
admin.site.register(Malla_Curricular)
admin.site.register(Grupo)
admin.site.register(Inscripcion_Grupo)
admin.site.register(Materia)
admin.site.register(Pensum)




# Register your models here.
