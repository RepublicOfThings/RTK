from django.shortcuts import render
from django.http import HttpResponse
import yaml
import re
import os
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.utils.deprecation import RemovedInDjango21Warning
import warnings

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

config = yaml.load(open(PROJECT_DIR+"/config.yml"))

application = config.get("application")
splunk = config.get("setup").get("splunk")
dashes = application.get("dashboards")
design = application.get("style")


def home(request):
    return HttpResponse(render(request, 'pages/home/index.html', {"title": "Home",
                                                                  **design,
                                                                  "dashboards": dashes,}))


def about(request):
    return HttpResponse(render(request, 'pages/about/index.html', {"title": "About",
                                                                   **design,
                                                                   "dashboards": dashes}))


def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          extra_context=None, redirect_authenticated_user=False):
    warnings.warn(
        'The login() view is superseded by the class-based LoginView().',
        RemovedInDjango21Warning, stacklevel=2
    )

    extra_context = {"title": "Home",
                     "css": design["css"],
                     "logo": design["logo"],
                     "smeiling": design["smeiling"]}

    print(extra_context)
    return LoginView.as_view(
        template_name=template_name,
        redirect_field_name=redirect_field_name,
        form_class=authentication_form,
        extra_context=extra_context,
        redirect_authenticated_user=redirect_authenticated_user,
    )(request)


def dashboards(request, name):
    regex = re.compile('/dashboard/(.*)/')
    title = "Dashboard"
    dashboard_conf = {}
    for dashboard, conf in dashes.items():
        if regex.search(conf["url"]).group(1) == name:
            title = dashboard
            dashboard_conf = conf

    template = splunk.get("url_template")

    target = template.format(host=splunk.get("host"),
                             port=splunk.get("port"),
                             user=splunk.get("username"),
                             pwd=splunk.get("password"),
                             app=dashboard_conf.get("app"),
                             dash=dashboard_conf.get("dash"))

    return HttpResponse(render(request, 'pages/dashboard/index.html', {"title": title,
                                                                       "css": design["css"],
                                                                       "logo": design["logo"],
                                                                       "target": target,
                                                                       "dashboards": dashes}))