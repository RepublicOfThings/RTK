"""
python deployer.py prepare --default # generate the new App configuration. (default flag deploys to current directory)
>> Directory: ...

python deployer.py create # deployment an RTKWebApp according to the provided config.

"""

import logging

target = "Include '/home/republicuser/djangostack-2.0.3-0/apps/django/django_projects/clean/conf/httpd-prefix.conf'"
with open("example") as file:
    data = ""
    for line in file:
        if line.replace("\n", "").strip() != target.replace("\n", "").strip():
            data += line
        else:
            print(line)

    open("cleaned", "w").write(data)
