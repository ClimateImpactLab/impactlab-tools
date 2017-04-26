"""
Utilities for path handling

Provides server-specific paths, configured in a server configuration file.
"""

import sys
import os
import yaml

default_server_config_path = "../server.yml"
server_config = None


# Path-handling functions

def sharedpath(subpath):
    """Return a subpath of the configured shareddir."""
    if server_config is None:
        msg = "Cannot find configuration file at {}".format(
            default_server_config_path)

        assert os.path.exists(default_server_config_path), msg

        use_config(get_file_config(default_server_config_path))

    return os.path.join(server_config['shareddir'], subpath)


def configpath(path):
    """Return an configured absolute path.  If the path is absolute, it
    will be left alone; otherwise, it is assumed to be a subpath of the
    configured `shareddir`."""

    if path[0] == '/':
        return path

    return sharedpath(path)


# Configuration-file handling functions

def use_config(config):
    """Use the given configuration for path functions."""
    global server_config

    if server_config is not None:
        for key in server_config:
            if key not in config:
                config[key] = server_config[key]

    server_config = config


def get_file_config(filepath):
    """Load a configuration file from a given path."""

    with open(filepath, 'r') as fp:
        config = yaml.load(fp)
        return config


def get_argv_config(index=1):
    """
    Load a configuration file specified as the `index` argv argument.

    In the future, this should also load specific configurable options from the
    command-line.
    """

    with open(sys.argv[index], 'r') as fp:
        config = yaml.load(fp)
        return config


if __name__ == '__main__':
    print(configpath('testing'))
