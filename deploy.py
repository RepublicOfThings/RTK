from rtk.deployment import RTKWebDeployment
import argparse
import logging
import getpass
import os


def _is_inited(name):
    if os.path.exists(".rtk_deployment/{name}/app/settings.py".format(name=name)):
        return True
    else:
        return False


def _apps():
    return os.listdir(".rtk_deployment/")


def _init_app(args, logger):
    logger.info("Initialising a new app...")
    if args.name is not None:
        app_name = args.name
    else:
        app_name = input("App Name:")

    d = RTKWebDeployment(app_name)
    if input("Configure splunk now? y/n").lower() == "y":
        splunk_username = input("Splunk username:")
        splunk_pwd = getpass.getpass("Splunk password:")
        d.initialise(splunk_user=splunk_username, splunk_password=splunk_pwd, use_defaults=args.defaults)
    else:
        d.initialise(use_defaults=args.defaults)


def _select_app():
    print("The following apps are ready for deployment:")
    for app in _apps():
        print(app)

    count = 1
    selection = input("Deployment target:")
    while selection not in _apps():
        selection = input("Deployment target:".format(count))
        print("No such app, try again ({0}/3 attempts)...")
        count += 1
        if count > 3:
            logger.info("Aborted deployment.")
            return None

    return selection


def _deploy_app(args, logger):
    selection = None
    logger.info("Preparing for deployment...")
    if args.name is None:
        apps = _apps()
        if len(apps) == 0:
            init = input("No apps are available. Initialise a new one? y/n").lower()
            if init == "y":
                _init_app(args, logger)
            else:
                print("Please initialise an app before attempting to re-deploy. Use the 'init' command.")
                return
        elif len(apps) == 1:
            default = input("Deploy '{0}'? y/n".format(apps[0])).lower()
            if default == "y":
                selection = apps[0]
            else:
                selection = _select_app()
        else:
            selection = _select_app()

    else:
        selection = args.name
        if selection not in _apps():
            print("The provided app name '{0}' is not available for installation.".format(selection))
            if input("Do you want to select another app? y/n").lower() == "y":
                selection = _select_app()
            else:
                logger.info("Aborted deployment.")

    if selection is not None:
        d = RTKWebDeployment(selection)
        d.prepare()
    else:
        logger.info("Invalid app selected for deployment.")
        logger.info("Aborted deployment.")


parser = argparse.ArgumentParser()
parser.add_argument("--prepare", "-p", help="Prepare an app for deployment: write config files and other resources.")
parser.add_argument("--create", "-c", help="Create and configure a target app.")
parser.add_argument("--destroy", "-rm", help="Destroy (permanently delete) an app.")
parser.add_argument("--init", "-i", help="Initialise a deployment (create new settings directory & file).")
parser.add_argument("--defaults", "-def", help="Use default configuration (taken from MCA app).", default=True)
parser.add_argument("--dummy", help="Execute a dummy deployment (don't overwrite Apache files).", default=False)
parser.add_argument("--deploy", "-d", help="Execute deployment steps (prepare->create).")

parser.add_argument("command")
parser.add_argument("--name")

if __name__ == "__main__":
    args = parser.parse_args()
    logger = logging.getLogger("RTKDeploy")
    logging.basicConfig(level=logging.DEBUG)

    if args.command == "new":
        _init_app(args, logger)

    elif args.command == "app":
        _deploy_app(args, logger)
