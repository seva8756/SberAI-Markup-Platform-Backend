import toml

import app

config = toml.load('configs/apiserver.toml')
app.start(app.config.Config(config))
