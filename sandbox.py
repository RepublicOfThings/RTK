"""
python deployer.py prepare --default # generate the new App configuration. (default flag deploys to current directory)
>> Directory: ...

python deployer.py create # deployment an RTKWebApp according to the provided config.

"""

from rtk.deployment import RTKWebDeployment

d = RTKWebDeployment("demo")
d.prepare(settings="./demo_settings/settings.py")

d.create()

# need to write apache config code.