import os
import tqdm
import pkg_resources
from rtk.utils import read_template


def count_walk(dir):
    count = 0
    for root, dirs, files in os.walk(dir):
        # path = root.split(os.sep)
        for _ in files:
            count += 1
    return count


def is_template(path, indicator="-tpl"):
    ext = os.path.splitext(path)[1]
    if ext[-4:] == indicator:
        return True
    else:
        return False


def template_walk(dir, config, indicator="-tpl"):
    n = count_walk(dir)
    with tqdm.tqdm(total=n, desc="Processing template files") as progress:
        for root, dirs, files in os.walk(dir):
            for file in files:
                if is_template(file, indicator):
                    print(file)
                progress.update(1)


def template_path(template_name, pkg="rtk", pkg_dir="templates"):
    root = pkg_resources.resource_filename(pkg, pkg_dir)
    return os.path.join(root, template_name)


root = pkg_resources.resource_filename("rtk", "templates/django")
print(root)

# template_walk("rtk/templates/django", {})

# n = count_walk("rtk/templates/django")
