from django.urls import path
from . import views


urlpatterns = [

    path('', views.q_and_or, name='q_objects'),
    path('nested', views.nested_q, name='nested'),
    path('search', views.search, name='search'),
    path('can_donate', views.f_object, name='can_donate'),
    path('f_dif', views.f_different_fields, name='f_dif'),
    path('q-f', views.q_f_together, name='q-f'),
    path('count-types', views.count_types, name='count-types'),
    path('concat', views.concat, name='concat'),
    path('coalesce', views.coalesce, name='coalesce'),
    path('coalesce_prevent', views.coalesce_prevent, name='coalesce'),
    path('coalesce2', views.coalesce2, name='coalesce2'),
    path('condition', views.conditional_expressions, name='condition'),
    path('mixed', views.mixed, name='mixed'),
    path('cast', views.cast, name='cast'),
    path('greatest', views.greatest, name='greatest'),
    # path('collate', views.collate, name='collate'),

]
