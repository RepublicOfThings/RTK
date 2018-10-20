import pkg_resources
import os


def template_path(template_name, pkg="rtk", pkg_dir="templates"):
    root = pkg_resources.resource_filename(pkg, pkg_dir)
    return os.path.join(root, template_name)


def read_template(template_name, **kwargs):
    with open(template_path(template_name, **kwargs)) as template:
        data = template.read()
    return data


def remove_line(filename, target_line, break_line="\n", file_suffix=""):
    output = ""

    if break_line is not None:
        target_line += break_line

    with open(filename) as file:
        for line in file:
            if line != target_line:
                output += line

    with open(filename + file_suffix, "w") as file:
        file.write(output)


def append_line(filename, target_line, break_line="\n", file_suffix="", *args):
    if os.path.exists(filename):
        with open(filename) as file:
            output = file.read(*args)
            if break_line is not None:
                target_line += break_line

            output += target_line
    else:
        if break_line is not None:
            target_line += break_line
        output = target_line

    with open(filename + file_suffix, "w") as file:
        file.write(output)
