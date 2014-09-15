# encoding: utf-8
from django.conf.urls import patterns, url, include
from rest_framework import routers
from tell.rest import LoggerViewSet, EntryViewSet
import views

router = routers.DefaultRouter()
router.register(r'loggers', LoggerViewSet)
router.register(r'entries', EntryViewSet)

urlpatterns = patterns('',
    url(r'^api/', include(router.urls)),
    url(r'^$', views.index, name='index'),
)