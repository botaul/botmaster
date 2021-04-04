import os
from twitter_autobase import webhook_manager as wman
from multiprocessing import Process
from requests import post
from time import sleep


print("creating ngrok process...")
public_url = wman.connect_ngrok(os.environ.get("NGROK_AUTH_TOKEN"))
assert "https" in public_url


print("creating server...")
stored_data = list()
    
stream_event = wman.StreamEvent(stored_data)
stream_event.set_callback(public_url+"/listener")
stream_event.update_credential_id(
    {
        'Darksiede1': os.environ.get("CONSUMER_SECRET"),
        'autobase_reborn': os.environ.get("CONSUMER_SECRET_2"),
    }
)

p1 = Process(target=stream_event.listen)
p1.start()

# waiting server
sleep(5)
    
assert post(public_url+"/listener/test").status_code == 200


print("registering webhook...")
cred1 = {
    'CONSUMER_KEY': os.environ.get("CONSUMER_KEY"),
    'CONSUMER_SECRET': os.environ.get("CONSUMER_SECRET"),
    'ACCESS_KEY': os.environ.get("ACCESS_KEY"),
    'ACCESS_SECRET': os.environ.get("ACCESS_SECRET"),
    'ENV_NAME': os.environ.get("ENV_NAME"),
}
print(cred1)
webhook_1 = wman.register_webhook(
    public_url+"/listener",
    "Darksiede1",
    type(
        "object",
        (object,),
        cred1,
    ) 
)

assert webhook_1.status_code == 204


print("registering webhook_2...")
cred2 = {
    'CONSUMER_KEY': os.environ.get("CONSUMER_KEY_2"),
    'CONSUMER_SECRET': os.environ.get("CONSUMER_SECRET_2"),
    'ACCESS_KEY': os.environ.get("ACCESS_KEY_2"),
    'ACCESS_SECRET': os.environ.get("ACCESS_SECRET_2"),
    'ENV_NAME': os.environ.get("ENV_NAME_2"),
}
print(cred2)
webhook_2 = wman.register_webhook(
    public_url+"/listener",
    "autobase_reborn",
    type(
        "object",
        (object,),
        cred2,
    ) 
)

assert webhook_2.status_code == 204

# stop Process
p1.terminate()