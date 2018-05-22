import logging
import argparse
import os
import warnings
import subprocess
from rtk.deployment import RTKApp


def selector(func):
    def wrapper(name, **kwargs):
        if name is not None:
            app = RTKApp(name, **kwargs)
        else:
            selection = _select_app()
            if selection is not None:
                app = RTKApp(selection, **kwargs)
            else:
                return None
        return func(app, **kwargs)
    return wrapper


def _apps():
    return os.listdir(".rtk_deployment/")


def _select_app():
    print("The following apps are available:")
    for app in _apps():
        print(app)

    count = 1
    selection = input("Deployment target:")
    while selection not in _apps():
        selection = input("Deployment target:".format(count))
        print("No such app, try again ({0}/3 attempts)...")
        count += 1
        if count > 3:
            logger.info("Too many retries. Aborted deployment.")
            return None

    return selection


def _add_app(name, dummy=False):
    if not name.islower():
        warnings.warn("All app names must be in lower case.")
    name = name.lower()
    if name in _apps():
        logger.error("App name '{0}' already in installed apps -- specify a unique name and try again.".format(name))
        raise ValueError("Non-unique app ID: '{0}'.".format(name))
    else:
        app = RTKApp(name)
    return app


def add(name, dummy=False, default=True):
    if name is not None:
        app = _add_app(name, dummy)
    else:
        app = _add_app(input("App name: "), dummy)
    app.build(default=default)


@selector
def update(app):
    app.update()


@selector
def activate(app):
    app.deploy()


@selector
def remove(app):
    app.delete()
    # app.restart()
    # subprocess.call(["bash", "./djangostack-2.0.3-0", "restart"])

@selector
def deactivate(app):
    app.deactivate()
    app.restart()


@selector
def reactivate(app):
    app.reactivate()
    app.restart()


parser = argparse.ArgumentParser()

parser.add_argument("command")
parser.add_argument("--target")
parser.add_argument("--dummy", default=True)


if __name__ == "__main__":
    args = parser.parse_args()
    logger = logging.getLogger("RTKDeploy")
    logging.basicConfig(level=logging.DEBUG)

    if args.command == "add":
        add(args.target, args.dummy)

    elif args.command == "activate":
        activate(args.target, mode=args.dummy)

    elif args.command == "deactivate":
        deactivate(args.target)

    elif args.command == "reactivate":
        reactivate(args.target)

    elif args.command == "remove":
        remove(args.target)

    elif args.command == "update":
        update(args.target)

    elif args.command == "available":
        for app in _apps():
            print(app)

    # elif args.command == "test":
    #     test(args.target, mode=args.dummy)

    else:
        logger.error("Unknown command '{0}'.".format(args.command))
