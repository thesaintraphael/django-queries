from django.urls import path
from . import views


urlpatterns = [

    path('select', views.select_related, name='select'),
    path('pre', views.prefetch_filter, name='pre'),
    path('pre-filter', views.prefetch_filter, name='pre-filter'),
    path('filter-pre', views.filter_prefect, name='filter'),
    path('only', views.using_only, name='filter'),

]
 