#!/usr/bin/python3
"""
Fabric script to generate a .tgz archive from
the contents of the web_static folder.
"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Creates a .tgz archive from web_static folder.

    Returns:
        str: Archive path if successful, None otherwise.
    """
    # Create the versions folder if it doesn't exist
    local("mkdir -p versions")

    # Generate the archive path
    time_format = "%Y%m%d%H%M%S"
    archive_path = "versions/web_static_{}.tgz".format(
            datetime.utcnow().strftime(time_format)
            )
    # Compress web_static contents into the archive
    result = local("tar -cvzf {} web_static".format(archive_path))

    # Check if the archiving was successful
    if result.failed:
        return None
    return archive_path


if __name__ == "__main__":
    archive_path = do_pack()
    if archive_path:
        print("web_static packed: {} -> {}Bytes\nDone.".format(
            archive_path, os.path.getsize(archive_path)))
    else:
        print("Packing web_static failed.")
