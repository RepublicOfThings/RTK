"""
python deployer.py prepare --default # generate the new App configuration. (default flag deploys to current directory)
>> Directory: ...

python deployer.py create # deployment an RTKWebApp according to the provided config.

"""

import logging
from rtk.deployment import RTKApp

logging.basicConfig(level=logging.DEBUG)

app = RTKApp("demo", mode="dummy")
app.build(default=True)
app.configure()
app.deploy()
