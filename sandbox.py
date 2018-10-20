from rtk.utils.logs import build_log, rtk_log_fmt
import logging
import argparse
from rtk.core import commands


GITHUB_BASE = "https://github.com/republicofthings/RepublicWebApp"
DJANGO_BASE = "/home/republicuser/djangostack-2.0.3-0/apps/django/django_projects"
APACHE_BASE = "/home/republicuser/djangostack-2.0.3-0/apache2"
STACK_BASE = "/home/republicuser/djangostack-2.0.3-0"


# this is a transparent png file
CLIENT_LOGO = "{django_static}/content/placeholder.png"

logging.basicConfig(level=logging.DEBUG, format=rtk_log_fmt)

build_log.info("test", extra=dict(event="test", meta="other"))

parser = argparse.ArgumentParser("rtk-app")

subparsers = parser.add_subparsers(help="rtk-app subcommand help")

gen = subparsers.add_parser("add", help="generate help")
gen.add_argument("--client", required=True)
gen.add_argument("--name", required=True)
gen.add_argument("--project", default=None)
gen.add_argument("--splunk_port", default=8000, type=int)
gen.add_argument("--splunk_host", default="37.48.244.182", type=str)
gen.add_argument("--splunk_username", default="", type=str)
gen.add_argument("--splunk_password", default="", type=str)
gen.add_argument("--github_repo", default=GITHUB_BASE, type=str)
gen.add_argument("--stack_base", default=STACK_BASE, type=str)
gen.add_argument("--django_base", default=DJANGO_BASE, type=str)
gen.add_argument("--apache_base", default=APACHE_BASE, type=str)
gen.add_argument("--client_logo", default=CLIENT_LOGO, type=str)
gen.add_argument("--template", default="default", type=str)
gen.add_argument("--prompt", default=False, type=bool)
gen.set_defaults(func=commands.generate)


gen = subparsers.add_parser("activate", help="generate help")
gen.add_argument("--client", required=True)
gen.add_argument("--name", required=True)
gen.set_defaults(func=commands.activate)


if __name__ == "__main__":
    args = parser.parse_args()
    args.func(args)
