"""
python deployer.py prepare --default # generate the new App configuration. (default flag deploys to current directory)
>> Directory: ...

python deployer.py create # deployment an RTKWebApp according to the provided config.

"""

import logging
from rtk.deployment import RTKApp
import re

logging.basicConfig(level=logging.DEBUG)

content = open("test.py").read()
print(content)
content = re.sub("{app_name}", "DemoWebApp", content)
print(content)
content = re.sub("{project}", "demo", content)
print(content)

# app = RTKApp("demo", mode="live")
# app.build(default=True)
# print(app.project)


# app.configure()
# app.deploy()
