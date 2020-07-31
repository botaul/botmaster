from twitter import Twitter
from twitter2 import Twitter2
from media import Media
import time
import threading
from github import Github
import datetime
import constants

tw = Twitter()
tw2 = Twitter2()
media = Media()
github = Github(constants.Github_username, constants.Github_password)

def start():
    print("Starting program...")
    dms = list()
    while True:
        if len(dms) != 0 :
            for i in range(len(dms)):
                message = dms[i]['message']
                sender_id = dms[i]['sender_id']
                id = dms[i]['id']
                screen_name = tw2.get_user_screen_name(sender_id)
                globals()['DATABASE'] = DATABASE + "\n" + message + " - @" + screen_name + " - " + sender_id
                print("Heroku Database saved")
                
                if constants.First_Keyword in message:
                    if dms[i]['media'] is None:
                        print("DM will be posted")
                        tw.post_tweet(message)
                        tw.delete_dm(id)
                    else:
                        print("DM will be posted with media.")
                        tw.post_tweet_with_media(message, dms[i]['media'], dms[i]['type'])
                        tw.delete_dm(id)

                elif constants.Second_Keyword in message and "https://" not in message and "http://" not in message and "twitter.com" not in message and len(message) <= 500:
                    if constants.Sub2_Keyword in message:
                        message = message.replace(constants.Second_Keyword, "")
                        message = message.replace(constants.Sub2_Keyword, "")
                        media.download_image()
                        media.process_image(message, screen_name)
                        tw2.post_tweet(name=screen_name)
                        tw2.delete_dm(id)
                    else:
                        message = message.replace(constants.Second_Keyword, "")
                        media.download_image()
                        media.process_image(message, None)
                        tw2.post_tweet(name=None)
                        tw2.delete_dm(id)

                elif constants.Third_keyword in message:
                    message = message.replace(constants.Third_keyword, "")
                    tw2.ASK(message, screen_name)
                    tw2.delete_dm(id)

            dms = list()
            globals()['ACTION'] = DATABASE
            print("waiting Github threading..(if > 20)")
            time.sleep(30)
            globals()['ACTION'] = ""

        else:
            print("Direct message is empty..")
            dms = tw.read_dm()
            if len(dms) == 0:
                time.sleep(60)
def push():
    try:
        if len(ACTION) > 20:
            globals()['ACTION'] = ""
            print("Github threading active...")
            repo = github.get_repo(constants.Github_repo)
            name = f"DATABASE {str(datetime.datetime.now() + datetime.timedelta(hours = 7))}.txt"
            repo.create_file(name, "commit", DATABASE)
            globals()['DATABASE'] = "_MENFESS DATABASE_"
            print("Github Database updated")
            time.sleep(720)
            push()
        else:
            time.sleep(5)
            push()
    except Exception as ex:
        print(ex)
        print("Github threading failed..")
        time.sleep(720)
        push()
        pass

if __name__ == "__main__":
    global DATABASE
    DATABASE = "_MENFESS DATABASE_"
    global ACTION
    ACTION = ""
    threading.Thread(target=start).start()
    threading.Thread(target=push).start()
