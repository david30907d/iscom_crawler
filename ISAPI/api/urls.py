# -*- coding: utf-8 -*-
from django.conf.urls import url
from api.views import api, findRoot

urlpatterns = [
  url(r'^$', api, name='api'),
  url(r'^findroot$', findRoot, name='findRoot'),
]
