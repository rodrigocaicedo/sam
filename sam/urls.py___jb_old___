from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from configuracion_sam.views import set_schoolyear
from django import http
from configuracion_sam import views as conf_sam_views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sam.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^configuracion/', include('configuracion_sam.urls')),
    url(r'^faltas/', include('disciplina_sam.urls')),
    url(r'^secretaria/', include("academic_office_sam.urls")),
    url(r'^accounts/login/$', auth_views.login),
    url(r'^accounts/logout/$', conf_sam_views.logout_view),
    url(r'^estudiante/(?P<estudiante>[-\w]+)/all_json_materias/$', 'all_json_materias'),
    url(r'^periodo_lectivo/(?P<schoolyear>[0-9,-]{9})/$',set_schoolyear, name='set_schoolyear'),
)

