from django.urls import path
from django.conf.urls import include, url
from . import views

urlpatterns = [
    path('',views.datascrap,name = 'datascrap'),
    path('dataframe/',views.datascrap_run,name = 'dataframe'),
    path('plot_csv/',views.plot_csv, name='plot_csv'),
    path('plot_csv/job',views.plot_csv, name='job'),

]