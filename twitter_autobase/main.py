# Original code by Prieyudha Akadita S.
#     Source: https://https://github.com/ydhnwb/autodm_base

# Re-code by Fakhri Catur Rofi under MIT License
#     Source: https://github.com/fakhrirofi/twitter_autobase

from .twitter import Twitter
from .gh_db import check_file_github, update_local_file, gh_database
from .webhook import webhook_manager as webMan
from .process_dm import process_dm
from .clean_dm_autobase import clean_main_autobase, clean_private_autobase
from time import sleep
from threading import Thread
from datetime import datetime, timezone, timedelta
from github import Github


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
        self.bot_id = str(self.me.id)
        self.database_indicator = False
        self.dms = list() #list of filtered dms that processed by process_dm


    def __update_follow(self, indicator):
        api = self.api
        me = self.me
        inAccMsg = False # indicator for accept message
        inFoll = False # indicator for followed
        while True:
            # AUTO ACCEPT MESSAGE REQUESTS
            # self.tw.follower is only 110, and the get requests is only 50
            # the order is from new to old
            if self.credential.Greet_newFollower:
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

    
    def notify_queue(self, dms, queue=0):
        """Notify the menfess queue to sender
        :param dms: dms that returned from self.read_dm -> list of dict
        :param queue: the current queue (len of current dms) -> int
        """
        try:
            x, y, z = -1 + queue, queue, 0
            # x is primary time (36 sec); y is queue; z is addition time for media
            time = datetime.now(timezone.utc) + timedelta(hours=self.credential.Timezone)
            for i in dms:
                y += 1
                x += (len(i['message']) // 272) + 1
                if i['media_url'] != None:
                    z += 3
                
                if self.credential.Private_mediaTweet:
                    z += len(i['attachment_urls']['media']) * 3

                # Delay for the first sender is very quick, so, it won't be notified
                if x == 0:
                    continue

                sent_time = time + timedelta(seconds= x*(37+self.credential.Delay_time) + z)
                sent_time = datetime.strftime(sent_time, '%H:%M')
                notif = self.credential.Notify_queueMessage.format(str(y), sent_time)
                self.send_dm(recipient_id=i['sender_id'], text=notif)

        except Exception as ex:
            pass
            print(ex)
            sleep(60)


    def update_dms(self, raw_dm):
        dm = process_dm(self, raw_dm)
        if self.credential.Notify_queue is True:
            # notify queue to sender
            self.notify_queue(dm, queue=len(self.dms))
        self.dms.extend(dm)


    def start_autobase(self):
        '''
        the last self.tw.post_tweet delay is moved here to make threading faster
        '''
        print("Starting program...")
        indicator = {'idle'}
        Thread(target=self.__update_follow, args=[indicator]).start()
        while 'idle' in indicator:
            sleep(1)
        
        # for i in credential.Admin_id:
        #     sent = self.tw.send_dm(recipient_id=i, text="Twitter autobase is starting...!")

        while True:
            while len(self.dms):
                dm = self.dms.pop(0)

                try:
                    message = dm['message']
                    sender_id = dm['sender_id']
                    media_url = dm['media_url']
                    attachment_urls = dm['attachment_urls']['tweet']
                    list_attchmentUrlsMedia = dm['attachment_urls']['media']

                    message = clean_main_autobase(self, message, attachment_urls)

                    # Private_mediaTweet
                    media_idsAndTypes = list() # e.g [(media_id, media_type), (media_id, media_type), ]
                    if self.credential.Private_mediaTweet:
                        message = clean_private_autobase(self, message, media_idsAndTypes, list_attchmentUrlsMedia)
                            
                    # Menfess contains sensitive contents
                    possibly_sensitive = False
                    if self.credential.Sensitive_word.lower() in message.lower():
                        possibly_sensitive = True

                    # POST TWEET
                    print("Posting menfess...")
                    postid = self.post_tweet(message, sender_id, media_url=media_url, attachment_url=attachment_urls[1],
                            media_idsAndTypes=media_idsAndTypes, possibly_sensitive=possibly_sensitive)
                            
                    # update heroku/local database
                    if self.database_indicator:
                        update_local_file(self, sender_id, message, postid)

                    # NOTIFY MENFESS SENT OR NOT
                    if postid != None and self.credential.Notify_sent:
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
                            
                    sleep(36+self.credential.Delay_time)

                except Exception as ex:
                    text = self.credential.Notify_sentFail1 + "\nError code: start_autobase method"
                    self.send_dm(recipient_id=sender_id, text=text)
                    print(ex)
                    sleep(30)
                    pass

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
