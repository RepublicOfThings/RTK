import os
import yaml
import subprocess
from rtk import RTK_CACHE
from shutil import copyfile, rmtree
from rtk.core.build import build_project, parameterise_project
from rtk.core.configure import append_apache_app, remove_apache_app
from rtk.utils.logs import build_log


class RTKApp(object):
    def __init__(self, client, path, setup=None, application=None):
        self.setup = setup
        self.client = client
        self._config_path = path
        self.application = application

    def build(self):
        if not os.path.exists(self.path):
            build_log.info("Building the project from Django-RTK Application templates.",
                           extra=dict(event="TASK", meta="| IN PROGRESS"))
            build_project(self.setup.get("paths"))

        build_log.info("Parameterising the templates...",
                       extra=dict(event="TASK", meta="| IN PROGRESS"))
        parameterise_project(self.setup, self.application)

        build_log.info("Cloning configuration into application structure...",
                       extra=dict(event="TASK", meta="| IN PROGRESS"))

        copyfile(self._config_path, os.path.join(self.setup.get("paths").get("django_app"), "config.yml"))

        build_log.info("Build task complete",
                       extra=dict(event="TASK", meta="| COMPLETE"))

    def activate(self):
        build_log.info("Beginning activation task...",
                       extra=dict(event="TASK", meta="| IN PROGRESS"))
        paths = self.setup.get("paths")
        build_log.info("Modifying Bitnami Apache configuration...",
                       extra=dict(event="TASK", meta="| IN PROGRESS"))
        append_apache_app(paths.get("bitnami_conf"), django_project=paths.get("django_project"))
        build_log.info("Activation task complete",
                       extra=dict(event="TASK", meta="| COMPLETE"))

    def deactivate(self):
        paths = self.setup.get("paths")
        if os.path.exists(self.path):
            build_log.info("Modifying Bitnami Apache configuration...",
                           extra=dict(event="TASK", meta="| IN PROGRESS"))
            remove_apache_app(paths.get("bitnami_conf"), django_project=paths.get("django_project"))
            build_log.info(f"Removed {self.application.get('name')} from Apache configuration.",
                           extra=dict(event="TASK", meta="| IN PROGRESS"))
        build_log.info("Deactivation task complete",
                       extra=dict(event="TASK", meta="| COMPLETE"))

    def delete(self):
        build_log.info(f"Deleting {self.application.get('name')}...",
                       extra=dict(event="TASK", meta="| IN PROGRESS"))
        self.deactivate()
        path = self.setup.get("paths")["django_project"]
        rmtree(path)
        build_log.info("Deletion task complete",
                       extra=dict(event="TASK", meta="| COMPLETE"))

    def restart(self):
        paths = self.setup.get("paths")
        subprocess.call(["bash", paths["sys_ctl"], "restart"])

    @property
    def path(self):
        return self.setup.get("paths")["django_app"]

    @property
    def exists(self):
        return os.path.exists(self.path)

    @classmethod
    def from_cache(cls, config, **kwargs):
        path = os.path.join(RTK_CACHE, config.client, config.name)
        path = f"{path}.yml"
        return cls.from_yaml(path, **kwargs)

    @classmethod
    def from_yaml(cls, filepath, *args, **kwargs):
        data = yaml.load(open(filepath, *args), **kwargs)
        return cls(path=filepath, **data)
