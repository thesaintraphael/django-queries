from django.urls import path
from . import views


urlpatterns = [

    path('', views.q_and_or, name='q_objects'),
    path('nested', views.q2, name='nested'),
    path('search', views.search, name='search'),

]
