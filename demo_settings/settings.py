# default RTKWebApp configuration for Republic of Things

SCHEMA = "http"

# APP_NAME -> The name of the app to be generated.
# APP_PATH -> The path to the django projects directory (where the App will be cloned to).
APP_NAME = "Demo"
APP_PATH = "./apps/django/django_projects"
STYLE = None
IMAGE = None

# APACHE_BITNAMI_PATH -> The path to the Apache Bitnami configuration directory.
APACHE_BITNAMI_PATH = "./apache2/conf/bitnami"

# Splunk Credentials
SPLUNK_USER = "admin"
SPLUNK_PWD = "my_password"
SPLUNK_HOST = "37.48.244.182"
SPLUNK_PORT = "8000"

# Splunk App Config
SPLUNK_HOMES_APP = "rot_smart_homes"
SPLUNK_HOMES_DASH = "demo_smeiling_dashboard"

SPLUNK_ALERT_APP = "rot_alert_manager"
SPLUNK_ALERT_DASH = "demo_alert_dashboard"

# Splunk Embedding Config
SPLUNK_URL = "{schema}://{host}:{port}/en-US/account/insecurelogin?username={user}&password={pwd}&return_to=app/{{app}}/{{dash}}"


# GitHub
GITHUB_REPO = "RTKWebAppProject"
GITHUB_USER = "markdouthwaite"
