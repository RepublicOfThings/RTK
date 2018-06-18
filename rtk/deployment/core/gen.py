import os
import re
import json
from .loggers import dlog
from ..templates import (defaults as default_settings,
                         template as template_settings,
                         deployment as deployment_template,
                         httpd_app as httpd_app_template,
                         httpd_prefix as httpd_prefix_template)
import uuid
from .utils import configure_template


class RTKAppBuilder(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, *args, **kwargs):
        self.settings(*args, **kwargs)
        self.deployment()
        self.conf()

    def settings(self, default=False, **kwargs):
        path = os.path.join(self.app.path, "app")

        self._prepare_path(path)

        if default:
            data = self._prepare_settings(default_settings, **kwargs)
        else:
            data = self._prepare_settings(template_settings, **kwargs)

        settings_path = os.path.join(path, "settings.py")

        dlog.info("Writing settings '{0}'...".format(settings_path))

        with open(settings_path, "w") as settings_file:
            settings_file.write(data)

    def deployment(self):
        dlog.info("Building deployment configuration...")
        config = configure_template(deployment_template.config.copy(), self.app.settings)
        self._prepare_path(self.app.deployment_path)
        path = os.path.join(self.app.deployment_path, "deployment.json")
        dlog.info("Writing deployment configuration to '{0}'...".format(path))
        json.dump(config, open(path, "w"), indent=4)
        dlog.info("Deployment configuration ready.")

    def conf(self):
        dlog.info("Building WSGI configuration files...")
        self._write_httpd_app()
        self._write_httpd_prefix()

    def _write_httpd_prefix(self):
        config = self.app.deployment
        prefix = httpd_prefix_template.config.format(path=config['app']['path'],
                                                     app=config['app']['name'])

        app_path = os.path.join(self.app.basedir, self.app.name, "config", "httpd-prefix-template.conf")

        dlog.info("Writing '{0}' file to '{1}'...".format("httpd-prefix-template.conf", app_path))

        with open(app_path, "w") as httpd_prefix:
            httpd_prefix.write(prefix)

    def _write_httpd_app(self):
        config = self.app.deployment
        app = httpd_app_template.config.format(path=config['app']['path'],
                                               app=config['app']['name'],
                                               project=self.app.project,
                                               thread=str(uuid.uuid4()).replace("-", ""),
                                               GLOBAL="RESOURCE",
                                               GROUP="GROUP")

        app_path = os.path.join(self.app.basedir, self.app.name, "config", "httpd-app-template.conf")

        dlog.info("Writing '{0}' file to '{1}'...".format("httpd-app-template.conf", app_path))

        with open(app_path, "w") as app_file:
            app_file.write(app)

    def _prepare_settings(self, settings, **kwargs):
        data = open(settings.__file__, "r").read()

        for key, value in kwargs.items():
            data = re.sub(r"{"+key+"}", value, data)

        data = re.sub(r"{app_name}", self.app.name, data)
        return data

    @staticmethod
    def _prepare_path(path):
        if not os.path.exists(path):
            os.makedirs(path)
