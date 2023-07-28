from app import Config


def TestConfig() -> Config.flask:
    c = Config({
        "LOG_LEVEL": "DEBUG",
        "Database": {},
        "Flask": {
            "DEBUG": True,
            "JWT_SECRET_KEY": "e77a7f4d56fcn76d38075b60061621be1c2d9a81e77a7f"
        }
    }).flask
    return c
