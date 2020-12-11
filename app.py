# Original code by Prieyudha Akadita S.
#     Source: https://https://github.com/ydhnwb/autodm_base

# Re-code by Fakhri Catur Rofi under MIT License
#     Source: https://github.com/fakhrirofi/twitter_autobase

import administrator_data
from twitter import Twitter
from time import sleep


def Start():
    print("Starting program...")
    dms = list()
    tw = Twitter()
    api = tw.api
    me = tw.me
    first = 1 # indicator for accept message
    first1 = 1 # indicator for followed
    # for i in administartor_data.Admin_id:
    #     sent = tw.send_dm(recipient_id=i, text="Twitter autobase is starting...!")

    while True:
        # AUTO ACCEPT MESSAGE REQUESTS
        print("Accepting message requests...")
        try:
            follower = api.followers_ids(user_id=me.id, count=50)
            if len(follower) != 0:
                if first == 1:
                    first = 0
                    tw.follower = follower.copy()

                for i in follower:
                    if i not in tw.follower:
                        notif = administrator_data.Notify_acceptMessage
                        # I don't know, sometimes error happen here, so, I update tw.follower after send_dm
                        try:
                            tw.send_dm(recipient_id=i, text=notif)
                            tw.follower.insert(0, i)
                            if len(tw.follower) > 55: tw.follower.pop()
                        except Exception as ex:
                            print(ex)
                            pass
                            
        except Exception as ex:
            print(ex)
            pass

        # GETTING LIST OF FOLLOWED
        if administrator_data.Only_followed is True:
            try:
                if first1 == 1:
                    first1 = 0
                    followed = tw.get_all_followed(me.id, first_delay=False)
                    tw.followed = followed.copy()
                else:
                    print("Updating friends ids...")
                    followed = api.friends_ids(user_id=me.id)
                
                for i in followed:
                    if i not in tw.followed:
                        notif = administrator_data.Notify_followed
                        tw.send_dm(recipient_id=i, text=notif)
                        tw.followed.append(i)

            except Exception as ex:
                print(ex)
                pass


        if len(dms) != 0:

            if administrator_data.Notify_queue is True:
                # Notify the menfess queue to sender
                tw.notify_queue(dms)

            for i in range(len(dms)):
                try:
                    message = dms[i]['message']
                    sender_id = dms[i]['sender_id']
                    media_url = dms[i]['media_url']
                    attachment_urls = dms[i]['attachment_urls']['tweet']
                    list_attchmentUrlsMedia = dms[i]['attachment_urls']['media']

                    if administrator_data.Database is True:
                        screen_name = tw.get_user_screen_name(sender_id)
                        if exists(filename_github):
                            with open(filename_github, 'a') as f:
                                f.write(f'''\n"""{unescape(message)}""" {screen_name} {sender_id}\n''')
                                f.close()
                        else:
                            with open(filename_github, 'w') as f:
                                f.write("MESSAGE USERNAME SENDER_ID\n" +
                                    f'''\n"""{unescape(message)}""" {screen_name} {sender_id}\n''')
                                f.close()
                        print("Heroku Database saved")
                    
                    if any(j.lower() in message.lower() for j in administrator_data.Trigger_word):
                        # Keyword Deleter
                        if administrator_data.Keyword_deleter is True:
                            message = message.split()
                            list_keyword = [j.lower() for j in administrator_data.Trigger_word] + \
                                        [j.upper() for j in administrator_data.Trigger_word] + \
                                        [j.capitalize() for j in administrator_data.Trigger_word]

                            [message.remove(j) for j in list_keyword if j in message]
                            message = " ".join(message)

                        # POST TWEET
                        if attachment_urls != (None, None):
                            message = message.split()
                            message.remove(attachment_urls[0])
                            message = " ".join(message)
                        
                        # Private_mediaTweet
                        media_idsAndTypes = list() # e.g [(media_id, media_type), (media_id, media_type), ]
                        # Pay attention to append and extend!
                        if administrator_data.Private_mediaTweet is True:
                            for media_tweet_url in list_attchmentUrlsMedia:
                                list_mediaIdsAndTypes = tw.upload_media_tweet(media_tweet_url[1])
                                if len(list_mediaIdsAndTypes) != 0:
                                    media_idsAndTypes.extend(list_mediaIdsAndTypes)
                                    message = message.split()
                                    message.remove(media_tweet_url[0])
                                    message = " ".join(message)
                        
                        # Menfess contains sensitive contents
                        possibly_sensitive = False
                        if administrator_data.Sensitive_word.lower() in message.lower():
                            possibly_sensitive = True

                        print("Posting menfess...")
                        postid = tw.post_tweet(message, sender_id, media_url=media_url, attachment_url=attachment_urls[1],
                                media_idsAndTypes=media_idsAndTypes, possibly_sensitive=possibly_sensitive)
                        
                        if postid == None:
                            # Error happen on system
                            text = administrator_data.Notify_sentFail1
                            tw.send_dm(recipient_id=sender_id, text=text)

                    else:
                        # Notify sender, message doesn't meet the algorithm's requirement
                        tw.send_dm(sender_id, administrator_data.Notify_sentFail2)

                except Exception as ex:
                    print(ex)
                    sleep(30)
                    pass

            dms = list()

        else:
            dms = tw.read_dm()
            if len(dms) == 0:
                print("Direct message is empty, sleeping for 30s...")
                sleep(30)


def Check_file_github(new=True):
    '''
    True when bot was just started, download & save file from github
    False when bot is running. If file exists, doesn't save the file from github.
    New parameter used if you update database not every midnight on Database method
    '''
    print("checking github file...")
    try:
        datee = datetime.now(timezone.utc) + \
            timedelta(hours=administrator_data.Timezone)
        globals()['filename_github'] = "Database {}-{}-{}.txt".format(
            datee.year, datee.month, datee.day)
        tmp.filename_github = filename_github
        contents = repo.get_contents("")

        if any(filename_github == content.name for content in contents):
            # If filename exists in github. But, when midnight,
            # filename automatically changed.
            print(f"filename_github detected, new: {str(new)}")
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
            contents = "MESSAGE USERNAME SENDER_ID\n"
            repo.create_file(filename_github, "first commit",
                             contents)

        if exists(filename_github) == False:
            with open(filename_github, 'w') as f:
                f.write(contents)
                f.close()
        else:
            pass

        if exists("Database {}-{}-{}.txt".format(
                datee.year, datee.month, datee.day - 1)):
            remove("Database {}-{}-{}.txt".format(
                datee.year, datee.month, datee.day - 1))
            print("Heroku yesterday's Database has been deleted")
        else:
            print("Heroku yesterday's Database doesn't exist")

    except Exception as ex:
        pass
        print(ex)


def Database():
    while True:
        try:
            # update every midnight, you can update directly from DM with 'db_update'
            # check on administrator_data.py
            datee = datetime.now(timezone.utc) + timedelta(hours=administrator_data.Timezone)
            if filename_github != f"Database {datee.year}-{datee.month}-{datee.day}.txt":
                print("Github threading active...")
                contents = repo.get_contents(filename_github)
                with open(filename_github) as f:
                    data = f.read()
                    f.close()
                repo.update_file(contents.path, "updating Database", data, contents.sha)
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
    if administrator_data.Database is True:
        # True = on, False = off
        from threading import Thread
        from datetime import datetime, timezone, timedelta
        from os.path import exists
        from os import remove
        from html import unescape
        from github import Github
        import tmp

        github = Github(administrator_data.Github_token)

        datee = datetime.now(timezone.utc) + timedelta(hours=administrator_data.Timezone)
        global filename_github, repo
        filename_github = "Database {}-{}-{}.txt".format(
            datee.year, datee.month, datee.day)
        repo = github.get_repo(administrator_data.Github_repo)

        tmp.repo = repo
        tmp.filename_github = filename_github

        Check_file_github(new=True)
        Thread(target=Database).start()

    Start()

