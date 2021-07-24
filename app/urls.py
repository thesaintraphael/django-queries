from django.urls import path
from . import views


urlpatterns = [

    path('', views.q_and_or, name='q_objects'),
    path('nested', views.nested_q, name='nested'),
    path('search', views.search, name='search'),
    path('can_donate', views.f_object, name='can_donate'),
    path('f_dif', views.f_different_fields, name='f_dif'),
    path('q-f', views.q_f_together, name='q-f'),

]
