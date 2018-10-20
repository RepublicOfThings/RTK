import os
from rtk.utils.logs import build_log
from rtk import RTK_CACHE
from rtk.core.application import RTKApp
from rtk.core.processing import render, process_paths, process_app_name, process_splunk_credentials
from rtk.utils import template_path


def generate(config, fmt="yml"):
    build_log.info("Generating your project...", extra=dict(event="CLI", meta="| IN PROGRESS"))
    client_path = process_paths(config, RTK_CACHE)

    config = process_splunk_credentials(config)
    config = process_app_name(config)
    build_log.info("Processed client details...", extra=dict(event="CLI", meta="| IN PROGRESS"))
    z = render(template_path(f"{config.template}.yml-tpl"), config.__dict__)
    build_log.info("Rendered the project template...", extra=dict(event="CLI", meta="| IN PROGRESS"))
    path = os.path.join(client_path, config.name+f".{fmt}")

    with open(path, "w") as file:
        file.write(z)
    build_log.info("Project was successfully generated.", extra=dict(event="CLI", meta="| COMPLETE"))


def deactivate(config, **kwargs):
    build_log.info(f"Deactivating '{config.client}/{config.name}'",
                   extra=dict(event="CLI", meta="| IN PROGRESS"))
    app = RTKApp.from_cache(config, **kwargs)
    app.deactivate()
    build_log.info(f"Deactivated '{config.client}/{config.name}'",
                   extra=dict(event="CLI", meta="| COMPLETE"))


def activate(config, **kwargs):
    build_log.info(f"Activating '{config.client}/{config.name}'",
                   extra=dict(event="CLI", meta="| IN PROGRESS"))
    app = RTKApp.from_cache(config, **kwargs)
    app.activate()
    build_log.info(f"Activated '{config.client}/{config.name}'",
                   extra=dict(event="CLI", meta="| COMPLETE"))


def build(config, **kwargs):
    build_log.info(f"Building your application '{config.name}'...",
                   extra=dict(event="CLI", meta="| IN PROGRESS"))
    app = RTKApp.from_cache(config, **kwargs)
    app.build()
    build_log.info(f"Your application was successfully built!",
                   extra=dict(event="CLI", meta="| COMPLETE"))
    build_log.info(f"You can now go ahead and activate your application.",
                   extra=dict(event="CLI", meta="| TIP"))


def delete(config, **kwargs):
    build_log.info(f"Deleting your application '{config.name}'...",
                   extra=dict(event="CLI", meta="| IN PROGRESS"))
    app = RTKApp.from_cache(config, **kwargs)
    app.delete()
    build_log.info(f"Application deleted.",
                   extra=dict(event="CLI", meta="| COMPLETE"))

def restart(config, **kwargs):
    build_log.info(f"Restarting your application '{config.name}'...",
                   extra=dict(event="CLI", meta="| IN PROGRESS"))
    build_log.warn(f"Remember, this will restart ALL application, not just '{config.name}'...",
                   extra=dict(event="CLI", meta="| IN PROGRESS"))
    app = RTKApp.from_cache(config, **kwargs)
    app.restart()
    build_log.info(f"Application restarted.",
                   extra=dict(event="CLI", meta="| TIP"))
