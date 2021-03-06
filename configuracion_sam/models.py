from django.db import models

from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password,False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email and password are required. Other fields are optional.
    """
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=False)
    last_name = models.CharField(_('last name'), max_length=30, blank=False)
    name = models.CharField(_('name'),max_length=61, blank=False)
    birthdate = models.DateField(_('birth date'), null=True)
    user_photo = models.FileField(upload_to = ".")
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])


class Periodo_Lectivo(models.Model):
    name = models.CharField(max_length=9, unique=True)
    inicio = models.DateField()
    fin = models.DateField()

    def __unicode__(self):
        return self.name


class Subperiodo(models.Model):
    periodo_lectivo = models.ForeignKey('Periodo_Lectivo')
    name = models.CharField(max_length = 128) 
    inicio = models.DateField()
    fin = models.DateField()

    class Meta:
        unique_together = ('inicio','fin',)
        
    def __unicode__(self):
        return self.periodo_lectivo.name+" "+self.name

class Estructura_Subperiodo(models.Model):
    subperiodo = models.ForeignKey("Subperiodo")
    name = models.TextField(max_length = 30)
    affecting_fraction = models.FloatField()
    inicio = models.DateField()
    fin = models.DateField()

    class Meta:
        unique_together = ("subperiodo","name")

    def __unicode__(self):
        return self.subperiodo.periodo_lectivo.name + " " + self.subperiodo.name + " " + self.name


class Clase(models.Model):

    clase_name = models.CharField(max_length=20)
    periodo_lectivo = models.ForeignKey('Periodo_Lectivo')
    nivel = models.IntegerField()
    nombre_ministerio = models.CharField(max_length=20)

    class Meta:
        unique_together = ('clase_name','periodo_lectivo',)

    def __unicode__(self):
       return self.clase_name + " " + self.periodo_lectivo.name


class Representante(models.Model):
    usuario = models.OneToOneField("CustomUser")

    def __unicode__(self):
        return self.usuario.name


class Estudiante(models.Model):
    usuario = models.OneToOneField('CustomUser')
    representante = models.ForeignKey("Representante")

    def __unicode__(self):
        return self.usuario.name


class Profesor(models.Model):
    usuario = models.OneToOneField("CustomUser")

    def __unicode__(self):
        return self.usuario.name

class Coordinador_Seccion(models.Model):
    usuario = models.OneToOneField('CustomUser')

    def __unicode__(self):
        return self.usuario.name

class Coordinador_Area_Academica(models.Model):
    usuario = models.OneToOneField('CustomUser')

    def __unicode__(self):
        return self.usuario.name


class Matricula(models.Model):

    ordinaria = "OR"
    extraordinaria = "EX"
    tipo = (
        (ordinaria, "Ordinaria"),
        (extraordinaria, "Extraordinaria"),
        )

    A = "A"
    B = "B"
    C = "C"
    paralelo = (
        (A, "A"),
        (B, "B"),
        (C, "C"),
    )


    estudiante = models.ForeignKey('Estudiante')
    clase = models.ForeignKey('Clase')
    paralelo = models.CharField(max_length=1,
                                choices=paralelo,
                                default=A)
    fecha = models.DateField()
    tipo = models.CharField(max_length = 2,
                            choices = tipo,
                            default = ordinaria)
    activo = models.BooleanField(default=True)

    class Meta:
        unique_together = ('estudiante', 'clase', )

    def __unicode__(self):
        return self.clase.periodo_lectivo.name + " " +self.estudiante.usuario.get_full_name()


class Malla_Curricular(models.Model):

    cualitativa = "C"
    cuantitativa = "Q"
    destrezas = "D"
    tipo = (
        (cualitativa, "Cualitativa"),
        (cuantitativa, "Cuantitativa"),
        (destrezas, "Por Destrezas")
    )

    clase = models.ForeignKey('Clase')
    nombre_materia = models.CharField(max_length = 20)
    tipo = models.CharField(max_length = 1,
                            choices = tipo,
                            default = cuantitativa)

    class Meta:
        unique_together = ('clase', 'nombre_materia',)

    def __unicode__(self):
        return self.nombre_materia + " " + self.clase.clase_name


class Seccion(models.Model):
    nombre = models.TextField(max_length=40)

    def __unicode__(self):
        return self.nombre


class Coordinadores_De_Seccion(models.Model):
    seccion = models.ForeignKey('Seccion')
    coordinadores = models.ManyToManyField('Coordinador_Seccion')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default = True)

    class Meta:
        unique_together=('seccion','activo',)

    def __unicode__(self):
        return self.seccion.nombre


class Grupo(models.Model):

    periodo_lectivo = models.ForeignKey('Periodo_Lectivo')
    nombre = models.CharField(max_length = 20)
    descripcion = models.TextField()
    seccion = models.ForeignKey('Seccion')

    class Meta:
        unique_together = ('periodo_lectivo', 'nombre',)

    def __unicode__(self):
        return self.nombre + " " + self.periodo_lectivo.name


class Inscripcion_Grupo(models.Model):
    matricula = models.ForeignKey('Matricula')
    grupo = models.ForeignKey('Grupo')
    inicio = models.DateField()
    fin = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        unique_together = ('matricula','grupo','activo',)

    def __unicode__(self):
        return self.matricula.estudiante.usuario.name + " - " + self.grupo.nombre


class Area_Academica(models.Model):
    nombre=models.TextField(max_length = 40)
    coordinador = models.ForeignKey('Coordinador_Area_Academica')
    fecha_inicio=models.DateField()
    fecha_fin=models.DateField(null=True,blank=True)
    activo=models.BooleanField(default=True)

    class Meta:
        unique_together=('nombre','activo',)

    def __unicode__(self):
        return self.nombre

class Coordinadores_De_Area_Academica(models.Model):
    area_academica = models.ForeignKey('Area_Academica')
    coordinador = models.ForeignKey('Coordinador_Area_Academica')
    grupos = models.ManyToManyField('Grupo')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default = True)

    class Meta:
        unique_together=('area_academica','coordinador','activo',)

    def __unicode__(self):
        return self.seccion.nombre + " - " + self.coordinador.usuario.name


class Materia(models.Model):
    nombre = models.TextField(max_length = 30)
    area_academica = models.ForeignKey('Area_Academica')
    periodos_lectivos=models.ManyToManyField('Periodo_Lectivo')

    class Meta:
        unique_together=('nombre','area_academica',)

    def __unicode__(self):
        return self.nombre + " - " + self.area_academica.nombre


class Pensum(models.Model):

    cualitativa = "C"
    cuantitativa = "Q"
    destrezas = "D"
    tipo = (
        (cualitativa, "Cualitativa"),
        (cuantitativa, "Cuantitativa"),
        (destrezas, "Por Destrezas")
    )

    grupo = models.ForeignKey('Grupo')
    materia = models.ForeignKey('Materia')
    profesor = models.ForeignKey('Profesor')
    evaluacion = models.CharField(max_length = 1,
                            choices = tipo,
                            default = cuantitativa)
    inicio = models.DateField()
    fin = models.DateField(null=True, blank=True)
    activo = models.BooleanField()

    class Meta:
        unique_together = ('grupo', 'materia', 'activo',)

    def __unicode__(self):
        return self.grupo.nombre + " " + self.materia.nombre + " " + self.profesor.usuario.name

