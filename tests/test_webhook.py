import os
from dotenv import load_dotenv
from twitter_autobase import webhook_manager as wman
from multiprocessing import Process
from requests import post
from time import sleep

load_dotenv()

def test_create_ngrok_process():
    global public_url
    public_url = wman.connect_ngrok(os.environ["NGROK_AUTH_TOKEN"])
    assert "https" in public_url


def test_server():
    stored_data = list()
    
    stream_event = wman.StreamEvent(stored_data)
    stream_event.set_callback(public_url+"/listener")
    stream_event.update_credential_id(
        {
            'Darksiede1': os.environ["CONSUMER_SECRET"],
        }
    )

    global p1
    p1 = Process(target=stream_event.listen)
    p1.start()

    # waiting server
    sleep(3)
    
    assert post(public_url+"/listener/test").status_code == 200

    # stop Process
    p1.terminate()
