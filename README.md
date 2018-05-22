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

1. Copy the ```deploy.py``` script into the ```republicuser``` directory (if it isn't already there!).

2. Prepare a new app configuration:

```
python deploy.py add
```

This will prompt you to create a new app settings file in the ```.rtk_deployment/{app_name}/app``` folder.
You should review this ```settings.py``` file before continuing. For additional arguments use the ```--help`` flag.

If you make changes to the ```settings.py``` app, make sure to run the following command **before** activating your app:

```
python deploy.py update
```

Note that if you deploy before updating the configuration, the changes won't be propagated to your app when it's deployed.

If you make a mistake and deploy, or change your mind about the configuration after deployment, use the following:

```
python deploy.py remove
```

Select your target app, and when prompted to delete your app configuration (the second y/n option), select no. Then use ```update``` and redeploy your app.

3. Next, activate the app. This will clone the app from GitHub, write the code for your new app, and then restart the Apache server. This can be achieved with the following:

```
python deploy.py activate
```

4. Deactivating an app can also be achieved. This will remove the app from the apache server but preserve the django app in the ```django_projects``` directory. This can be done with:

```
python deploy.py deactivate
```

5. A deactivated app can be reactivated (restored to apache server) with:

```
python deploy.py reactivate
```

6. Finally, an app can be deleted with the following:

```
python deploy.py remove
```

### Additional Notes

* Only apps installed in the ```.rtk_deployment``` directory can be manipulated with the ```deploy.py``` script. Make sure to add and remove apps only with this script.
* The RTKApp object can be used to generically create apps in pure Python code. Feel free to experiment!

### Example - DemoApp

Initialise a new app (note that the optional --target flag avoids command line prompt for a name).
```
python deploy.py add --target=demo_app
```

Edit the ```.rtk_deployment/demo_app/app/settings.py``` file to make it point to your target splunk dashes etc. Don't forget the quotation marks when changing stuff!

Activate the app as follows:

```
python deploy.py activate --target=demo_app
```

Now navigate to ```www.smeiling.co.uk:8080/demo_app``` -- it should be live!

