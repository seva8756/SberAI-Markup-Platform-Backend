import os

import toml

from app.utils import utils

config = \
    toml.load(utils.get_project_root() + '/configs/apiserver.toml')[
        "TestDatabase"]


def get_test_database_config():
    return config
