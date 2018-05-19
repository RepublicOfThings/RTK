# default RTKWebApp configuration for Republic of Things

SCHEMA = "http"

# APP_NAME -> The name of the app to be generated.
# APP_PATH -> The path to the django projects directory (where the App will be cloned to).
APP_NAME = "{app_name}"
APP_PATH = "/home/republicuser/djangostack-2.0.3-0/apps/django/django_projects"
STYLE = None
LOGO = None

# BITNAMI TOPLEVEL
CTLSCRIPT = "/home/republicuser/djangostack-2.0.3-0/ctlscript.sh"

# APACHE_BITNAMI_PATH -> The path to the Apache Bitnami configuration directory.
APACHE_BITNAMI_PATH = "/home/republicuser/djangostack-2.0.3-0/apache2/conf/bitnami"

# Splunk Credentials
SPLUNK_USER = "{splunk_user}"
SPLUNK_PWD = "{splunk_password}"
SPLUNK_HOST = "37.48.244.182"
SPLUNK_PORT = "8000"

# Splunk App Config
SPLUNK_HOMES_APP = "rot_smart_homes_app"
SPLUNK_HOMES_DASH = "smeiling_dashboard_mca_v10_splunk"

SPLUNK_ALERT_APP = "alert_manager"
SPLUNK_ALERT_DASH = "incident_posture_clone_v10"

# Splunk Embedding Config
SPLUNK_URL = "{schema}://{host}:{port}/en-US/account/insecurelogin?username={user}&password={pwd}&return_to=app/{{app}}/{{dash}}"

# GitHub
GITHUB_REPO = "RTKWebApp"
GITHUB_USER = "republicofthings"
