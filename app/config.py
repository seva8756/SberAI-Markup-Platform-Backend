import toml


class FlaskConfig:
    DEBUG = False
    CSRF_ENABLED = True  # Включение защиты против "Cross-site Request Forgery (CSRF)"
    SECRET_KEY = ""  # Случайный ключ, которые будет исползоваться для подписи данных, например cookies.

    def __init__(self, settings: object):
        self.DEBUG = settings['DEBUG']
        self.SECRET_KEY = settings['SECRET_KEY']


class Config(object):
    Log_Level: str = "DEBUG"
    Database: object = None
    Flask: FlaskConfig = None

    def __init__(self, config_path='configs/apiserver.toml'):
        config = toml.load(config_path)

        self.Flask = FlaskConfig(config['Flask'])
        self.Database = config['Database']
        self.Log_Level = config['LOG_LEVEL']
