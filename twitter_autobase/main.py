# Original code by Prieyudha Akadita S.
#     Source: https://https://github.com/ydhnwb/autodm_base

# Re-code by Fakhri Catur Rofi under MIT License
#     Source: https://github.com/fakhrirofi/twitter_autobase

from .twitter import Twitter
from .gh_db import check_file_github, update_local_file, gh_database
from .webhook import webhook_manager as webMan
from .process_dm import process_dm
from .clean_dm_autobase import clean_main_autobase, clean_private_autobase
from .command import AdminCommand, UserCommand
from time import sleep
from threading import Thread
from datetime import datetime, timezone, timedelta
from github import Github


class Autobase(Twitter):
    '''
    :param credential: class that contains object class like config.py -> object
    :param prevent_loop: list
    '''
    def __init__(self, credential, prevent_loop):
        '''You can control account and bot using credential & tw attributes

        Attributes:
            - credential
            - AdminCmd
            - bot_username
            - database_indicator

        :param credential: class that contains object class like config.py -> object
        '''
        super().__init__(credential)
        self.bot_username = self.me.screen_name
        self.bot_id = str(self.me.id)
        self.database_indicator = False
        self.db_intervalTime = dict()
       
        self.db_sent = dict() # { 'sender_id': {'postid': [list_postid_thread],}, }
        self.db_deleted = dict() # { 'sender_id': ['postid',] }
        self.day = (datetime.now(timezone.utc) + timedelta(hours=credential.Timezone)).day
        
        self.AdminCmd = AdminCommand(self.api, credential)
        self.UserCmd = UserCommand(self.api, credential)

        self.dms = list() # list of filtered dms that processed by process_dm

        self.prevent_loop = prevent_loop # list of all bot_id (str) that runs using this bot to prevent loop messages from each accounts

    
    def notify_follow(self, follow_events):
        '''
        :param follow_events: dict of 'follow_events' from self.webhook_connector
        '''
        if follow_events['follow_events'][0]['type'] != 'follow':
            return

        # id of the user who clicks 'follow' buttons
        source_id = follow_events['follow_events'][0]['source']['id']
        
        # Greet to new follower
        if source_id not in self.prevent_loop: # user is not bot
            if self.credential.Greet_newFollower:
                self.send_dm(source_id, self.credential.Notif_newFollower)

        # Notify user followed by bot, (admin of the bot clicks follow buttons on user profile)
        # elif source_id in self.prevent_loop:
        elif self.credential.Greet_followed:
            target_id = follow_events['follow_events'][0]['target']['id']

            if target_id not in self.prevent_loop:
                self.send_dm(target_id, self.credential.Notif_followed)


    def db_sent_updater(self, action, sender_id=str(), postid=str(), list_postid_thread=list()):
        '''Update self.db_sent
        :param action: 'update','add_sent', 'add_deleted' or 'delete_sent' -> str
        :param sender_id: sender id who has sent the menfess -> str
        :param postid: tweet id or (sender_id, tweet id) -> str or tuple
        '''
        try:
            if action == 'update':
                day = (datetime.now(timezone.utc) + timedelta(hours=self.credential.Timezone)).day
                if day != self.day:
                    self.day = day
                    self.db_sent.clear()
                    self.db_deleted.clear()
            
            elif action == 'add_sent':
                if sender_id not in self.db_sent: # require sender_id, postid, list_postid_thread
                    self.db_sent[sender_id] = {postid: list_postid_thread}
                else: self.db_sent[sender_id][postid] = list_postid_thread
            
            elif action == 'add_deleted': # require sender_id and postid
                if sender_id not in self.db_deleted:
                    self.db_deleted[sender_id] = [postid]
                else: self.db_deleted[sender_id] += [postid]

            elif action == 'delete_sent': # require sender_id and postid
                del self.db_sent[sender_id][postid]
                if len(self.db_sent[sender_id]) == 0:
                    del self.db_sent[sender_id]

        except Exception as ex:
            pass
            print(ex)

    
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


    def webhook_connector(self, raw_data):
        # https://developer.twitter.com/en/docs/twitter-api/enterprise/account-activity-api/guides/account-activity-data-objects
        if 'direct_message_events' in raw_data:
            dm = process_dm(self, raw_data)
            if self.credential.Notify_queue is True:
                # notify queue to sender
                self.notify_queue(dm, queue=len(self.dms))
            self.dms.extend(dm)
        
        elif 'follow_events' in raw_data:
            self.notify_follow(raw_data)


    def start_autobase(self):
        '''
        the last self.tw.post_tweet delay is moved here to make threading faster
        '''
        print("Starting autobase...")

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
                    response = self.post_tweet(message, sender_id, media_url=media_url, attachment_url=attachment_urls[1],
                            media_idsAndTypes=media_idsAndTypes, possibly_sensitive=possibly_sensitive)
                            
                    # update heroku/local database
                    if self.database_indicator:
                        update_local_file(self, sender_id, message, response['postid'])

                    # NOTIFY MENFESS SENT OR NOT
                    if response['postid'] != None:
                        if self.credential.Notify_sent:
                            notif = self.credential.Notify_sentMessage.format(self.bot_username)
                            text = notif + str(response['postid'])
                            self.send_dm(recipient_id=sender_id, text=text)

                        # ADD TO DB_SENT
                        self.db_sent_updater('add_sent', sender_id, response['postid'], response['list_postid_thread'])

                    elif response['postid'] == None:
                        # Error happen on system
                        text = self.credential.Notify_sentFail1 + f"\nerror_code: {response['error_code']}"                         
                        self.send_dm(recipient_id=sender_id, text=text)
                    else:
                        # credential.Notify_sent is False
                        pass
                            
                    sleep(36+self.credential.Delay_time)

                except Exception as ex:
                    text = self.credential.Notify_sentFail1 + "\nerror_code: start_autobase method, " + str(ex)
                    self.send_dm(recipient_id=sender_id, text=text)
                    print(ex)
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
