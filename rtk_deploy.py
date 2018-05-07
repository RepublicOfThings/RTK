from rtk.deployment import RTKWebDeployment
import argparse
import logging


"""
Creating an App

The creation process is broken into 3 steps: Generating User Settings, Generating Deployment Configuration,
and then the creation and configuration of the app itself. It is recommended that for initial deployments,
each of these steps is executed separately and the output of each step checked. For subsequent deployments,
the --deploy flag can be used to execute steps 2 & 3 together. 

1. Generate the App's settings directory.
    ``` python rtk_deploy.py --init=example ``` (initialises settings for app 'example')
    
    This can be done manually be creating a directory 'APPNAMEHERE_settings', and adding a 'settings.py' to this. 
    Or, use the --init flag to auto-populate this directory.
    The settings.py file in this directory will be used to generate the app. Make sure all the information is correct.
    This file is the *only* file that should be edited by a user. Inspect deployment configurations to check everything
    is correct, but don't edit them!

2. Generate the App's deployment configuration.
    ``` python rtk_deploy.py --prepare=example ``` (generates configuration for app 'example')
    This step generates the config files for the app. It's worth checking these files are fully populated. Remember:
    avoid editing them unless you know precisely what you're doing.
    
3. Create the App.
    ``` python rtk_deploy.py --prepare=example ``` (generates configuration for app 'example')


Auto-deploy.
    Provided a settings.py file is available, this will role steps 2&3 together. Deployment would then be:
    If necessary run the initialisation code:
    ``` python rtk_deploy.py --init=example ``` (initialises settings for app 'example' -- this only needs to be run once!)
    If the initialisation step has already been run, execute deployment!
    ``` python rtk_deploy.py --deploy=example ``` (deploys the app!)

"""

parser = argparse.ArgumentParser()
parser.add_argument("--prepare", help="Prepare an app for deployment: write config files and other resources.")
parser.add_argument("--create", help="Create and configure a target app.")
parser.add_argument("--destroy", help="Destroy (permanently delete) an app.")
parser.add_argument("--settings", help="Path to the app's settings folder.", default="./{app_name}_settings/settings.py")
parser.add_argument("--init", help="Initialise a deployment (create new settings directory & file).")
parser.add_argument("--defaults", help="Use default configuration (taken from MCA app).", default=False)
parser.add_argument("--deploy", help="Execute deployment steps (prepare->create).")

if __name__ == "__main__":
    args = parser.parse_args()
    logger = logging.getLogger("RTKDeploy")
    logging.basicConfig(level=logging.DEBUG)

    if args.prepare is not None:
        app = args.prepare
        logger.info("Preparing app: {0}".format(app))
        d = RTKWebDeployment(app)
        if args.settings == "./{app_name}_settings/settings.py":
            d.prepare(settings=args.settings.format(app_name=app))
        else:
            d.prepare(settings=args.settings)

    elif args.create is not None:
        app = args.create
        logger.info("Creating app: {0}".format(app))
        d = RTKWebDeployment(app)
        d.create()

    elif args.destroy is not None:
        app = args.destroy
        logger.info("Destroying app: {0}".format(app))
        d = RTKWebDeployment(app)
        d.destroy()

    elif args.init is not None:
        app = args.init
        logger.info("Initialising app: {0}".format(app))
        d = RTKWebDeployment(app)
        d.initialise(use_defaults=args.defaults)

    elif args.deploy is not None:
        app = args.deploy
        logger.info("Deploying app: {0}".format(app))
        d = RTKWebDeployment(app)
        if args.settings == "./{app_name}_settings/settings.py":
            d.prepare(settings=args.settings.format(app_name=app))
        else:
            d.prepare(settings=args.settings)
        d.create()
