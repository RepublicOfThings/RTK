"""
python deployer.py prepare --default # generate the new App configuration. (default flag deploys to current directory)
>> Directory: ...

python deployer.py create # deployment an RTKWebApp according to the provided config.

"""

import os
import subprocess
# os.mkdir(".toaster")
subprocess.call(["chmod", "777", ".toaster"])

from rtk.deployment import RTKWebDeployment

# d = RTKWebDeployment("demo")

# d.destroy()

# d.prepare(settings="./demo_settings/template.py")
# d.create()

# need to write apache config code.