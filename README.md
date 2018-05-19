# RTK

## Notes

* This documentation assumes that the default python version on the system is Python 3. If this is not the case, make sure to substitute ```python``` with ```python3``` in terminal commands.
* There are currently *no* overwrite protections built-in. Make sure you don't accidentally overwrite any files!

## Installation

Clone the repository from GitHub.

```
git clone https://github.com/RepublicOfThings/RTK
```

Follow any input requests as required.

Navigate into the RTK directory. Install the package:

```
sudo python setup.py install
```

## Deploying a Web App

(If starting from scratch)
0. Download and install RTK2 from GitHub (see above).

1. Copy the ```deploy.py``` script into the ```republicuser``` directory.

2. Prepare a new app configuration:

```
python deploy.py new
```

This will prompt you to create a new app settings file in the ```.rtk_deployment/{app_name}/app``` folder.
You should review this ```settings.py``` file before continuing. For additional arguments use the ```--help`` flag.

3. Next, deploy the app. This can be achieved with the following:

```
python deploy.py app
```


### Example - DemoApp

Initialise a new app (note that the optional --name flag avoids command line prompt for a name).
```
python deploy.py new
```

This will produce the following interaction:

```
INFO:RTKDeploy:Initialising a new app...
App Name:DemoApp
Configure splunk now? y/ny
Splunk username:republic
Splunk password:
INFO:RTKDeploy:Prepared your new app for deployment.
```

Next up, check the settings file at `.rtk_deployment/DemoApp/app/settings.py`, then its time to deploy! Given there is only one app prepared, you will see the following:

```
python deploy app
INFO:RTKDeploy:Preparing for deployment...
Deploy 'DemoApp'? y/n y
INFO:RTKWebDeployment:Preparing your app configuration file...
INFO:RTKWebDeployment:App configuration is ready.
INFO:RTKWebDeployment:Preparing your apache configuration files...
INFO:RTKWebDeployment:Writing httpd-app-template...
INFO:RTKWebDeployment:Writing httpd-prefix-template...
INFO:RTKWebDeployment:Apache configuration templates are ready.

```
