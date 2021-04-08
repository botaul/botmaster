# v1.7.x candidate

from twitter_autobase import Autobase
from twitter_autobase import webhook_manager as webMan
from threading import Thread
import config
from requests import post
from time import sleep

User = Autobase(config)
if config.Database:
    User.start_database(config.Github_database)

autobase = Thread(target=User.start_autobase)
autobase.start()

# SETTING NGROK AND WEBHOOK SERVER
url = webMan.connect_ngrok(config.NGROK_AUTH_TOKEN)
server = webMan.server_config(
    url=url+"/listener",
    dict_credential={
        User.bot_username : config.CONSUMER_SECRET,
    },
    dict_func={
        User.bot_id : User.update_dms,
    },
    subscribe=[
        'direct_message_events',
    ]
)
webhook = Thread(target=server.listen)
webhook.start()

# TEST SERVER
while post(url+"/listener/test").status_code != 200:
    sleep(1)

# REGISTER WEBHOOK
webMan.register_webhook(url+"/listener", User.bot_username, config)

