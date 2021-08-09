from django.urls import path
from . import views


urlpatterns = [

    path('avg', views.average_price, name='average-price'),
    path('max', views.max_and_avg, name='max-averga'),
    path('count', views.count_things, name='count'),
    path('ang', views.ann_and_agg, name='ang'),

]
