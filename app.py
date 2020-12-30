# Original code by Prieyudha Akadita S.
#     Source: https://https://github.com/ydhnwb/autodm_base

# Re-code by Fakhri Catur Rofi under MIT License
#     Source: https://github.com/fakhrirofi/twitter_autobase

from twitter import Twitter
from time import sleep
from threading import Thread
from datetime import datetime, timezone, timedelta
from os.path import exists
from os import remove
from html import unescape
from github import Github
from json import dump, load


class Autobase:
    '''
    :param credential: class that contains object class like administrator_data.py -> object 
    '''
    def __init__(self, credential):
        '''
        Attributes:
            - credential
            - tw
            - AdminCmd
            - bot_username
            - database_indicator

        :param credential: class that contains object class like administrator_data.py -> object
        '''
        self.credential = credential
        self.tw = Twitter(credential)
        self.AdminCmd = self.tw.AdminCmd
        self.bot_username = self.tw.me.screen_name
        self.database_indicator = False


    def __update_follow(self, indicator):
        api = self.tw.api
        me = self.tw.me
        first = 1 # indicator for accept message
        first1 = 1 # indicator for followed
        while True:
            # AUTO ACCEPT MESSAGE REQUESTS
            print("Accepting message requests...")
            try:
                follower = api.followers_ids(user_id=me.id, count=50)
                if len(follower) != 0:
                    if first == 1:
                        first = 0
                        self.tw.follower = follower.copy()

                    for i in follower:
                        if i not in self.tw.follower:
                            notif = self.credential.Notify_acceptMessage
                            # I don't know, sometimes error happen here, so, I update self.tw.follower after send_dm
                            try:
                                self.tw.send_dm(recipient_id=i, text=notif)
                                self.tw.follower.insert(0, i)
                                if len(self.tw.follower) > 55: self.tw.follower.pop()
                            except Exception as ex:
                                print(ex)
                                pass
                                
            except Exception as ex:
                print(ex)
                pass

            # GETTING LIST OF FOLLOWED
            if self.credential.Only_followed is True:
                try:
                    if first1 == 1:
                        first1 = 0
                        followed = self.tw.get_all_followed(me.id, first_delay=False)
                        self.tw.followed = followed.copy()
                    else:
                        print("Updating friends ids...")
                        followed = api.friends_ids(user_id=me.id)
                    
                    for i in followed:
                        if i not in self.tw.followed:
                            notif = self.credential.Notify_followed
                            self.tw.send_dm(recipient_id=i, text=notif)
                            self.tw.followed.append(i)

                except Exception as ex:
                    print(ex)
                    pass
            
            if 'idle' in indicator:
                indicator.remove('idle')      
            sleep(67)


    def __update_dm(self, dms, indicator):
        while True:
            dms_new = self.tw.read_dm()
            indicator.remove('dm_safe')
            dms.extend(dms_new)
            indicator.add('dm_safe')
            sleep(5)
    

    def update_file_heroku(self, sender_id, message, postid):
        screen_name = self.tw.get_user_screen_name(sender_id)
        if exists(self.AdminCmd.filename_github):
            with open(self.AdminCmd.filename_github, 'r+') as f:
                data = load(f)
                for x in range(len(data)):
                    if int(data[x]['id']) == int(sender_id):
                        data[x]['username'] = screen_name
                        data[x]['menfess'].append({'postid':postid, 'text':message})
                        break
                else:
                    data.append({'username':screen_name, 'id':int(sender_id),
                        'menfess': [{'postid':postid, 'text':message}]})
                f.seek(0)
                dump(data, f, indent=4)
                f.truncate()
                f.close()
        else:
            with open(self.AdminCmd.filename_github, 'w') as f:
                f.write("[]")
                f.close()


    def start_autobase(self):
        print("Starting program...")
        dms = list()
        indicator = {'idle', 'dm_safe'}
        Thread(target=self.__update_follow, args=[indicator]).start()
        while 'idle' in indicator:
            sleep(3)
        Thread(target=self.__update_dm, args=[dms, indicator]).start()
        # for i in administartor_data.Admin_id:
        #     sent = self.tw.send_dm(recipient_id=i, text="Twitter autobase is starting...!")

        while True:
            if len(dms) != 0:

                # Cleaning dms
                dmsCopy = dms.copy()
                while 'dm_safe' not in indicator:
                    sleep(1)
                dms.clear()

                if self.credential.Notify_queue is True:
                    # Notify the menfess queue to sender
                    self.tw.notify_queue(dmsCopy)

                for i in range(len(dmsCopy)):
                    try:
                        message = dmsCopy[i]['message']
                        sender_id = dmsCopy[i]['sender_id']
                        media_url = dmsCopy[i]['media_url']
                        attachment_urls = dmsCopy[i]['attachment_urls']['tweet']
                        list_attchmentUrlsMedia = dmsCopy[i]['attachment_urls']['media']
                        
                        if any(j.lower() in message.lower() for j in self.credential.Trigger_word):
                            # Keyword Deleter
                            if self.credential.Keyword_deleter is True:
                                message = message.split()
                                list_keyword = [j.lower() for j in self.credential.Trigger_word] + \
                                            [j.upper() for j in self.credential.Trigger_word] + \
                                            [j.capitalize() for j in self.credential.Trigger_word]

                                [message.remove(j) for j in list_keyword if j in message]
                                message = " ".join(message)

                            # Cleaning attachment_url
                            if attachment_urls != (None, None):
                                message = message.split()
                                if attachment_urls[0] in message:
                                    message.remove(attachment_urls[0])
                                message = " ".join(message)
                            
                            # Cleaning hashtags and mentions
                            message = message.replace("#", "#/")
                            message = message.replace("@", "@/")

                            # Private_mediaTweet
                            media_idsAndTypes = list() # e.g [(media_id, media_type), (media_id, media_type), ]
                            # Pay attention to append and extend!
                            if self.credential.Private_mediaTweet is True:
                                for media_tweet_url in list_attchmentUrlsMedia:
                                    list_mediaIdsAndTypes = self.tw.upload_media_tweet(media_tweet_url[1])
                                    if len(list_mediaIdsAndTypes) != 0:
                                        media_idsAndTypes.extend(list_mediaIdsAndTypes)
                                        message = message.split()
                                        message.remove(media_tweet_url[0])
                                        message = " ".join(message)
                            
                            # Menfess contains sensitive contents
                            possibly_sensitive = False
                            if self.credential.Sensitive_word.lower() in message.lower():
                                possibly_sensitive = True

                            # POST TWEET
                            print("Posting menfess...")
                            postid = self.tw.post_tweet(message, sender_id, media_url=media_url, attachment_url=attachment_urls[1],
                                    media_idsAndTypes=media_idsAndTypes, possibly_sensitive=possibly_sensitive)
                            
                            # update heroku database
                            if self.database_indicator is True:
                                self.update_file_heroku(sender_id, message, postid)

                            if postid == None:
                                # Error happen on system
                                text = self.credential.Notify_sentFail1
                                self.tw.send_dm(recipient_id=sender_id, text=text)

                        else:
                            # Notify sender, message doesn't meet the algorithm's requirement
                            self.tw.send_dm(sender_id, self.credential.Notify_sentFail2)

                    except Exception as ex:
                        print(ex)
                        sleep(30)
                        pass

            else:
                sleep(3)

            
    def check_file_github(self, new=True):
        '''
        True when bot was just started, download & save file from github
        False when bot is running. If file exists, doesn't save the file from github.
        'new' parameter used if you update database not every midnight on Database method
        '''
        print("checking github file...")
        try:
            datee = datetime.now(timezone.utc) + \
                timedelta(hours=self.credential.Timezone)
            self.AdminCmd.filename_github = "{} {}-{}-{}.json".format(
                self.bot_username, datee.year, datee.month, datee.day)
            contents = self.AdminCmd.repo.get_contents("")

            if any(self.AdminCmd.filename_github == content.name for content in contents):
                # If filename exists in github. But, when midnight,
                # filename automatically changed.
                print(f"filename_github detected, new: {str(new)}")
                if new == False:
                    return
                for content in contents:
                    if self.AdminCmd.filename_github == content.name:
                        contents = content.decoded_content.decode()
                        break
            else:
                print("filename_github not detected")
                contents = "[]"
                self.AdminCmd.repo.create_file(self.AdminCmd.filename_github, "first commit",
                                contents)

            if exists(self.AdminCmd.filename_github) == False:
                with open(self.AdminCmd.filename_github, 'w') as f:
                    f.write(contents)
                    f.close()
            else:
                pass

            old_filename = "{} {}-{}-{}.json".format(
                    self.bot_username, datee.year, datee.month, datee.day - 1)

            if exists(old_filename):
                remove(old_filename)
                print("Heroku yesterday's Database has been deleted")
            else:
                print("Heroku yesterday's Database doesn't exist")

        except Exception as ex:
            pass
            print(ex)


    def database(self):
        while True:
            try:
                # update every midnight, you can update directly from DM with 'db_update'
                # check on administrator_data.py
                datee = datetime.now(timezone.utc) + timedelta(hours=self.credential.Timezone)
                if self.AdminCmd.filename_github != f"{self.bot_username} {datee.year}-{datee.month}-{datee.day}.json":
                    print("Github threading active...")
                    contents = self.AdminCmd.repo.get_contents(self.AdminCmd.filename_github)
                    with open(self.AdminCmd.filename_github) as f:
                        self.AdminCmd.repo.update_file(contents.path, "updating Database", f.read(), contents.sha)
                        f.close()
                    self.check_file_github(new=False)
                    print("Github Database updated")
                    sleep(60)

                else:
                    sleep(60)

            except Exception as ex:
                print(ex)
                print("Github threading failed..")
                sleep(720)
                pass


    def start_database(self):
        self.database_indicator = True
        github = Github(self.credential.Github_token)

        datee = datetime.now(timezone.utc) + timedelta(hours=self.credential.Timezone)
        self.AdminCmd.filename_github = "{} {}-{}-{}.json".format(
            self.bot_username, datee.year, datee.month, datee.day)
        self.AdminCmd.repo = github.get_repo(self.credential.Github_repo)

        self.check_file_github(new=True)
        Thread(target=self.database).start()


if __name__ == "__main__":
    import administrator_data
    
    User = Autobase(administrator_data)
    if administrator_data.Database is True:
        User.start_database()

    User.start_autobase()

