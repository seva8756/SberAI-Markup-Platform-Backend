from datetime import timedelta


class FlaskConfig:
    DEBUG = False
    CSRF_ENABLED = True  # Включение защиты против "Cross-site Request Forgery (CSRF)"
    JWT_SECRET_KEY = ""  # Случайный ключ, для подписи JWT
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    def __init__(self, settings: dict[str, str]):
        self.DEBUG = settings['DEBUG']
        self.JWT_SECRET_KEY = settings['JWT_SECRET_KEY']


class Config(object):
    log_level: str = "DEBUG"
    database: object = None
    flask: FlaskConfig = None

    def __init__(self, config: dict[str, str]):
        self.flask = FlaskConfig(config['Flask'])
        self.database = config['Database']
        self.log_level = config['LOG_LEVEL']
