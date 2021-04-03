import os
from twitter_autobase import webhook_manager as wman
from multiprocessing import Process
from requests import post
from time import sleep


def test_create_ngrok_process():
    global public_url
    public_url = wman.connect_ngrok(os.environ.get("NGROK_AUTH_TOKEN"))
    assert "https" in public_url


def test_server():
    stored_data = list()
    
    stream_event = wman.StreamEvent(stored_data)
    stream_event.set_callback(public_url+"/listener")
    stream_event.update_credential_id(
        {
            'Darksiede1': os.environ.get("CONSUMER_SECRET"),
            'autobase_reborn': os.environ.get("CONSUMER_SECRET_2"),
        }
    )

    global p1
    p1 = Process(target=stream_event.listen)
    p1.start()

    # waiting server
    sleep(5)
    
    assert post(public_url+"/listener/test").status_code == 200


def test_register_webhook():
    webhook_1 = wman.register_webhook(
        public_url+"/listener",
        "Darksiede1",
        type(
            "object",
            (object,),
            {
                'CONSUMER_KEY': os.environ.get("CONSUMER_KEY"),
                'CONSUMER_SECRET': os.environ.get("CONSUMER_SECRET"),
                'ACCESS_KEY': os.environ.get("ACCESS_KEY"),
                'ACCESS_SECRET': os.environ.get("ACCESS_SECRET"),
                'ENV_NAME': os.environ.get("ENV_NAME"),
            }
        ) 
    )

    assert webhook_1.status_code == 204


def test_multiple_register_webhook():
    webhook_2 = wman.register_webhook(
        public_url+"/listener",
        "autobase_reborn",
        type(
            "object",
            (object,),
            {
                'CONSUMER_KEY': os.environ.get("CONSUMER_KEY_2"),
                'CONSUMER_SECRET': os.environ.get("CONSUMER_SECRET_2"),
                'ACCESS_KEY': os.environ.get("ACCESS_KEY_2"),
                'ACCESS_SECRET': os.environ.get("ACCESS_SECRET_2"),
                'ENV_NAME': os.environ.get("ENV_NAME_2"),
            }
        ) 
    )

    assert webhook_2.status_code == 204

    # stop Process
    p1.terminate()