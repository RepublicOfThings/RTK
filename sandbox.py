"""
python deployer.py prepare --default # generate the new App configuration. (default flag deploys to current directory)
>> Directory: ...

python deployer.py create # deployment an RTKWebApp according to the provided config.

"""


with open("bangers.txt") as bangers:
    data = ""

    for line in bangers:
        if line != "\n":
            data += line


    print(data)