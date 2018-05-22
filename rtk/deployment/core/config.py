import os
import re
from .loggers import dlog
from ..templates.django_app import config as splunk_template
from rtk.utils import keys

NEW = 0
INIT = 1
READY = 2
DEPLOYED = 3


class RTKAppConfig(object):
    def __init__(self, app):
        self.app = app

    def __call__(self):
        if self.app.status == DEPLOYED:
            dlog.info("Configuring your new app...")
            self.wsgi()
            self.settings()
            self.apache()
            self.splunk()
            dlog.info("Configuration complete...")
        else:
            dlog.error("Cannot deploy app - make sure to build your app settings and clone the app first.")

    def apache(self):
        dlog.info("Configuring Apache...")
        config = self._deployment
        apache = self._apache
        bitnami_prefix_path = os.path.join(apache["path"], "bitnami-apps-prefix.conf")
        new_app_include = apache["template"].format(path=config["app"]["path"],
                                                    app=config["app"]["name"])

        data = self._update_prefix_conf(bitnami_prefix_path, new_app_include)

        if self.app.dummy:
            print("DummyCommand: Access {0}.".format(bitnami_prefix_path))
            print("DummyCommand: Write \n {0}".format(data))
        else:
            dlog.info("Writing Apache config to '{0}'...".format(bitnami_prefix_path))
            with open(bitnami_prefix_path, "w") as bitnami_file:
                bitnami_file.write(data)
        dlog.info("Apache configured.")

    def wsgi(self):
        wsgi = self._wsgi
        dlog.info("Configuring WSGI...")
        self._write_wsgi_conf(wsgi)
        self._write_wsgi_file()

    def _write_wsgi_conf(self, wsgi: dict) -> None:
        conf_path = os.path.join(self.app.django_path, "conf")
        for config_file, template_file in wsgi["conf"].items():
            path = os.path.join(conf_path, config_file)
            dlog.info("Writing WSGI to '{0}'...".format(path))
            with open(os.path.join(self.app.deployment_path, template_file)) as current:
                if self.app.dummy:
                    print("DummyCommand: Write '{0}' to '{1}'".format(template_file, path))
                    print("DummyCommand: Dumping... \n {0}".format(current.read()))
                else:
                    with open(path, "w") as target:
                        target.write(current.read())
                        target.close()
                        current.close()
            dlog.info("Configured WSGI.")

    def _write_wsgi_file(self):
        wsgi_path = os.path.join(self.app.django_path, self.app.project, "wsgi.py")
        with open(wsgi_path, "r") as wsgi:
            content = wsgi.read()
            wsgi.close()
            content = re.sub("{app_name}", self.app.project, content)
            content = re.sub("{project}", self.app.name, content)
            if self.app.dummy:
                print("DummyCommand: Write to '{0}''".format(wsgi_path))
                print("DummyCommand: Dumping... \n {0}".format(content))
            else:
                with open(wsgi_path, "w") as wsgi:
                    wsgi.write(content)
                    wsgi.close()

    def splunk(self):
        splunk = self._splunk
        app_settings = splunk_template.format(user=splunk["user"],
                                                 pwd=splunk["pwd"],
                                                 host=splunk["host"],
                                                 port=splunk["port"],
                                                 alerts=splunk["dashboards"]["alerts"]["dash"],
                                                 homes=splunk["dashboards"]["homes"]["dash"],
                                                 alert_app=splunk["dashboards"]["alerts"]["app"],
                                                 homes_app=splunk["dashboards"]["homes"]["app"],
                                                 url=splunk["url"]
                                                 )

        settings_path = os.path.join(self.app.django_path, self.app.baseapp, "app_settings.py")

        if self.app.dummy:
            print("DummyCommand: Write splunk settings to '{0}'.".format(settings_path))
            print("DummyCommand: Dumping... \n {0}".format(app_settings))
        else:
            with open(settings_path, "w") as settings_file:
                settings_file.write(app_settings)
                settings_file.close()

    def settings(self, key_pattern=r'{__SECRET_KEY__}'):
        settings_path = os.path.join(self.app.django_path, self.app.project, "settings.py")
        with open(settings_path, "r") as settings:
            content = settings.read()
            settings.close()
            if re.search(key_pattern, content):
                content = re.sub(key_pattern, keys.generate_secret(), content)
                content = re.sub("r{__PROJECT__}", self.app.project, content)
                if self.app.dummy:
                    print("DummyCommand: Write to '{0}''".format(settings_path))
                    print("DummyCommand: Dumping... \n {0}".format(content))
                else:
                    with open(settings_path, "w") as settings:
                        settings.write(content)
                        settings.close()

    @property
    def _deployment(self):
        return self.app.deployment

    def _update_prefix_conf(self, prefix_file, include_statement):
        if self.app.dummy:
            print("DummyCommand: Update bitnami-apps-prefix.conf")
            print("DummyCommand: Add {0}".format(include_statement))
            return include_statement
        else:
            data = ""
            dlog.info("Loading Apache data from '{0}'...".format(prefix_file))
            for statement in open(prefix_file):  # this isn't robust: will miss statements without linebreaks.
                if statement == include_statement:
                    return
                elif statement.strip() == "\n":
                    pass
                else:
                    data += statement + "\n"

            data += include_statement
            data = "\n".join(list(set([ll.rstrip() for ll in data.splitlines() if ll.strip()])))
            dlog.info("Writing Apache data '{0}'...".format(data))
            return data

    def __getattr__(self, item):
        if item[1:] in self.app.deployment.keys():
            return self.app.deployment[item[1:]]
        else:
            super().__getattribute__(item)