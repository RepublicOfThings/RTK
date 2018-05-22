import logging
import argparse
import os
import warnings
from rtk.deployment import RTKApp

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
        logger.error("App name '{0}' already in user -- specify a unique name and try again.".format(name))
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
    app.configure()


def activate(name, dummy=False):
    if name is not None:
        app = RTKApp(name)
    else:
        selection = _select_app()
        if selection is not None:
            app = RTKApp(name)
        else:
            return None

    app.deploy()


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
        activate(args.target, args.dummy)

    elif args.command == "deactivate":
        pass

    elif args.command == "remove":
        pass

    else:
        logger.error("Unknown command '{0}'.".format(args.command))

