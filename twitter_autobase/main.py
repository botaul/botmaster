# Original code by Prieyudha Akadita S.
#     Source: https://https://github.com/ydhnwb/autodm_base

# Re-code by Fakhri Catur Rofi under MIT License
#     Source: https://github.com/fakhrirofi/twitter_autobase

from .twitter import Twitter
from time import sleep
from threading import Thread
from datetime import datetime, timezone, timedelta
from os.path import exists
from os import remove
from html import unescape
from github import Github
from json import dump, load
from .gh_db import check_file_github, update_local_file, gh_database


class Autobase(Twitter):
    '''
    :param credential: class that contains object class like config.py -> object 
    '''
    def __init__(self, credential):
        '''You can control account and bot using credential & tw attributes

        Attributes:
            - credential
            - tw
            - AdminCmd
            - bot_username
            - database_indicator

        :param credential: class that contains object class like config.py -> object
        '''
        super().__init__(credential)
        self.bot_username = self.me.screen_name
        self.database_indicator = False


    def __update_follow(self, indicator):
        api = self.api
        me = self.me
        inAccMsg = False # indicator for accept message
        inFoll = False # indicator for followed
        while True:
            # AUTO ACCEPT MESSAGE REQUESTS
            # self.tw.follower is only 110, and the get requests is only 50
            # the order is from new to old
            print("Accepting message requests...")
            try:
                follower = api.followers_ids(user_id=me.id, count=100)
                if len(follower) != 0:
                    if inAccMsg == False:
                        inAccMsg = True
                        self.follower = follower.copy()

                    for i in follower[::-1]:
                        if i not in self.follower:
                            notif = self.credential.Notify_acceptMessage
                            # I don't know, sometimes error happen here, so, I update self.tw.follower after send_dm
                            try:
                                self.send_dm(recipient_id=i, text=notif)
                                self.follower.insert(0, i)
                                if len(self.follower) > 110: self.follower.pop()
                            except Exception as ex:
                                print(ex)
                                pass
                                
            except Exception as ex:
                print(ex)
                sleep(60)
                pass

            # GETTING LIST OF FOLLOWED
            # self.tw.followed is from old to new
            if self.credential.Only_followed is True:
                try:
                    if inFoll == False:
                        inFoll = True
                        followed = self.get_all_followed(me.id, first_delay=False)
                        self.followed = followed[::-1]
                    else:
                        print("Updating friends ids...")
                        followed = api.friends_ids(user_id=me.id, count=50)
                    
                    for i in followed:
                        if i not in self.followed:
                            notif = self.credential.Notify_followed
                            self.send_dm(recipient_id=i, text=notif)
                            self.followed.append(i)

                except Exception as ex:
                    print(ex)
                    sleep(60)
                    pass
            
            if 'idle' in indicator:
                indicator.remove('idle')      
            sleep(67)


    def __update_dm(self, dms):
        '''
        delay 60s on self.tw.read_dm is moved here to make threading faster
        '''
        while True:
            dms_new = self.read_dm()
            if self.credential.Notify_queue is True:
                # notify queue to sender
                self.notify_queue(dms_new, queue=len(dms))

            dms.extend(dms_new)
            sleep(65)


    def start_autobase(self):
        '''
        the last self.tw.post_tweet delay is moved here to make threading faster
        '''
        print("Starting program...")
        dms = list()
        indicator = {'idle'}
        Thread(target=self.__update_follow, args=[indicator]).start()
        while 'idle' in indicator:
            sleep(1)
        Thread(target=self.__update_dm, args=[dms]).start()
        # for i in credential.Admin_id:
        #     sent = self.tw.send_dm(recipient_id=i, text="Twitter autobase is starting...!")

        while True:
            if len(dms) != 0:

                while len(dms) > 0:
                    dm = dms.pop(0)

                    try:
                        message = dm['message']
                        sender_id = dm['sender_id']
                        media_url = dm['media_url']
                        attachment_urls = dm['attachment_urls']['tweet']
                        list_attchmentUrlsMedia = dm['attachment_urls']['media']
                        
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
                                    list_mediaIdsAndTypes = self.upload_media_tweet(media_tweet_url[1])
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
                            postid = self.post_tweet(message, sender_id, media_url=media_url, attachment_url=attachment_urls[1],
                                    media_idsAndTypes=media_idsAndTypes, possibly_sensitive=possibly_sensitive)
                            
                            # update heroku/local database
                            if self.database_indicator is True:
                                update_local_file(self, sender_id, message, postid)

                            # NOTIFY MENFESS SENT OR NOT
                            if postid != None and self.credential.Notify_sent is True:
                                notif = self.credential.Notify_sentMessage.format(self.bot_username)
                                text = notif + str(postid)
                                self.send_dm(recipient_id=sender_id, text=text)                       
                            elif postid == None:
                                # Error happen on system
                                text = self.credential.Notify_sentFail1                           
                                self.send_dm(recipient_id=sender_id, text=text)
                            else:
                                # credential.Notify_sent is False
                                pass
                            
                            sleep(30+self.credential.Delay_time)

                        else:
                            # Notify sender, message doesn't meet the algorithm's requirement
                            self.send_dm(sender_id, self.credential.Notify_sentFail2)

                    except Exception as ex:
                        print(ex)
                        sleep(30)
                        pass

            else:
                sleep(3)


    def start_database(self, Github_database=True):
        self.database_indicator = True
        if Github_database is True:
            github = Github(self.credential.Github_token)
            self.AdminCmd.repo = github.get_repo(self.credential.Github_repo)
            self.AdminCmd.repo.indicator = True
            check_file_github(self, new=True)

        datee = datetime.now(timezone.utc) + timedelta(hours=self.credential.Timezone)
        self.AdminCmd.filename_github = "{} {}-{}-{}.json".format(
            self.bot_username, datee.year, datee.month, datee.day)   

        Thread(target=gh_database, args=[self, Github_database]).start()

if __name__ == "__main__":
    import config

    User = Autobase(config)
    if config.Database:
        User.start_database(config.Github_database)

    User.start_autobase()
