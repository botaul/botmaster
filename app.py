from twitter import Twitter
from media import Media
import time
import threading
from github import Github
import datetime
import constants
import requests
from requests_oauthlib import OAuth1
from os.path import exists

tw = Twitter()
media = Media()
github = Github(constants.Github_username, constants.Github_password)


def start():
    print("Starting program...")
    dms = list()
    api = tw.api
    me = api.me()
    tw.bot_id = me.id
    first = open('follower_data.txt').read()  # outside loop

    while True:

        print("Updating followers...")
        follower1 = api.followers_ids(user_id=me.id)
        follower = list()
        # follower1 (list of int)
        # follower = follower1 convert to str (list of str)
        for i in range(len(follower1)):
            follower.append(str((follower1)[i]))

        tw.follower = follower

        if len(first) <= 3:
            data1 = "\n".join(follower) + "\n"
            new = open("follower_data.txt", "w")
            new.write(data1)
            new.close()
            first = "checked"

        data = open('follower_data.txt').read()  # inside loop
        data1 = ""  # inside loop

        for i in range(len(follower)):
            if follower[i] not in data:
                data1 = data1 + follower[i] + "\n"
                notif = "[BOT]\nYEAY! Sekarang kamu bisa mengirim menfess, jangan lupa baca peraturan base yaa!"
                api.send_direct_message(recipient_id=follower[i], text=notif)

        data2 = data[:len(data)-1].split("\n")
        data3 = data[:len(data)-1].split("\n")
        i = 0
        max = len(data2)-1
        while i <= max:
            if data2[i] not in follower:
                data2.remove(data2[i])
                max -= 1
                i -= 1
            i += 1
        # data =  follower sebelumnya(text)
        # data1 = follower baru (text)
        # data2 = follower sebelumnya yg berubah (list)
        # data3 = follower sebelumnya yg tetap (list)
        if data2 != data3:
            data = "\n".join(data2) + "\n"
            data = data + data1
            new = open("follower_data.txt", "w")
            new.write(data)
            new.close()
        elif data2 == data3:
            new = open("follower_data.txt", "a")
            new.write(data1)
            new.close()

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
                            postid = tw.post_tweet(message)
                            if postid != None:
                                text = notif + str(postid)
                                sent = api.send_direct_message(
                                    recipient_id=sender_id, text=text)
                            else:
                                sent = api.send_direct_message(
                                    recipient_id=sender_id, text="[BOT]\nMaaf ada kesalahan pada sistem :(\ntolong screenshot & laporkan kepada admin")
                            tw.delete_dm(id)
                            tw.delete_dm(sent.id)
                        else:
                            print("DM will be posted with media.")
                            postid = tw.post_tweet_with_media(
                                message, dms[i]['media'], dms[i]['type'])
                            if postid != None:
                                text = notif + str(postid)
                                sent = api.send_direct_message(
                                    recipient_id=sender_id, text=text)
                            else:
                                sent = api.send_direct_message(
                                    recipient_id=sender_id, text="[BOT]\nMaaf ada kesalahan pada sistem :(\ntolong screenshot & laporkan kepada admin")
                            tw.delete_dm(id)
                            tw.delete_dm(sent.id)

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
                                    recipient_id=sender_id, text=text)
                            else:
                                sent = api.send_direct_message(
                                    recipient_id=sender_id, text="[BOT]\nMaaf ada kesalahan pada sistem :(\ntolong screenshot & laporkan kepada admin")
                            tw.delete_dm(id)
                            tw.delete_dm(sent.id)
                        else:
                            media.download_image()
                            media.process_image(message, None)
                            postid = tw.post_tweet_quote(name=None)
                            if postid != None:
                                text = notif + str(postid)
                                sent = api.send_direct_message(
                                    recipient_id=sender_id, text=text)
                            else:
                                sent = api.send_direct_message(
                                    recipient_id=sender_id, text="[BOT]\nMaaf ada kesalahan pada sistem :(\ntolong screenshot & laporkan kepada admin")
                            tw.delete_dm(id)
                            tw.delete_dm(sent.id)

                    elif constants.Third_keyword in message:
                        message = message.replace(constants.Third_keyword, "")
                        if dms[i]['media'] is None:
                            sent1 = tw.ASK(message, screen_name)
                        elif dms[i]['type'] != 'photo':
                            sent1 = tw.ASK(
                                str(message + " video type"), screen_name)
                        else:
                            print("asking with media")
                            message = message.split()
                            message = " ".join(message[:len(message)-1])
                            tw.download_media(dms[i]['media'], "photo.jpg")
                            media1 = api.media_upload("photo.jpg")
                            sent1 = api.send_direct_message(sender_id, str(message + " @" + screen_name),
                                                            None, 'media', media1.media_id_string)

                        sent = api.send_direct_message(
                            recipient_id=sender_id, text="[BOT]\nPesan kamu telah dikirimkan ke admin")
                        tw.delete_dm(sent1.id)
                        tw.delete_dm(sent.id)
                        tw.delete_dm(id)

                    else:
                        sent = api.send_direct_message(
                            sender_id, "ketentuan keyword menfess kamu tidak sesuai!")
                        tw.delete_dm(sent.id)
                        tw.delete_dm(id)

                except Exception as ex:
                    print(ex)
                    time.sleep(30)
                    pass

            dms = list()
            globals()['ACTION'] = DATABASE
            print("waiting Github threading..(if > 20)")
            time.sleep(30)
            globals()['ACTION'] = ""

        else:
            print("Direct message is empty..")
            dms = tw.read_dm()
            if len(dms) == 0:
                time.sleep(30)


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
                time.sleep(3600)
        
            else:
                time.sleep(10)
            
            
        except Exception as ex:
            print(ex)
            print("Github threading failed..")
            time.sleep(720)
            pass


if __name__ == "__main__":
    global DATABASE
    DATABASE = "_MENFESS DATABASE_"
    global ACTION
    ACTION = ""
    threading.Thread(target=start).start()
    threading.Thread(target=push).start()
