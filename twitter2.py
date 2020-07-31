import tweepy
import constants
import time
import os

class Twitter2 :
    def __init__(self):
        print("Init twitter api")

    @staticmethod
    def init_tweepy():
        api = tweepy.OAuthHandler(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)
        api.set_access_token(constants.ACCESS_KEY, constants.ACCESS_SECRET)
        return tweepy.API(api)

    def delete_dm(self, id):
        print("Delete dm with id "+ str(id))
        try:
            api = self.init_tweepy()
            api.destroy_direct_message(id)
            time.sleep(40)
        except Exception as ex:
            print(ex)
            time.sleep(60)
            pass

    def ASK(self, message, screen_name):
        try:
            print("ASKING")
            message1 = message + " @" + screen_name
            api = self.init_tweepy()
            api.send_direct_message(recipient_id = constants.Admin_id, text = message1)
        except Exception as ex:
            print(ex)
            time.sleep(60)
            pass

    def post_tweet(self, name):
        print("Uploading..")
        try:
            if name is None:
                tweet = constants.Second_Keyword
            elif name != None:
                tweet = f"{constants.Second_Keyword} by @{name}"
            api = self.init_tweepy()
            api.update_with_media(filename="ready.png", status=tweet)
            os.remove('ready.png')
        except Exception as ex:
            print(ex)
            time.sleep(60)
            pass

    def get_user_screen_name(self, id):
        try:
            print("Getting username")
            api = self.init_tweepy()
            user = api.get_user(id)
            return user.screen_name
        except Exception as ex:
            print(ex)
            user = "Exception"
            time.sleep(60)
            return user
            pass
