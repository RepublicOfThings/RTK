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
content = re.sub(r"{__SECRET_KEY__}", 'key', content)
content = re.sub(r"{__PROJECT__}", 'test', content)
print(content)

# app = RTKApp("demo", mode="live")
# app.build(default=True)
