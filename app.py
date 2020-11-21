# Original code by Prieyudha Akadita S.
#     Source: https://https://github.com/ydhnwb/autodm_base

# Re-code by Fakhri Catur Rofi under MIT License
#     Source: https://github.com/fakhrirofi/twitter_autobase

import administrator_data
import temp
from twitter import Twitter
from time import sleep
from threading import Thread
from datetime import datetime, timezone, timedelta
from os.path import exists
from os import remove
from html import unescape
from random import randrange


def Start():
    print("Starting program...")
    dms = list()
    tw = Twitter()
    api = tw.api
    temp.api = api
    me = api.me()
    tw.bot_id = me.id
    open('follower_data.txt', 'w').write("")
    first = 1
    # sent = api.send_direct_message(recipient_id=administrator_data.Admin_id, text="Twitter autobase is starting...!").id
    # tw.delete_dm(sent)

    while True:
        print("Updating followers...")
        # Auto accept message requests
        # Comment these if you want close your DM
        follower = api.followers_ids(user_id=me.id)
        if len(follower) != 0:
            try:
                if first == 1:
                    first = 0
                    data = [str(i) for i in follower]
                    data = " ".join(data)
                    open("follower_data.txt", "w").write(data)

                data = open('follower_data.txt').read()

                for i in follower:
                    if str(i) not in data:
                        data += " " + str(i)
                        notif = "YEAY! Sekarang kamu bisa mengirim menfess, jangan lupa baca peraturan base yaa!"
                        # I don't know, sometimes error happen here, so, I update tw.follower after this loop
                        sent = api.send_direct_message(recipient_id=i, text=notif).id
                        tw.delete_dm(sent)
                        
                tw.follower = follower
                open('follower_data.txt', 'w').write(data)
                del data
                
            except Exception as ex:
                print("error when send DM to follower, error when get follower from API")
                pass

        else:
            print("error when get follower from API")

        if len(dms) != 0:
            for i in range(len(dms)):
                try:
                    message = dms[i]['message']
                    sender_id = dms[i]['sender_id']
                    media_url = dms[i]['media_url']
                    attachment_urls = dms[i]['attachment_urls']

                    if administrator_data.Database == True:
                        screen_name = tw.get_user_screen_name(sender_id)
                        if exists(filename_github):
                            open(filename_github, 'a').write(
                                f'''\n"""{unescape(message)}""" {screen_name} {sender_id}\n''')
                        else:
                            open(filename_github, 'w').write(
                                "MESSAGE USERNAME SENDER_ID\n" +
                                f'''\n"""{unescape(message)}""" {screen_name} {sender_id}\n''')
                        print("Heroku Database saved")

                    notif = f"Yeay, Menfess kamu telah terkirim! https://twitter.com/{me.screen_name}/status/"
                    
                    if any(j.lower() in message.lower() for j in administrator_data.Trigger_word):
                        # Keyword Deleter
                        message = message.split()
                        list_keyword = [j.lower() for j in administrator_data.Trigger_word] + \
                                       [j.upper() for j in administrator_data.Trigger_word] + \
                                       [j.capitalize() for j in administrator_data.Trigger_word]

                        [message.remove(j) for j in list_keyword if j in message]
                        message = " ".join(message)

                        # post tweet
                        if attachment_urls != (None, None):
                            message = message.split()
                            message.remove(attachment_urls[0])
                            message = " ".join(message)
                        
                        print("DM will be posted")
                        postid = tw.post_tweet(message, media_url=media_url, attachment_url=attachment_urls[1])

                        # notify sender
                        if postid != None:
                            text = notif + str(postid)
                        else:
                            text = "Maaf ada kesalahan pada sistem :(\ntolong screenshot & laporkan kepada admin"
                        
                        sent = api.send_direct_message(recipient_id=sender_id, text=text).id
                        tw.delete_dm(sent)

                    else:
                        sent = api.send_direct_message(
                            sender_id, "ketentuan keyword menfess kamu tidak sesuai!").id
                        tw.delete_dm(sent)

                except Exception as ex:
                    print(ex)
                    sleep(30)
                    pass

            dms = list()

        else:
            print("Direct message is empty...")
            dms = tw.read_dm()
            if len(dms) == 0:
                sleep(25+randrange(0, 5))


def Check_file_github(new=True):
    '''
    True when bot was just started, download & save file from github
    False when bot is running. if file exists, doesn't save the file from github
    '''
    print("checking github file...")
    try:
        datee = datetime.now(timezone.utc) + \
            timedelta(hours=administrator_data.Timezone)
        globals()['filename_github'] = "Database {}-{}-{}.txt".format(
            datee.day, datee.month, datee.year)
        temp.filename_github = filename_github
        contents = repo.get_contents("")

        if any(filename_github == content.name for content in contents):
            print(f"filename_github detected, set: {str(new)}")
            if new == False:
                return
            for content in contents:
                if filename_github == content.name:
                    contents = content.decoded_content.decode()
                    if contents[-1] != "\n":
                        contents += "\n"
                    break
        else:
            print("filename_github not detected")
            repo.create_file(filename_github, "first commit",
                             "MESSAGE USERNAME SENDER_ID")
            contents = "MESSAGE USERNAME SENDER_ID\n"

        if exists(filename_github) == False:
            open(filename_github, 'w').write(contents)
        else:
            pass

        if exists("Database {}-{}-{}.txt".format(
                datee.day - 1, datee.month, datee.year)):
            remove("Database {}-{}-{}.txt".format(
                datee.day - 1, datee.month, datee.year))
            print("Heroku yesterday's Database has been deleted")
        else:
            print("Heroku yesterday's Database doesn't exist")

    except Exception as ex:
        pass
        print(ex)


def Database():
    while True:
        try:
            # update every midnight, u can update directly from DM with 'db_update'
            # check on administrator_data.py
            datee = datetime.now(timezone.utc) + timedelta(hours=administrator_data.Timezone)
            if filename_github != f"Database {datee.day}-{datee.month}-{datee.year}.txt":
                print("Github threading active...")
                contents = repo.get_contents(filename_github)
                repo.update_file(contents.path, "updating Database", open(
                    filename_github).read(), contents.sha)
                Check_file_github(new=False)
                print("Github Database updated")
                sleep(60)

            else:
                sleep(60)

        except Exception as ex:
            print(ex)
            print("Github threading failed..")
            sleep(720)
            pass


if __name__ == "__main__":
    if administrator_data.Database == True:
        # True = on, False = off
        from github import Github
        github = Github(administrator_data.Github_token)

        datee = datetime.now(timezone.utc) + timedelta(hours=administrator_data.Timezone)
        global filename_github, repo
        filename_github = "Database {}-{}-{}.txt".format(
            datee.day, datee.month, datee.year)
        repo = github.get_repo(administrator_data.Github_repo)

        temp.repo = repo
        temp.filename_github = filename_github

        Check_file_github(new=True)
        Thread(target=Database).start()

    Start()

