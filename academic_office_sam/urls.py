__author__ = 'Rodrigo'
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from academic_office_sam import views

urlpatterns = patterns('',
    url(r'^registro/$',views.register_grade.as_view(), name='registro'),
    url(r'^registro/(?P<grade_id>\d+)/$',views.create_grade, name='create_grade'),
)
urlpatterns += staticfiles_urlpatterns()
