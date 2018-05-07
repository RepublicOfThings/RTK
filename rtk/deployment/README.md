# RTK.DEPLOYMENT

The RTK deployment module provides tools for the deployment of SmEILing Web Apps.

## Deploying an App

1. Create a folder in your home directory (on republic_user, this is the directory with djangostack-2.0.3-0 in it) called `{appname}_settings`.
At this stage, try to use only lower case versions of the app's name. For example, this may be `demo_settings`.
2. In this folder, create a file `settings.py`. Place all your settings for the project in this file. For an example template that
would deploy the app `demo` see the `example.txt` file in the `rtk/deployment/resources/` directory.
3.