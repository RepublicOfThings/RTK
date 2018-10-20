import os
import tqdm
import yaml
import uuid
import shutil
import pkg_resources
from distutils.dir_util import copy_tree
from rtk.core import render


def count_walk(path):
    count = 0
    for root, dirs, files in os.walk(path):
        for _ in files:
            count += 1
    return count


def is_template(path, indicator="-tpl"):
    ext = os.path.splitext(path)[1]
    if ext[-4:] == indicator:
        return True
    else:
        return False


def template_walk(path, config, indicator="-tpl"):
    n = count_walk(path)
    with tqdm.tqdm(total=n, desc="Processing template files") as progress:
        for root, dirs, files in os.walk(path):
            for file in files:
                if is_template(file, indicator):
                    parameterise_template(file, config, root)
                progress.update(1)


def template_path(template_name, pkg="rtk", pkg_dir="templates"):
    root = pkg_resources.resource_filename(pkg, pkg_dir)
    return os.path.join(root, template_name)


def parameterise_template(filepath, config, root="/", indicator="-tpl"):
    data = render(filepath, config, root)
    filename, ext = os.path.splitext(filepath)
    ext = ext[:-len(indicator)]
    new_file = f"{filename}{ext}"
    path = os.path.join(root, new_file)
    with open(path, "w") as file:
        file.write(data)


def build_project(paths):
    app_path = paths.get("django_app")
    project_path = paths.get("django_project")
    try:
        if not os.path.exists(project_path):
            base_path = paths.get("django_project")
            templates = pkg_resources.resource_filename("rtk", "templates/django")
            copy_tree(templates, project_path)

            project = os.path.split(project_path)[1]
            os.rename(os.path.join(base_path, "TemplateWebApp"), os.path.join(project_path, project))
            os.rename(os.path.join(base_path, "template_app"), app_path)
        else:
            raise FileExistsError(f"An application already exists at '{project_path}'.")

    except OSError as error:
        shutil.rmtree(project_path)
        raise OSError(error)


def parameterise_project(setup, app):
    paths = setup.get("paths")
    env = dict(
        django_base=paths.get("django_base"),
        django_wsgi=paths.get("django_wsgi"),
        django_project=paths.get("django_project"),
        django_conf=paths.get("django_conf"),
        django_static=paths.get("django_static"),
        name=app.get("name"),
        project=app.get("project"),
        secret=str(uuid.uuid4()).replace("-", ""),
        thread=str(uuid.uuid4()).replace("-", "")
    )

    template_walk(paths.get("django_base"), env)

