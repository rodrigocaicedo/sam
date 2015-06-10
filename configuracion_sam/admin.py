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
admin.site.register(Clase)
admin.site.register(Estudiante)
admin.site.register(Profesor)
admin.site.register(Matricula)
admin.site.register(Materia)
admin.site.register(Carga_Horario)
admin.site.register(Representante)
# Register your models here.
