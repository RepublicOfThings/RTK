import os


def clone(config, root="./", name=None):

    repository_name = os.path.split(config.get("repository"))[1]

    if name is None:
        name = repository_name

    base_path = os.path.join(root, name)
    local_path = os.path.join(base_path, name)
    clone_path = os.path.join(base_path, repository_name)

    if os.path.exists(local_path):
        raise FileExistsError(f"An application already exists on the path '{local_path}'.")
    else:
        os.system(f"git clone {config.get('repository')} {base_path}")

    if clone_path != local_path:
        os.rename(clone_path, local_path)
