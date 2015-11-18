from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#from configuracion_sam.views import set_schoolyear
from disciplina_sam import views

urlpatterns = patterns('',
    url(r'^$',views.index, name='index'),
    url(r'^ac_estudiante/', views.ac_estudiante, name='ac_estudiante'),
    url(r'^ac_profesor/', views.ac_profesor, name='ac_profesor'),
    url(r'^ac_profesor_busqueda/', views.ac_profesor_busqueda, name='ac_profesor_busqueda'),
    url(r'^ac_categoria/', views.ac_categoria, name='ac_categoria'),
    url(r'^disciplina/$',views.disciplina, name='disciplina'),
    url(r'^disciplina/estado/(?P<registro_id>\d+)/$',views.cambiar_estado_disciplina, name='cambiar_estado_disciplina'),
    url(r'^disciplina/busqueda/$',views.busqueda_disciplina, name='busqueda_disciplina'),
    url(r'^disciplina/registro/$',views.crear, name='registro_disciplina'),
    url(r'^disciplina/editar/(?P<falta_id>\d+)/$', views.editar, name='editar'),
    #url(r'^reportes/$',views.reportes, name='reportes'),
    url(r'^disciplina/detalle/(?P<falta_id>\d+)/$', views.detalle_falta, name='detalle_falta'),
    url(r'^disciplina/detalle/crear/(?P<falta_id>\d+)/$', views.crear_detalle, name='crear_detalle'),
    url(r'^configuracion/$',views.categorias, name='categorias'),
    url(r'^configuracion/editar/(?P<categoria_id>\d+)/$',views.editar_categorias, name='editar_categorias'),
    url(r'^configuracion/borrar/(?P<categoria_id>\d+)/$',views.borrar_categorias, name='borrar_categorias'),
)
urlpatterns += staticfiles_urlpatterns()
