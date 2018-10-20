from django.conf.urls import url
from django.contrib.auth.views import login, logout
from django.urls import path

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^dashboard/(?P<name>[^/]+)/$', views.dashboards, name="dashboards"),
    ]
