#!/usr/bin/python3
"""
Fabric script to clean up old archives.
"""

from fabric.api import *
import os


env.hosts = ['54.210.107.201', '54.237.76.82']
env.user = 'ubuntu'


def do_clean(number=0):
    """
    Deletes out-of-date archives.

    Args:
        number (int): The number of archives to keep.
                      If 0 or 1, keep only the most recent version.
                      If 2, keep the most recent and second most recent
                        versions, and so on.
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]
    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
