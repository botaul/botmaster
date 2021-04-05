import json
from .twitivity import Event, Activity
from pyngrok import ngrok

# Connect ngrok
def connect_ngrok(ngrok_auth_token: str) -> str:
    ngrok.set_auth_token(ngrok_auth_token)
    ngrok_tunnel = ngrok.connect(5000)
    public_url = (ngrok_tunnel.public_url).replace("http", "https")
    print("NGROK URL: {}".format(public_url))
    
    return public_url

# Register webhook
def register_webhook(url: str, name: str, credential, delLastWeb=True):

    activity = Activity(
        {
            'consumer_key'      : credential.CONSUMER_KEY,
            'consumer_secret'   : credential.CONSUMER_SECRET,
            'access_token'      : credential.ACCESS_KEY,
            'access_token_secret': credential.ACCESS_SECRET,
            'env_name'          : credential.ENV_NAME
        }
    )
    # delete the last active webhook
    if delLastWeb is True:
        for environment in activity.webhooks()['environments']:
            if environment['environment_name'] == activity.env_name:
                if len(environment['webhooks']):
                    webhook_id = environment['webhooks'][0]['id']
                    activity.delete(webhook_id)
                    break

    url += "/{}".format(name)
    print(activity.register_webhook(url))
    return activity.subscribe()

# Webhook server
class StreamEvent(Event):
    '''
    :param func_data: function (contains only 1 argument) that will be called when webhook receives data
    :param subscribe: list of (str) subscriptions that will be subscribed.\
    see more on: https://developer.twitter.com/en/docs/twitter-api/enterprise/account-activity-api/guides/account-activity-data-objects
    '''
    
    def __init__(self, func_data, subscribe):
        self.func_data = func_data
        self.subcriptions = subscribe
    
    @classmethod
    def set_callback(cls, callback_url: str):
        cls.CALLBACK_URL = callback_url
    
    @classmethod
    def update_credential_id(cls, credential_id: dict):
        cls.credential_id.update(credential_id)

    def on_data(self, data: json):
        if data is None:
            return
        for x in self.subcriptions:
            if x in data:
                self.func_data(data)
                break

if __name__ == "__main__":
    import config
    from multiprocessing import Process
    from time import sleep
    from requests import post

    public_url = connect_ngrok(config.NGROK_AUTH_TOKEN)

    def func_data(data):
        print(json.dumps(data, indent=2))

    stream_event = StreamEvent(
        func_data,
        [
            'direct_message_events',
        ]
    )
    
    stream_event.set_callback(public_url+"/listener")
    stream_event.update_credential_id(
        {
            'darksiede' : config.CONSUMER_SECRET,
            'autobase_reborn' : config.CONSUMER_SECRET_2,
        }
    )
    
    p1 = Process(target=stream_event.listen)
    p1.start()

    # Wait server
    while post(public_url+"/listener/test").status_code != 200:
        sleep(1)

    register_webhook(
        public_url+"/listener",
        "darksiede",
        type(
            "data",
            (object,),
            {
                'CONSUMER_KEY'      : config.CONSUMER_KEY,
                'CONSUMER_SECRET'   : config.CONSUMER_SECRET, 
                'ACCESS_KEY'        : config.ACCESS_KEY,
                'ACCESS_SECRET'     : config.ACCESS_SECRET,
                'ENV_NAME'          : config.ENV_NAME,
            }
        )
    )
    
    register_webhook(
        public_url+"/listener",
        "autobase_reborn",
        type(
            "data",
            (object,),
            {
                'CONSUMER_KEY'      : config.CONSUMER_KEY_2,
                'CONSUMER_SECRET'   : config.CONSUMER_SECRET_2, 
                'ACCESS_KEY'        : config.ACCESS_KEY_2,
                'ACCESS_SECRET'     : config.ACCESS_SECRET_2,
                'ENV_NAME'          : config.ENV_NAME_2,
            }
        )
    )

    p1.join()