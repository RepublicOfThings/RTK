# RTK

## Installation

Clone the repository from GitHub.

```
git clone https://github.com/RepublicOfThings/RTK
```

Follow any input requests as required.

Navigate into the RTK directory. Install the package:

```
sudo python3 setup.py install
```

## Deploying a Web App

(If starting from scratch)
0. Download and install RTK2 from GitHub (see above).

1. Copy the ```rtk_deploy.py``` script into the ```republicuser``` directory.

2. Initialise a new app configuration:

```
python3 rtk_deploy.py --init=TestApp --defaults=True
```

The ```--init``` flag is used to initialise a directory (in the current working directory) that
contains a file ```settings.py```. This file contains the basic configuration information
that *can* be modified by the user. The name of the app must be given.
Navigate to the ```TestApp_settings/settings.py``` file to check/update your app settings.

The ```--defaults``` flag indicates whether the settings should copy
the original app (i.e. the default configuration). If this is provided, the settings file will be largely
populated and only require the user to add a Splunk Username and Password.

3. Prepare deployment configuration:

```
python3 rtk_deploy.py --prepare=TestApp
```

This will produce a second directory (in the current working directory) that contains
all the templates and config files for the app. This is done so the configuration
can be inspected *before* deployment. It is essentially a debug step. Try not to manually change these files.

4. Deploy the app:

```
python3 rtk_deploy.rtk --deploy=TestApp
```


