import os
import re
from .loggers import dlog
from ..templates.django_app import config as splunk_template
from rtk.utils import keys
import uuid

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
            if data is not None:
                with open(bitnami_prefix_path, "w") as bitnami_file:
                    bitnami_file.write(data)
        dlog.info("Apache configured.")

    def wsgi(self):
        wsgi = self._wsgi
        dlog.info("Configuring WSGI...")
        self._write_wsgi_conf(wsgi)
        self._write_wsgi_file()

    def clean(self):
        config = self._deployment
        bitnami_prefix_path = os.path.join(self._apache["path"], "bitnami-apps-prefix.conf")
        target = self._apache["template"].format(path=config["app"]["path"],
                                                    app=config["app"]["name"])
        dlog.info("Loading Apache data from '{0}'...".format(bitnami_prefix_path))
        with open(bitnami_prefix_path) as file:
            data = ""
            for line in file:
                if line.replace("\n", "").strip() != target.replace("\n", "").strip():
                    data += line

        data = "\n".join(list(set([ll.rstrip() for ll in data.splitlines() if ll.strip()])))
        dlog.info("Writing Apache data '{0}'...".format(data))
        with open(bitnami_prefix_path, "w") as bitnami_file:
            bitnami_file.write(data)

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

        settings_path = os.path.join(self.app.django_path, self.app.webapp, "app_settings.py")

        if self.app.dummy:
            print("DummyCommand: Write splunk settings to '{0}'.".format(settings_path))
            print("DummyCommand: Dumping... \n {0}".format(app_settings))
        else:
            with open(settings_path, "w") as settings_file:
                settings_file.write(app_settings)
                settings_file.close()

    def settings(self):
        dlog.info("Configuring app settings...")
        settings_path = os.path.join(self.app.django_path, self.app.project, "settings.py")
        with open(settings_path, "r") as settings:
            content = settings.read()
            settings.close()

            content = re.sub(r"{__SECRET_KEY__}", keys.generate_secret(), content)
            content = re.sub(r"{__PROJECT__}", self.app.project, content)
            content = re.sub(r"{__WEBAPP__}", self.app.webapp, content)
            if self.app.dummy:
                print("DummyCommand: Write to '{0}''".format(settings_path))
                print("DummyCommand: Dumping... \n {0}".format(content))
            else:
                with open(settings_path, "w") as updated:
                    updated.write(content)
                    updated.close()
            dlog.info("Configured app settings.")

        manage_path = os.path.join(self.app.django_path, "manage.py")
        with open(manage_path, "r") as manage:
            content = manage.read()
            manage.close()

            content = re.sub(r"{__PROJECT__}", self.app.project, content)

            if self.app.dummy:
                print("DummyCommand: Write to '{0}''".format(manage_path))
                print("DummyCommand: Dumping... \n {0}".format(content))
            else:
                with open(manage_path, "w") as updated:
                    updated.write(content)
                    updated.close()
            dlog.info("Configured app settings.")

        proj_urls_path = os.path.join(self.app.django_path, self.app.project, "urls.py")
        with open(proj_urls_path, "r") as proj_urls:
            content = proj_urls.read()
            proj_urls.close()

            content = re.sub(r"{__WEBAPP__}", self.app.webapp, content)
            if self.app.dummy:
                print("DummyCommand: Write to '{0}''".format(proj_urls_path))
                print("DummyCommand: Dumping... \n {0}".format(content))
            else:
                with open(proj_urls_path, "w") as updated:
                    updated.write(content)
                    updated.close()
            dlog.info("Configured project urls.")

        apps_path = os.path.join(self.app.django_path, self.app.webapp, "apps.py")
        with open(apps_path, "r") as apps:
            content = apps.read()
            apps.close()

            content = re.sub(r"{__WEBAPP__}", self.app.webapp, content)
            if self.app.dummy:
                print("DummyCommand: Write to '{0}''".format(apps_path))
                print("DummyCommand: Dumping... \n {0}".format(content))
            else:
                with open(apps_path, "w") as updated:
                    updated.write(content)
                    updated.close()

        urls_path = os.path.join(self.app.django_path, self.app.webapp, "urls.py")
        with open(urls_path, "r") as urls:
            content = urls.read()
            urls.close()
            content = re.sub(r"{__WEBAPP__}", self.app.webapp, content)
            if self.app.dummy:
                print("DummyCommand: Write to '{0}''".format(urls_path))
                print("DummyCommand: Dumping... \n {0}".format(content))
            else:
                with open(urls_path, "w") as updated:
                    updated.write(content)
                    updated.close()

        views_path = os.path.join(self.app.django_path, self.app.webapp, "views.py")
        with open(views_path, "r") as views:
            content = views.read()
            views.close()
            content = re.sub(r"{__WEBAPP__}", self.app.webapp, content)
            if self.app.dummy:
                print("DummyCommand: Write to '{0}''".format(views_path))
                print("DummyCommand: Dumping... \n {0}".format(content))
            else:
                with open(views_path, "w") as updated:
                    updated.write(content)
                    updated.close()

    @property
    def _deployment(self):
        return self.app.deployment

    def _update_prefix_conf(self, prefix_file, include_statement):
        if self.app.dummy:
            print("DummyCommand: Update bitnami-apps-prefix.conf")
            print("DummyCommand: Add {0}".format(include_statement))
            return None
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