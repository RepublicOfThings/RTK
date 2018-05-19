# Template for Republic Web App (SmEILing)
# see rtk/deployment/templates/defaults.py

SCHEMA = "http"

# APP_NAME -> The name of the app to be generated.
# APP_PATH -> The path to the django projects directory (where the App will be cloned to).
APP_NAME = "{app_name}"
APP_PATH = "{path_to_app_directory}"

STYLE = None
LOGO = None

# BITNAMI TOPLEVEL
CTLSCRIPT = "{ctlscript}"

# APACHE_BITNAMI_PATH -> The path to the Apache Bitnami configuration directory.
APACHE_BITNAMI_PATH = "{path_to_bitnami_config}"

# Splunk Credentials
SPLUNK_USER = "{splunk_user}"
SPLUNK_PWD = "{splunk_password}"
SPLUNK_HOST = "{splunk_host}"
SPLUNK_PORT = "{splunk_port}"

# Splunk App Config
SPLUNK_HOMES_APP = "{homes_app}"
SPLUNK_HOMES_DASH = "{homes_dashboard}"

SPLUNK_ALERT_APP = "{alert_app}"
SPLUNK_ALERT_DASH = "{alert_dashboard}"

# GitHub
GITHUB_REPO = "{github_repository}"
GITHUB_USER = "{github_user}"

# !!!! DO NOT EDIT !!!!

# Splunk Embedding Config
SPLUNK_URL = "{schema}://{host}:{port}/en-US/account/insecurelogin?username={user}&password={pwd}&return_to=app/{{app}}/{{dash}}"

# ...