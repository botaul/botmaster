from twitter import Twitter
from media import Media
from time import sleep
from threading import Thread
from github import Github
import datetime
import constants
import requests
from requests_oauthlib import OAuth1
from os.path import exists
import os

tw = Twitter()
media = Media()
github = Github(constants.Github_username, constants.Github_password)


def start():
    print("Starting program...")
    dms = list()
    api = tw.api
    me = api.me()
    tw.bot_id = me.id
    open('follower_data.txt', 'w').truncate()
    first = open('follower_data.txt').read()
    # sent = api.send_direct_message(recipient_id=me.id, text="Twitter autobase is starting...!").id
    # tw.delete_dm(sent)

    while True:
        print("Updating followers...")
        follower = api.followers_ids(user_id=me.id)
        if len(follower) != 0:
            tw.follower = follower

            if len(first) <= 3:
                str_follower = [str(i) for i in follower]
                data = " ".join(str_follower)
                open("follower_data.txt", "w").write(data)
                first = "checked"
                del str_follower

            data = open('follower_data.txt').read()
            data = data.split()
            data1 = str()
            data2 = data.copy()

            for i in follower:
                if str(i) not in data:
                    data1 += " " + str(i)
                    notif = "[BOT]\nYEAY! Sekarang kamu bisa mengirim menfess, jangan lupa baca peraturan base yaa!"
                    sent = api.send_direct_message(
                        recipient_id=i, text=notif).id
                    tw.delete_dm(sent)

            for i in data2:
                if int(i) not in follower:
                    data.remove(i)

            if data != data2:
                data = " ".join(data)
                data = data + data1
                new = open("follower_data.txt", "w")
                new.write(data)
                new.close()
            elif data == data2 and len(data1) != 0:
                new = open("follower_data.txt", "a")
                new.write(data1)
                new.close()

            del data
            del data1
            del data2

        else:
            print("error when get follower from API")
            pass

        if len(dms) != 0:
            for i in range(len(dms)):
                try:
                    message = dms[i]['message']
                    sender_id = dms[i]['sender_id']
                    id = dms[i]['id']
                    screen_name = tw.get_user_screen_name(sender_id)
                    globals()['DATABASE'] = DATABASE + "\n" + message + \
                        " - @" + screen_name + " - " + sender_id
                    print("Heroku Database saved")

                    notif = f"Yeay, Menfess kamu telah terkirim! https://twitter.com/{me.screen_name}/status/"
                    if constants.First_Keyword in message:
                        if dms[i]['media'] is None:
                            print("DM will be posted")
                            if 'urls' not in dms[i]:
                                postid = tw.post_tweet(message)
                            else:
                                message = message.split()
                                message = " ".join(message[:-1])
                                if constants.Sub1_keyword not in message:
                                    postid = tw.post_multiple_media(
                                        message, dms[i]['urls'])
                                else:
                                    postid = tw.post_tweet(message, attachment_url=dms[i]['urls'])

                            if postid == "not_available":
                                message = message.split()
                                message = " ".join(message[:-1])
                                postid = tw.post_tweet(message, attachment_url=dms[i]['urls'])
                                text = notif + \
                                    "\nfyi:hanya dapat mengirim 4 foto atau 1 video" + \
                                    str(postid)
                                sent = api.send_direct_message(
                                    recipient_id=sender_id, text=text).id
                            elif postid != None:
                                text = notif + str(postid)
                                sent = api.send_direct_message(
                                    recipient_id=sender_id, text=text).id
                            else:
                                sent = api.send_direct_message(
                                    recipient_id=sender_id, text="[BOT]\nMaaf ada kesalahan pada sistem :(\ntolong screenshot & laporkan kepada admin").id
                            tw.delete_dm(id)
                            tw.delete_dm(sent)
                        else:
                            print("DM will be posted with media.")
                            postid = tw.post_tweet_with_media(
                                message, dms[i]['media'], dms[i]['type'])
                            if postid != None:
                                text = notif + str(postid)
                                sent = api.send_direct_message(
                                    recipient_id=sender_id, text=text).id
                            else:
                                sent = api.send_direct_message(
                                    recipient_id=sender_id, text="[BOT]\nMaaf ada kesalahan pada sistem :(\ntolong screenshot & laporkan kepada admin").id
                            tw.delete_dm(id)
                            tw.delete_dm(sent)

                    elif constants.Second_Keyword in message and "https://" not in message and "http://" not in message and "twitter.com" not in message and len(message) <= 500:
                        message = message.replace(
                            constants.Second_Keyword, "")
                        if constants.Sub2_Keyword in message:
                            message = message.replace(
                                constants.Sub2_Keyword, "")
                            media.download_image()
                            media.process_image(message, screen_name)
                            postid = tw.post_tweet_quote(screen_name)
                            if postid != None:
                                text = notif + str(postid)
                                sent = api.send_direct_message(
                                    recipient_id=sender_id, text=text).id
                            else:
                                sent = api.send_direct_message(
                                    recipient_id=sender_id, text="[BOT]\nMaaf ada kesalahan pada sistem :(\ntolong screenshot & laporkan kepada admin").id
                            tw.delete_dm(id)
                            tw.delete_dm(sent)
                        else:
                            media.download_image()
                            media.process_image(message, None)
                            postid = tw.post_tweet_quote(name=None)
                            if postid != None:
                                text = notif + str(postid)
                                sent = api.send_direct_message(
                                    recipient_id=sender_id, text=text).id
                            else:
                                sent = api.send_direct_message(
                                    recipient_id=sender_id, text="[BOT]\nMaaf ada kesalahan pada sistem :(\ntolong screenshot & laporkan kepada admin").id
                            tw.delete_dm(id)
                            tw.delete_dm(sent)

                    elif constants.Third_keyword in message:
                        message = message.replace(constants.Third_keyword, "")
                        if dms[i]['media'] is None:
                            sent1 = tw.ASK(message, screen_name)
                        elif dms[i]['type'] != 'photo':
                            print("asking with video")
                            message = message.split()
                            message = " ".join(message[:-1])
                            tw.download_media(dms[i]['media'], "video.mp4")
                            media_id = tw.media_upload_chunk(
                                "video.mp4", False)
                            os.remove("video.mp4")
                            sent1 = api.send_direct_message(sender_id, str(message + " @" + screen_name),
                                                            None, 'media', media_id).id
                        else:
                            print("asking with photo")
                            message = message.split()
                            message = " ".join(message[:-1])
                            tw.download_media(dms[i]['media'], "photo.jpg")
                            media_id = api.media_upload("photo.jpg")
                            os.remove("photo.jpg")
                            sent1 = api.send_direct_message(sender_id, str(message + " @" + screen_name),
                                                            None, 'media', media_id.media_id_string).id

                        sent = api.send_direct_message(
                            recipient_id=sender_id, text="[BOT]\nPesan kamu telah dikirimkan ke admin").id
                        tw.delete_dm(sent1)
                        tw.delete_dm(sent)
                        tw.delete_dm(id)

                    else:
                        sent = api.send_direct_message(
                            sender_id, "ketentuan keyword menfess kamu tidak sesuai!").id
                        tw.delete_dm(sent)
                        tw.delete_dm(id)

                except Exception as ex:
                    print(ex)
                    sleep(30)
                    pass

            dms = list()
            globals()['ACTION'] = DATABASE
            print("waiting Github threading..(if > 20)")
            sleep(30)
            globals()['ACTION'] = ""

        else:
            print("Direct message is empty..")
            dms = tw.read_dm()
            if len(dms) == 0:
                sleep(30)


def push():
    while True:
        try:
            if len(ACTION) > 20:
                globals()['ACTION'] = ""
                print("Github threading active...")
                repo = github.get_repo(constants.Github_repo)
                name = f"DATABASE {str(datetime.datetime.now() + datetime.timedelta(hours = constants.Timezone))}.txt"
                repo.create_file(name, "commit", DATABASE)
                globals()['DATABASE'] = "_MENFESS DATABASE_"
                print("Github Database updated")
                sleep(3600)

            else:
                sleep(10)

        except Exception as ex:
            print(ex)
            print("Github threading failed..")
            sleep(720)
            pass


if __name__ == "__main__":
    global DATABASE
    DATABASE = "_MENFESS DATABASE_"
    global ACTION
    ACTION = ""
    Thread(target=start).start()
    Thread(target=push).start()
