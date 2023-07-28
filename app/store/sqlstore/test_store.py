import os

import toml

config = \
    toml.load(os.getcwd() + '/configs/apiserver.toml')[
        "TestDatabase"]


def get_test_database_config():
    return config
