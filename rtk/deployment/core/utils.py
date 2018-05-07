

def configure_template(config, settings):
    config["app"]["name"] = settings.APP_NAME
    config["app"]["path"] = settings.APP_PATH
    config["app"]["style"] = settings.STYLE
    config["app"]["image"] = settings.IMAGE
    config["apache"]["path"] = settings.APACHE_BITNAMI_PATH
    print(config["apache"])
    config["apache"]["template"] = config["apache"]["template"].format(app_path=settings.APP_PATH,
                                                                       app_name=settings.APP_NAME)
    print(config["apache"], config["app"]["name"])
    config["splunk"]["user"] = settings.SPLUNK_USER
    config["splunk"]["pwd"] = settings.SPLUNK_PWD
    config["splunk"]["host"] = settings.SPLUNK_HOST
    config["splunk"]["port"] = settings.SPLUNK_PORT
    config["splunk"]["dashboards"]["homes"]["dash"] = settings.SPLUNK_HOMES_DASH
    config["splunk"]["dashboards"]["homes"]["app"] = settings.SPLUNK_HOMES_APP
    config["splunk"]["dashboards"]["alerts"]["dash"] = settings.SPLUNK_ALERT_DASH
    config["splunk"]["dashboards"]["alerts"]["app"] = settings.SPLUNK_ALERT_APP
    config["splunk"]["url"] = settings.SPLUNK_URL.format(user=settings.SPLUNK_USER,
                                                         pwd=settings.SPLUNK_PWD,
                                                         host=settings.SPLUNK_HOST,
                                                         port=settings.SPLUNK_PORT,
                                                         app="{app}",
                                                         dash="{dash}",
                                                         schema=settings.SCHEMA)

    config["github"]["user"] = settings.GITHUB_USER
    config["github"]["repo"] = settings.GITHUB_REPO
    config["github"]["url"] = config["github"]["url"].format(app_repository=settings.GITHUB_REPO,
                                                             github_user=settings.GITHUB_USER)


    return config
