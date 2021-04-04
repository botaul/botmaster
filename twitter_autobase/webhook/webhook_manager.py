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
def register_webhook(url: str, name: str, credential):
    print("Registering webhook...")
    activity = Activity(
        {
            'consumer_key'      : credential.CONSUMER_KEY,
            'consumer_secret'   : credential.CONSUMER_SECRET,
            'access_token'      : credential.ACCESS_KEY,
            'access_token_secret': credential.ACCESS_SECRET,
            'env_name'          : credential.ENV_NAME
        }
    )
    url += "/{}".format(name)
    print(activity.register_webhook(url))
    return activity.subscribe()

# Webhook server
class StreamEvent(Event):
    
    def __init__(self, stored_data: list):
        self.stored_data = stored_data
    
    @classmethod
    def set_callback(cls, callback_url: str):
        cls.CALLBACK_URL = callback_url
    
    @classmethod
    def update_credential_id(cls, credential_id: dict):
        cls.credential_id.update(credential_id)

    def on_data(self, data):
        if data is None:
            return
            
        self.stored_data.append(data)
        print(json.dumps(data, indent=2))

if __name__ == "__main__":
    import config
    from multiprocessing import Process
    from time import sleep
    from requests import post

    public_url = connect_ngrok(config.NGROK_AUTH_TOKEN)

    stored_data = list()

    stream_event = StreamEvent(stored_data)
    stream_event.set_callback(public_url+"/listener")
    stream_event.update_credential_id(
        {
            'darksiede' : config.CONSUMER_SECRET,
            'autobase_reborn' : ""
        }
    )
    
    p1 = Process(target=stream_event.listen)
    p1.start()

    # Wait server
    while post(public_url+"/listener/test").status_code != 200:
        sleep(1)

    register_webhook(public_url+"/listener", "darksiede", config)
    
    register_webhook(
        public_url+"/listener",
        "autobase_reborn",
        type(
            "data",
            (object,),
            {
                'CONSUMER_KEY'      : "",
                'CONSUMER_SECRET'   : "",
                'ACCESS_KEY'        : "",
                'ACCESS_SECRET'     : "",
                'ENV_NAME'          : ""  
            }
        )
    )

    p1.join()