__author__ = 'Rodrigo'
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from academic_office_sam import views

urlpatterns = patterns('',
    url(r'^$',views.index, name='index'),
    url(r'^regsitro/$',views.register_grade, name='registro'),
)
urlpatterns += staticfiles_urlpatterns()
