from django.urls import path
from django.conf.urls import url
from .views import *
from . import views



urlpatterns = [
    url(r'^$', views.UploadView.as_view(), name='UploadView'),
    url(r'^upload/', views.UploadView.as_view(), name='UploadView'),
    url(r'^analysis/', views.analysis.as_view(), name="analysis"),
    url(r'^group/', views.group.as_view(), name="group")
    #url(r'^import_sheet/', views.import_sheet, name="import_sheet"),
    #url(r'^main/', views.MainPage, name="Main page")

]