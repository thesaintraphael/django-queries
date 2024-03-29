from django.urls import path
from . import views


urlpatterns = [

    path('avg', views.average_price, name='average-price'),
    path('max', views.max_and_avg, name='max-averga'),
    path('count', views.count_things, name='count'),
    path('ang', views.ann_and_agg, name='ang'),
    path('fore', views.aggreagate_for_each, name='for-each'),
    path('join', views.join_aggreagate, name='join'),
    path('sum', views.sum_pages, name='sum-pages'),
    path('filter', views.filter_ag, name='filter'),
    path('agn', views.aggregate_annotaions, name='agg-ann'),

]
