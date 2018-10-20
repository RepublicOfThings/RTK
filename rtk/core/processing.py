import os
from jinja2 import FileSystemLoader, Environment


def render(path: str, config: dict, base_path: str="/") -> str:
    env = Environment(loader=FileSystemLoader(base_path))
    return env.from_string(env.loader.get_source(env, path)[0]).render(**config)


def format_file(path, partial_=True, **kwargs):
    with open(path) as source:
        data = source.read()

    if not partial_:
        data = data.format(**kwargs)
    else:
        for key, value in kwargs.items():
            pattern = "{" + key + "}"
            data = data.replace(pattern, value)

    with open(path, "w") as target:
        target.write(data)


def process_template_project(config):
    pass


def process_splunk_credentials(config):

    if config.splunk_username == "" and config.prompt:
        splunk_username = input("Please enter your Splunk username:")
        setattr(config, "splunk_username", splunk_username)

    if config.splunk_password == "" and config.prompt:
        splunk_password = input("Please enter your Splunk password:")
        setattr(config, "splunk_password", splunk_password)

    return config


def process_app_name(config):

    if config.name is None and config.prompt:
        name = input("Please enter a name for your application:")
        setattr(config, "name", name)

    elif config.name is None:
        setattr(config, "name", f"{config.client}_app")

    if config.project is None and config.prompt:
        project = input("Please enter a name for your project:")
        setattr(config, "project", project)

    elif config.project is None:
        setattr(config, "project", f"{config.name}".capitalize())

    return config


def process_paths(config, deployment_cache):
    if not os.path.exists(deployment_cache):
        os.mkdir(deployment_cache)

    client_path = os.path.join(deployment_cache, config.client)

    if not os.path.exists(client_path):
        os.mkdir(client_path)

    return client_path
