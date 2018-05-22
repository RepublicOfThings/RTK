from .gen import RTKAppBuilder
from .config import RTKAppConfig
from .loggers import dlog
import importlib.util
import shutil
import subprocess
import os
import json

NEW = 0
INIT = 1
READY = 2
DEPLOYED = 3


class RTKApp(object):

    basedir = ".rtk_deployment"
    baseproj = "RTKWebApp"
    baseapp = "webapp"

    def __init__(self, name, mode="live"):
        self.name = name
        self.mode = mode
        if mode == "dummy":
            dlog.warn("App initialised in '{0}' mode. Changes to app will not be performed.".format(mode))

    def clone(self):
        dlog.info("Cloning app ...")
        if not self.dummy:
            dlog.info("Cloning from {0} to {1}.".format(self.github_url, self.django_path))
            os.system("git clone {0} {1}".format(self.github_url, self.django_path))
            os.system("mv {0} {1}".format(os.path.join(self.django_path, self.baseproj),
                                          os.path.join(self.django_path, self.project)))
            dlog.info("Done cloning.")
        else:
            print("DummyCommand: git clone {0} {1}".format(self.github_url, self.django_path))

    def deploy(self):
        if self.status >= READY:
            dlog.info("Executing deployment...")
            self.clone()
            dlog.info("Configuring app...")
            self.configure()
            dlog.info("Authorising access to new app...")
            self.authorise()
            dlog.info("Beginning restart...")
            self.restart()
            dlog.info("Deployment complete.")
        else:
            dlog.info("App cannot be deployed - make sure to call 'build' first.")

    def delete(self):
        if input("Are you sure you want to delete the following django directory '{0}'? y/n").lower().strip() == "y":
            shutil.rmtree(self.django_path)
            self.configure.clean()
        if input("Are you sure you want to delete the following deployment directory '{0}'? y/n").lower().strip() == "y":
            shutil.rmtree(self.path)


    def authorise(self, permissions="777"):
        if self.status >= READY:
            dlog.info("Changing access permissions for '{0}' to '{1}'...".format(self.django_path, permissions))
            subprocess.call(["chmod", permissions, self.django_path])
            dlog.info("Access permissions changed.")

    def restart(self):
        if self.status >= READY:
            dlog.info("Restarting apache with '{0}'...".format(self.deployment["apache"]["ctlscript"]))
            subprocess.call(["bash", self.deployment["apache"]["ctlscript"], "restart"])
            dlog.info("Restart complete.")

    @property
    def project(self):
        initial = self.name[0].upper()
        initial += self.name[1:]
        return "{0}WebApp".format(initial)

    @property
    def build(self):
        return RTKAppBuilder(self)

    @property
    def configure(self):
        return RTKAppConfig(self)

    @property
    def github_url(self):
        return self.deployment["github"]["url"]

    @property
    def status(self):
        out = NEW
        if os.path.exists(self.settings_path):
            out = INIT
        if os.path.exists(self.deployment_path):
            out = READY
        if out == 2:
            if os.path.exists(self.django_path):
                out = DEPLOYED
        return out

    @property
    def path(self):
        return os.path.join(".rtk_deployment", self.name)

    @property
    def settings_path(self):
        return os.path.join(".rtk_deployment", self.name, "app", "settings.py")

    @property
    def deployment_path(self):
        return os.path.join(".rtk_deployment", self.name, "config")

    @property
    def django_path(self):
        return os.path.join(self.deployment["app"]["path"], self.name)

    @property
    def settings(self):
        spec = importlib.util.spec_from_file_location("settings", self.settings_path)
        settings = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(settings)
        return settings

    @property
    def deployment(self):
        return json.load(open(os.path.join(".rtk_deployment", self.name, "config", "deployment.json")))

    @property
    def dummy(self):
        if self.mode == "live":
            return False
        else:
            return True
