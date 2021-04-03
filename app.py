from twitter_autobase.main import Autobase
import config

User = Autobase(config)
if config.Database:
    User.start_database(config.Github_database)

User.start_autobase()