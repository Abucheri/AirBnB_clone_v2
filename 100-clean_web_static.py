#!/usr/bin/python3
"""
Fabric script to clean up old archives.
"""

from fabric.api import env, local, run
from pathlib import Path


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
    try:
        number = int(number)
    except ValueError:
        print("Error: 'number' must be an integer.")
        return

    if number < 0:
        print("Error: 'number' must be a non-negative integer.")
        return

    # Local cleanup
    local("ls -1t versions | tail -n +{} | xargs -I {{}} rm versions/{{}}"
          .format(number + 1))

    # Remote cleanup
    releases_path = "/data/web_static/releases"
    releases = run("ls -1t {} | tail -n +{}"
                   .format(releases_path, number + 1)).split('\n')

    for release in releases:
        run("rm -rf {}/{}".format(releases_path, release))

    # Remove dangling symlink
    current_path = "/data/web_static/current"
    current_release = run("readlink {} | xargs -I {{}} basename {{}}"
                          .format(current_path), quiet=True)

    if current_release not in run("ls -1 {}"
                                  .format(releases_path), quiet=True):
        run("rm -rf {}".format(current_path))
