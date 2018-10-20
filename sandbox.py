import os
import tqdm


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
    manifest = ""
    with tqdm.tqdm(total=n, desc="Processing template files") as progress:
        for root, dirs, files in os.walk(path):
            manifest += f"include {root}/*\n"
            # for file in files:
            #     print(os.path.splitext(file))
    print(manifest)

template_walk("rtk/templates", {})