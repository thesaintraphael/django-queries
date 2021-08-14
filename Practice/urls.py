from django import urls
from django.contrib import admin
from django.urls import path, include

import debug_toolbar


urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('', include('app.urls')),
    path('', include('agg.urls')),
    path('', include('app_related.urls')),
]
