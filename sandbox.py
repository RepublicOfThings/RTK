from rtk.utils.logs import build_log, rtk_log_fmt
import logging
import argparse
from rtk.core import commands


GITHUB_BASE = "https://github.com/republicofthings/RepublicWebApp"
DJANGO_BASE = "/home/republicuser/djangostack-2.0.3-0/apps/django/django_projects"
APACHE_BASE = "/home/republicuser/djangostack-2.0.3-0/apache2"
STACK_BASE = "/home/republicuser/djangostack-2.0.3-0"


# this is a transparent png file
CLIENT_LOGO = "https://upload.wikimedia.org/wikipedia/commons/3/3a/TransparentPlaceholder.png"

logging.basicConfig(level=logging.DEBUG, format=rtk_log_fmt)

parser = argparse.ArgumentParser("rtk-app")

subparsers = parser.add_subparsers(help="rtk-app subcommand help")

gen = subparsers.add_parser("add", help="Add an application to a local cache ready for activation.")
gen.add_argument("-c", "--client", required=True, help="The name of the client the app will serve.")
gen.add_argument("-n", "--name", required=True, help="The name of the Django app.")
gen.add_argument("-p", "--project", default=None, help="The name of the Django Project the app will reside in. If left undefined, this will use the name of the app (recommended).")
gen.add_argument("-sp", "--splunk_port", default=8000, type=int, help="The Splunk port.")
gen.add_argument("-sh", "--splunk_host", default="37.48.244.182", type=str, help="The Splunk host.")
gen.add_argument("-susr", "--splunk_username", default="", type=str, help="A valid Splunk username.")
gen.add_argument("-spwd", "--splunk_password", default="", type=str, help="A valid Splunk passowrd.")
# gen.add_argument("--github_repo", default=GITHUB_BASE, type=str, help="An exposed Splunk port for a given dashboard.")
gen.add_argument("-bn", "--stack_base", default=STACK_BASE, type=str, help="The default path to the top-level Bitnami `djangostack` directory.")
gen.add_argument("-dj", "--django_base", default=DJANGO_BASE, type=str, help="The default path to the `django_projects` directory.")
gen.add_argument("-ap", "--apache_base", default=APACHE_BASE, type=str, help="The default path to the `apache2` directory")
gen.add_argument("-l", "--logo", default=CLIENT_LOGO, type=str, help="A path or URL to a client's logo.")
gen.add_argument("-t", "--template", default="default", type=str, help="The application template to use.", choices=['default','vodafone','cityverve'])
gen.add_argument("--prompt", default=False, type=bool, help="Optionally use a basic set of prompts to enter Splunk credentials and project details from the command line.")
gen.set_defaults(func=commands.generate)


superuser = subparsers.add_parser("superuser", help="generate help")
superuser.add_argument("--client", required=True)
superuser.add_argument("--name", required=True)
superuser.add_argument("--restart", default=False, type=bool)
superuser.set_defaults(func=commands.superuser)


activate = subparsers.add_parser("activate", help="generate help")
activate.add_argument("--client", required=True)
activate.add_argument("--name", required=True)
activate.add_argument("--restart", default=False, type=bool)
activate.set_defaults(func=commands.activate)


deactivate = subparsers.add_parser("deactivate", help="generate help")
deactivate.add_argument("--client", required=True)
deactivate.add_argument("--name", required=True)
deactivate.add_argument("--restart", default=False, type=bool)
deactivate.set_defaults(func=commands.deactivate)


build = subparsers.add_parser("build", help="generate help")
build.add_argument("--client", required=True)
build.add_argument("--name", required=True)
build.set_defaults(func=commands.build)


delete = subparsers.add_parser("delete", help="generate help")
delete.add_argument("--client", required=True)
delete.add_argument("--name", required=True)
delete.add_argument("--restart", default=False, type=bool)
delete.set_defaults(func=commands.delete)


restart = subparsers.add_parser("restart", help="generate help")
restart.add_argument("--client", required=True)
restart.add_argument("--name", required=True)
restart.set_defaults(func=commands.restart)


if __name__ == "__main__":
    args = parser.parse_args()
    args.func(args)
