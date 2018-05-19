from rtk.deployment.templates import deployment, defaults, template, httpd_prefix, httpd_app, django_app
from .utils import configure_template
import importlib.util
import logging
import json
import re
import os.path
import os
import subprocess
import shutil


class RTKApp(object):
    def __init__(self, name):
        self.name = name

    def authorise(self, permissions="777"):
        if self.status == 3:
            subprocess.call(["chmod", permissions, self.django_path])

    @property
    def status(self):
        out = 0
        if os.path.exists(os.path.join(".rtk_deployment", self.name, "app", "settings.py")):
            out = 1
        if os.path.exists(os.path.join(".rtk_deployment", self.name, "config", "deployment.json")):
            out = 2
        if out == 2:
            if os.path.exists(self.django_path):
                out = 3
        return out

    @property
    def django_path(self):
        return os.path.join(self._config["app"]["path"], self.name)

    @property
    def _config(self):
        return json.load(open(os.path.join(".rtk_deployment", self.name, "config", "deployment.json")))


class RTKWebDeployment(object):
    def __init__(self, name, basedir=".rtk_deployment/{0}", level=logging.DEBUG):
        logging.basicConfig(level=level)
        self.name = name
        self.basedir = basedir.format(name)
        self._logger = logging.getLogger("RTKWebDeployment")
        self._errors = {}

    @property
    def app_path(self):
        config = self._load_config()
        return os.path.join(config["app"]["path"], self.name)

    def _load_config(self):
        config_path = os.path.join(self.basedir, "config", "deployment.json")
        if os.path.exists(config_path):
            config = json.load(open(config_path, "r"))
            return config
        else:
            self._errors.update({"ConfigFileNotFound": "No configuration found on path {0}".format(config_path)})
            return {}

    def initialise(self, use_defaults=False, **kwargs):
        path = os.path.join(self.basedir, "app")
        if not os.path.exists(path):
            os.makedirs(path)

        if use_defaults:
            data = open(defaults.__file__, "r").read()
        else:
            data = open(template.__file__, "r").read()

        for key, value in kwargs.items():
            data = re.sub(r"{"+key+"}", value, data)

        data = re.sub(r"{app_name}", self.name, data)

        with open(os.path.join(path, "settings.py"), "w") as settings_file:
            settings_file.write(data)

    def create(self, **kwargs):
        self._log("Creating your new app...")
        config = self._load_config()

        if len(config) == 0:
            self._deployment_status()
            return

        try:
            self.clone_base_app(config)
        except Exception as error:
            self._errors.update({"GitHubCloningError": error})

        try:
            self._log("Configuring your new app '{0}'...".format(config['app']['name']))
            self.configure_app(config)
            self.configure_apache(config, **kwargs)
        except OSError as error:
            self._errors.update({"EnvironmentError": error})
        self._deployment_status()

    def destroy(self):
        config = self._load_config()

        confirm = input("Are you sure you want to permanently delete '{0}'? Type the app name to continue... \n".format(config["app"]["name"]))
        if confirm.lower() == self.name:
            self._log("Destroying your app '{0}'...".format(config["app"]["name"]))
            app_path = os.path.join(config['app']['path'], config["app"]["name"])
            self._log("Deleting Django app folder...")
            shutil.rmtree(app_path)
            self._log("Reverting Apache and Bitnami configuration...")
            self.revert_apache(config)
        else:
            self._log("Aborted.")
        self._deployment_status()

    def configure_app(self, config):
        self.configure_wsgi(config)
        self.configure_settings(config)

    def configure_wsgi(self, config):
        self._log("Writing Django's WSGI settings...")
        wsgi = config["wsgi"]
        for filename, template in wsgi["conf"].items():
            self._log("Writing '{0}' ...".format(filename))
            self._write_wsgi(config, template, filename)
        self._log("Django's WSGI settings are ready.")

    def configure_settings(self, config):
        self._log("Writing some Python code...")
        splunk = config["splunk"]
        app_settings = django_app.config.format(user=splunk["user"],
                                                 pwd=splunk["pwd"],
                                                 host=splunk["host"],
                                                 port=splunk["port"],
                                                 alerts=splunk["dashboards"]["alerts"]["dash"],
                                                 homes=splunk["dashboards"]["homes"]["dash"],
                                                 alert_app=splunk["dashboards"]["alerts"]["app"],
                                                 homes_app=splunk["dashboards"]["homes"]["app"],
                                                 url=splunk["url"]
                                                 )
        project_path = os.path.join(config['app']['path'], config['app']['name'])
        settings_path = os.path.join(project_path, "rtkapp", "app_settings.py")
        with open(settings_path, "w") as settings_file:
            settings_file.write(app_settings)
            settings_file.close()

        self._log("Nice shiny new Python code is ready.")
        self._log("Django app is configured for Splunk.")

    def _write_wsgi(self, config, wsgi_file, filename):
        project_path = os.path.join(config['app']['path'], config['app']['name'])
        wsgi_conf_path = os.path.join(project_path, "conf")
        wsgi_file_path = os.path.join(wsgi_conf_path, filename)
        temp_file_path = os.path.join(self.basedir, wsgi_file)
        if not os.path.exists(wsgi_conf_path):
            os.makedirs(wsgi_conf_path)

        data = open(temp_file_path, "r").read()

        with open(wsgi_file_path, "w") as wsgi_file:
            wsgi_file.write(data)
            wsgi_file.close()

    def revert_apache(self, config):
        apache_config = config["apache"]
        include_statement = apache_config["template"].format(path=config["app"]["path"],
                                                             app=config["app"]["name"])
        bitnami_config = os.path.join(apache_config["path"], "/bitnami-apps-prefix.conf")

        try:
            data = ""
            for statement in open(bitnami_config):  # this isn't robust: will miss statements without linebreaks.
                if statement == include_statement:
                    pass
                else:
                    data += statement + "\n"

            with open(bitnami_config, "w") as bitnami:
                bitnami.write(data)

        except FileNotFoundError as error:
            self._errors.update({"BitnamiConfigError": error})
            self._log("Could not find a Bitnami configuration.", level=logging.ERROR)

    def configure_apache(self, config, dummy=True):
        apache_config = config["apache"]
        include_statement = apache_config["template"].format(path=config["app"]["path"],
                                                             app=config["app"]["name"])

        if dummy:
            bitnami_config = os.path.join(apache_config["path"], "bitnami-apps-prefix.conf")
        else:
            bitnami_config = os.path.join(apache_config["path"], "bitnami-apps-prefix-dummy.conf")

        try:
            data = ""
            for statement in open(bitnami_config):  # this isn't robust: will miss statements without linebreaks.
                if statement == include_statement:
                    return
                elif statement.strip() == "\n":
                    pass
                else:
                    data += statement + "\n"

            data += include_statement + "\n"

            with open(bitnami_config, "w") as bitnami:
                bitnami.write(data)

        except FileNotFoundError as error:
            self._errors.update({"BitnamiConfigError": error})
            self._log("Could not find a Bitnami configuration.", level=logging.ERROR)

    def clone_base_app(self, config):
        self._log("Cloning app from GitHub...")
        git_url = config["github"]["url"]
        app_path = os.path.join(config['app']['path'], config["app"]["name"])
        if os.path.exists(app_path):
            self._log("An app already exists on the path '{0}', skipping clone phase.".format(app_path))
        else:
            os.system("git clone {0} {1}".format(git_url, app_path))
            self._log("Cloned '{0}' to '{1}'.".format(config['app']['name'], app_path))

    def prepare(self):
        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)

        if os.path.exists(os.path.join(self.basedir, "app", "settings.py")):
            settings = os.path.join(self.basedir, "app", "settings.py")
        else:
            settings = None

        config = deployment.config.copy()
        if settings is not None:
            spec = importlib.util.spec_from_file_location("settings", settings)
            settings = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(settings)
            settings.APP_NAME = self.name
        else:
            settings = defaults
            settings.APP_NAME = self.name

        config = self._prepare_config(config, settings)
        self._prepare_apache(config)

    def _deployment_status(self):
        if len(self._errors) > 0:
            self._log("!--------------------------------------------------!", level=logging.ERROR)
            self._log("During setup, the following errors were encountered:", level=logging.ERROR)
            for error, message in self._errors.items():
                self._log(">> {0} - {1}".format(error, message), level=logging.ERROR)
            self._log("Configuration may not have executed successfully.", level=logging.ERROR)
            self._log("!--------------------------------------------------!", level=logging.ERROR)
        else:
            self._log("No errors were detected -- activity was successful.")

    def _prepare_config(self, config, settings=None):
        self._log("Preparing your app configuration file...")
        config = configure_template(config, settings)
        path = os.path.join(self.basedir, "config")
        if not os.path.exists(path):
            os.makedirs(path)
        self._log("App configuration is ready.")
        path = os.path.join(path, "deployment.json")
        json.dump(config, open(path, "w"), indent=4)
        return config

    def _prepare_apache(self, config):
        self._log("Preparing your apache configuration files...")
        prefix = httpd_prefix.config.format(path=config['app']['path'], app=config['app']['name'])
        app = httpd_app.config.format(path=config['app']['path'],
                                      app=config['app']['name'],
                                      GLOBAL="GLOBAL",
                                      GROUP="GROUP")

        app_path = os.path.join(self.basedir, "config", "httpd-app-template.conf")
        with open(app_path, "w") as app_file:
            self._log("Writing httpd-app-template...")
            app_file.write(app)

        prefix_path = os.path.join(self.basedir, "config", "httpd-prefix-template.conf")
        with open(prefix_path, "w") as prefix_file:
            self._log("Writing httpd-prefix-template...")
            prefix_file.write(prefix)

        self._log("Apache configuration templates are ready.")

    def _log(self, msg, level=logging.INFO, *args, **kwargs):
        self._logger.log(level, msg, *args, **kwargs)
