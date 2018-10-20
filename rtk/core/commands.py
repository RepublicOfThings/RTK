import os
from rtk import RTK_CACHE
from rtk.core.application import RTKApp
from rtk.core.processing import render, process_paths, process_app_name, process_splunk_credentials
from rtk.utils import template_path


def generate(config, fmt="yml"):
    client_path = process_paths(config, RTK_CACHE)

    config = process_splunk_credentials(config)
    config = process_app_name(config)

    z = render(template_path(f"{config.template}.yml-tpl"), config.__dict__)
    path = os.path.join(client_path, config.name+f".{fmt}")

    with open(path, "w") as file:
        file.write(z)


def deactivate(config, **kwargs):
    app = RTKApp.from_cache(config, **kwargs)
    app.deactivate()


def activate(config, **kwargs):
    app = RTKApp.from_cache(config, **kwargs)
    app.activate()


def build(config, **kwargs):
    app = RTKApp.from_cache(config, **kwargs)
    app.build()


def delete(config, **kwargs):
    app = RTKApp.from_cache(config, **kwargs)
    app.delete()


def restart(config, **kwargs):
    app = RTKApp.from_cache(config, **kwargs)
    app.restart()
