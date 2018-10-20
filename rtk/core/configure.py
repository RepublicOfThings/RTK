import os
import uuid
from shutil import copyfile
from rtk.core import format_file
from rtk.utils import template_path, append_line, remove_line


def append_apache_app(bitnami_conf, django_project="<APP_NOT_SET>"):
    path = template_path("httpd-prefix.conf-tpl", pkg_dir="templates/conf")

    with open(path) as prefix_file:
        data = prefix_file.read().strip()
        data = data.replace("{django_project}", django_project)

    apache_path, filename = os.path.split(bitnami_conf)
    if not os.path.exists(apache_path):
        os.makedirs(apache_path)

    append_line(bitnami_conf, target_line=data)


def remove_apache_app(bitnami_conf, django_project="<APP_NOT_SET>"):
    if os.path.exists(bitnami_conf):
        path = template_path("httpd-prefix.conf-tpl", pkg_dir="templates/conf")

        with open(path) as prefix_file:
            data = prefix_file.read().strip()
            data = data.replace("{django_project}", django_project)

        remove_line(bitnami_conf, target_line=data)


def configure_django_conf(django_conf,
                          name="<NAME_NOT_SET>",
                          django_static="<STATIC_NOT_SET>",
                          django_app="<APP_NOT_SET>",
                          django_project="<PROJECT_NOT_SET>",
                          django_wsgi="<WSGI_NOT_SET>",
                          **kwargs):

    httpd_templates = {
        "httpd-app.conf-tpl": "httpd-app.conf",
        "httpd-prefix.conf-tpl": "httpd-prefix.conf"
    }

    thread = str(uuid.uuid4()).replace("-", "")

    for template, conf in httpd_templates.items():
        output_file = os.path.join(django_conf, conf)
        path = template_path(template, pkg_dir="templates/conf")
        copyfile(path, output_file)
        format_file(output_file,
                    name=name,
                    django_wsgi=django_wsgi,
                    django_app=django_app,
                    django_static=django_static,
                    django_project=django_project,
                    thread=thread,
                    **kwargs)