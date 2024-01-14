#!/usr/bin/python3
"""
Fabric script to create and distribute an archive to web servers.
"""

from fabric.api import env, run, put, local
from datetime import datetime
from os.path import exists

env.hosts = ['54.210.107.201', '54.237.76.82']
env.user = 'ubuntu'


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        str: Archive path if successful, otherwise None.
    """
    try:
        local("mkdir -p versions")
        archive_path = "versions/web_static_{}.tgz".format(
                datetime.utcnow().strftime("%Y%m%d%H%M%S"))
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception as e:
        print(e)
        return None


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


def deploy():
    """
    Calls do_pack and do_deploy functions to create and distribute the archive.

    Returns:
        bool: True if successful, False otherwise.
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
