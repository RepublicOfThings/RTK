config = {
  "app": {
    "name": "{app_name}",
    "path": "{app_path}",
    "style": None,
    "image": None
  },

  "apache": {
    "path": "{apache_bitnami_path}",
    "template": "Include '{app_path}/{app_name}/conf/httpd-prefix.conf'"
  },

  "wsgi": {
    "conf": {
      "httpd-app.conf": "httpd-app-template.conf",
      "httpd-prefix.conf": "httpd-prefix-template.conf"
    }
  },

  "splunk": {
    "user": "{splunk_user}",
    "pwd": "{splunk_pwd}",
    "host": "{splunk_host}",
    "port": "{splunk_port}",
    "url": "http://{splunk_host}:{splunk_port}/en-US/account/insecurelogin?username={splunk_user}&password={splunk_pwd}&return_to=app/{app_name}/{dash}",
    "dashboards": {
      "homes": {
        "dash": "{homes_dashboard}",
        "app": "{homes_app}"
      },
      "alerts": {
        "dash": "{alerts_dashboard}",
        "app": "{alerts_app}"
      }
    }
  },

  "github": {
    "repo": "{app_repository}",
    "user": "{github_user}",
    "url": "https://github.com/{github_user}/{app_repository}"
  }

}
