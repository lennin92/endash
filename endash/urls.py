# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.authtoken import views
from rest_framework_swagger.views import get_swagger_view

from dashboard.views import urls as durls, IndexView

schema_view = get_swagger_view(title='UES Energy Dashboard')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/token-auth/', views.obtain_auth_token),
    url(r'^api/', include(durls)),
    url(r'^swagger/$', schema_view),
    url(r'^$', IndexView.as_view(), name='Main')
]
