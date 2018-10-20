import os
import yaml
import subprocess
from rtk import RTK_CACHE
from shutil import copyfile, rmtree
from rtk.core.build import build_project, parameterise_project
from rtk.core.configure import append_apache_app, remove_apache_app


class RTKApp(object):
    def __init__(self, client, path, setup=None, application=None):
        self.setup = setup
        self.client = client
        self._config_path = path
        self.application = application

    def build(self):
        if not os.path.exists(self.path):
            build_project(self.setup.get("paths"))
        parameterise_project(self.setup, self.application)
        copyfile(self._config_path, os.path.join(self.setup.get("paths").get("django_app"), "config.yml"))

    def activate(self):
        paths = self.setup.get("paths")
        if not os.path.exists(self.path):
            self.build()
        append_apache_app(paths.get("bitnami_conf"), django_project=paths.get("django_project"))

    def deactivate(self):
        paths = self.setup.get("paths")
        if os.path.exists(self.path):
            remove_apache_app(paths.get("bitnami_conf"), django_project=paths.get("django_project"))

    def delete(self):
        self.deactivate()
        rmtree(self.path)

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
