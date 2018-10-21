# RTK2

Author: Mark Douthwaite
Contact: mark@douthwaite.io
Version: 2.0.3

## Purpose

This package provides tools and utilities for the development and deployment of standardised Django-based web applications
with embedded Splunk dashboards. In particular, it supplies the `rtk-app` command line tool for _automating_ the deployment
of these applications on a target system.

## Features

The principle features of RTK2 are:

*  Automated deployment tools with minimal

## Workflow

### 0 Installation

Note: this section should be unnecessary (hence '0') -- the latest version of RTK should always be installed on the target system.

1) Clone the package from GitHub:

```commandline
 git clone https://github.com/RepublicOfThings/RTK RTK2
```

2) Navigate to the package directory, and switch to the RTK2 development branch.
```commandline
cd RTK2
git checkout develop
```

3) Run the setup script in this directory.
```commandline
python3 setup.py install
```

After a few moments, you should have the latest version of RTK installed!

### 1 Adding an App

Adding an app can be achieved as follows:

```commandline
rtk-app add --name={app_name} --client={client_name} --template={template_name}  
```

Where `--name` indicates the name of the application, `--client` indicates the client for which the app will be deployed.
These two arguments are seperate to help enable multiple apps to be managed and deployed per client. See the 'App Cache Structure'
section below for more details.

The `--template` argument indicates which template app to use. RTK2 is designed to support using arbitrarily many templates
to specify the style of application. See the 'Available Templates' section for more details.

### 2 Activating an App

To activate an app, run the following:

```commandline
rtk-app activate --name={app_name} --client={client_name}  
```

This will generate a project in your `django_projects` directory (wherever that may be). It will also add the app to
the Apache config files (where appropriate). Currently, re-running an `add` command with the same `--client` and `--name`
arguments will **overwrite** configurations within the `.rtk_cache` -- make sure to be careful to use unique names.

To make the changes live, perform a restart:

```commandline
rtk-app restart --name={app_name} --client={client_name}  
```

### 3 Deactivating an App

To deactivate an app (i.e. take it offline, but without deleting the project itself), run the following:

```commandline
rtk-app deactivate --name={app_name} --client={client_name}  
```

To make the changes live, perform a restart:

```commandline
rtk-app restart --name={app_name} --client={client_name}  
```

### 4 Deleting an App

If you need to delete the app run the following:

```commandline
rtk-app delete --name={app_name} --client={client_name}  
```

This may need to be done if you make changes to the application's `.rtk_cache` configuration file.

This **will not** delete the application from the `.rtk_cache`. This is because you can simply overwrite the config files
in here by re-running the `add` step.

To make the changes live, perform a restart:

```commandline
rtk-app restart --name={app_name} --client={client_name}  
```

### Notes

As of version 2.0.3, the `--restart=True` argument can be passed to the `activate`, `deactivate`, and `delete` commands.

#### App Cache Structure

Prior to `activation`, the configuration of an application in stored in the `.rtk_cache` hidden directory. The configuration
is specified in a YAML file. 

```
+ .rtk_cache
    + {client-0}
        - {name-0}.yml
        - {name-1}.yml
        ...
    + {client-0}
        - {name-0}.yml
        - {name-1}.yml
        ...       
``` 

#### Configuration File

**Note: To see any changes to the configuration file take effect will require the re-deployment of the application.**

Before running the `activate` command, you should confirm the file you've generated meets your needs. An example config
file is shown below. Make sure the `splunk: username` and `splunk: password` keys are populated. The application itself
is specified under the `application` key. This manages the styles, logos and dashboards that will be visible in the
Django application.

```yaml
client: random_council

setup:
    splunk:
        port: 8000
        host: 37.48.244.182
        username: username
        password: password
        url_template: http://{host}:{port}/en-US/account/insecurelogin?username={user}&password={pwd}&return_to=app/{app}/{dash}

    paths:
        django_base: /home/republicuser/djangostack-2.0.3-0/apps/django/django_projects
        ...

application:
    name: random_council_app
    project: random_council
    style: https://upload.wikimedia.org/wikipedia/commons/3/3a/TransparentPlaceholder.png
        css: /random_council/random_council/static/app/content/republic.css
        logo: /random_council/random_council/static/app/content/placeholder.png
        republic: /random_council/random_council/static/app/republic_logo.png
        smeiling: /random_council/random_council/static/app/smeiling_logo.png

    dashboards: 
      Alerts:
          url: random_council/dashboard/alerts/
          dash: incident_posture_clone_v10
          app: alert_manager
      Connected Homes:
          url: random_council/dashboard/otherhomes/
          dash: smeiling_dashboard_mca_v10_splunk
          app: rot_smart_homes_app
```

Adding dashboards can be achieved as follows:

```yaml
    dashboards:
      Alerts:
        ...
      Connected Homes:
        ...
      Even More Connected Homes:
          url: random_council/dashboard/otherhomes/
          dash: smeiling_dashboard_mca_v10_splunk
          app: rot_smart_homes_app
```

Image ![](/Users/MarkDouthwaite/Documents/GitHub/RTK/dashboards.png)

#### Templates

Template|Description
:----:|:----:
default|A very basic template with no defined dashboard and placeholder branding.
vodafone|A Vodafone-branded app with a single dashboard.
cityverve|A CityVerve-branded ap with two dashboards (Alerts, Connected Homes).


#### Additional Arguments

The `rtk-app` tool provides an extensive set of flags to help customise your application, including:

```
  --client CLIENT
  --name NAME
  --project PROJECT
  --splunk_port SPLUNK_PORT
  --splunk_host SPLUNK_HOST
  --splunk_username SPLUNK_USERNAME
  --splunk_password SPLUNK_PASSWORD
  --github_repo GITHUB_REPO
  --stack_base STACK_BASE
  --django_base DJANGO_BASE
  --apache_base APACHE_BASE
  --client_logo CLIENT_LOGO
  --template TEMPLATE
  --prompt PROMPT
```

To get more information on these arguments, simply run the following:

```commandline
rtk-app add -h
```

#### Adding Command Line Prompts

A possible alternative to command line arguments is to enable the command line prompts functionality of `rtk-app`. To
do this, add the `--prompt=True` flag to your `add` command. This will let you enter the Splunk username and password
for an app here instead.

```commandline
rtk-app add --name={app_name} --client={client_name} --template={template_name} --prompt=True
>>> Please enter your Splunk username: ...
>>> Please enter your Splunk password: ...
>>> Please enter a name for your project: ...
```
