import os

import toml

config = \
    toml.load(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + '/configs/apiserver.toml')[
        "TestDatabase"]


def get_test_database_config():
    return config
