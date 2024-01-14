#!/usr/bin/python3
"""
Fabric script to create and distribute an archive to web servers.
"""

from fabric.api import env, run, put, local, execute
from datetime import datetime
import os.path
from functools import lru_cache

env.hosts = ['54.210.107.201', '54.237.76.82']
env.user = 'ubuntu'


@lru_cache(maxsize=None)
def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        str: Archive path if successful, otherwise None.
    """
    dtime = datetime.utcnow()
    file_path = "versions/web_static_{}{}{}{}{}{}.tgz".format(dtime.year,
                                                              dtime.month,
                                                              dtime.day,
                                                              dtime.hour,
                                                              dtime.minute,
                                                              dtime.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file_path)).failed is True:
        return None
    return file_path


def do_deploy(archive_path):
    """
    Distributes an archive to web servers.

    Args:
        archive_path (str): Path to the archive to deploy.

    Returns:
        bool: True if successful, False otherwise.
    """
    if os.path.isfile(archive_path) is False:
        return False
    file_path = archive_path.split("/")[-1]
    name = file_path.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file_path)).failed is True:
        return False

    if run("rm -rf /data/web_static/releases/{}/".
            format(name)).failed is True:
        return False

    if run("mkdir -p /data/web_static/releases/{}/".
            format(name)).failed is True:
        return False

    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
            format(file_path, name)).failed is True:
        return False

    if run("rm /tmp/{}".format(file_path)).failed is True:
        return False

    if run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".
            format(name, name)).failed is True:
        return False

    if run("rm -rf /data/web_static/releases/{}/web_static".
            format(name)).failed is True:
        return False

    if run("rm -rf /data/web_static/current").failed is True:
        return False

    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
            format(name)).failed is True:
        return False
    return True


def deploy():
    """
    Calls do_pack and do_deploy functions to create and distribute the archive.

    Returns:
        bool: True if successful, False otherwise.
    """
    file_path = do_pack()
    if file_path is None:
        return False
    return do_deploy(file_path)
