from rtk.deployment.templates import deployment, defaults, httpd_prefix, httpd_app, django_app
from .utils import configure_template
import importlib.util
import logging
import json
import os.path


class RTKWebDeployment(object):
    def __init__(self, name, basedir="{0}_deployment/", level=logging.DEBUG):
        # ./deploy.sh --prepare=demo --settings=custom.py
        # ./deploy.sh --create=demo
        # ./deploy.sh --destroy=demo
        # ./deploy.sh --new

        # >> Project Name: Demo
        # >> Project Path: djangostack-2.0.3-0 ... (use default? y/n)
        # >> Project Schema: http (use default? y/n)

        logging.basicConfig(level=level)
        self.name = name
        self.basedir = basedir.format(name)
        self._logger = logging.getLogger("RTKWebDeployment")
        if not os.path.exists(self.basedir):
            os.mkdir(self.basedir)

    def create(self):
        self._log("Creating your new app...")
        config_path = os.path.join(self.basedir, "deployment.json")
        config = json.load(open(config_path, "r"))
        self.clone_base_app(config)
        self._log("Configuring your new app '{0}'...".format(config['app']['name']))
        self.configure_app(config)
        self.configure_apache(config)
        self._log("Your new '{0}' is ready. Restart Apache.".format(config['app']['name']))

    def destroy(self):
        pass

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

    def configure_apache(self, config):
        pass

    def clone_base_app(self, config):
        self._log("Cloning app from GitHub...")
        git_url = config["github"]["url"]
        app_path = os.path.join(config['app']['path'], config["app"]["name"])
        if os.path.exists(app_path):
            self._log("An app already exists on the path '{0}', skipping clone phase.".format(app_path))
        else:
            os.system("git clone {0} {1}".format(git_url, app_path))
            self._log("Cloned '{0}' to '{1}'.".format(config['app']['name'], app_path))

    def prepare(self, settings=None):
        config = deployment.config.copy()
        if settings is not None:
            spec = importlib.util.spec_from_file_location("settings", settings)
            settings = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(settings)
        else:
            settings = defaults

        config = self._prepare_config(config, settings)
        self._prepare_apache(config)

    def _prepare_config(self, config, settings=None):
        self._log("Preparing your app configuration file...")
        config = configure_template(config, settings)
        path = os.path.join(self.basedir, "deployment.json")
        self._log("App configuration is ready.")
        json.dump(config, open(path, "w"), indent=4)
        return config

    def _prepare_apache(self, config):
        self._log("Preparing your apache configuration files...")
        prefix = httpd_prefix.config.format(path=config['app']['path'], app=config['app']['name'])
        app = httpd_app.config.format(path=config['app']['path'],
                                      app=config['app']['name'],
                                      GLOBAL="GLOBAL",
                                      GROUP="GROUP")

        app_path = os.path.join(self.basedir, "httpd-app-template.conf")
        with open(app_path, "w") as app_file:
            self._log("Writing httpd-app-template...")
            app_file.write(app)

        prefix_path = os.path.join(self.basedir, "httpd-prefix-template.conf")
        with open(prefix_path, "w") as prefix_file:
            self._log("Writing httpd-prefix-template...")
            prefix_file.write(prefix)

        self._log("Apache configuration templates are ready.")

    def _log(self, *args, **kwargs):
        self._logger.info(*args, **kwargs)
