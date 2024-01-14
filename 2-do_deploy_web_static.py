#!/usr/bin/python3
"""
Fabric script to deploy an archive to web servers.
"""

from fabric.api import env, run, put, local
from os.path import exists
from datetime import datetime
from fabric.operations import sudo


env.hosts = ['54.210.107.201', '54.237.76.82']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Distributes an archive to web servers.

    Args:
        archive_path (str): Path to the archive to deploy.

    Returns:
        bool: True if successful, False otherwise.
    """
    if not exists(archive_path):
        return False
    try:
        archive_name = archive_path.split("/")[-1]
        archive_no_ext = archive_name.split(".")[0]

        # Upload the archive to /tmp/ directory on the web server
        put(archive_path, '/tmp/')

        # Create the release folder
        run('mkdir -p /data/web_static/releases/{}'.format(archive_no_ext))

        # Uncompress the archive
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.
            format(archive_name, archive_no_ext))

        # Delete the archive
        run('rm /tmp/{}'.format(archive_name))

        # Move contents to the proper location
        run('mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'.
            format(archive_no_ext, archive_no_ext))

        # Remove the web_static folder
        run('rm -rf /data/web_static/releases/{}/web_static'.
            format(archive_no_ext))

        # Delete the current symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.
            format(archive_no_ext))

        print('New version deployed!')
        return True
    except Exception as e:
        print(e)
        return False
