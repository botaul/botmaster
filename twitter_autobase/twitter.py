# Original code by Prieyudha Akadita S.
#     Source: https://https://github.com/ydhnwb/autodm_base
# Re-code by Fakhri Catur Rofi
#     Source: https://github.com/fakhrirofi/twitter_autobase

from .command import AdminCommand, UserCommand
from .watermark import app as watermark
from .async_upload import MediaUpload
from tweepy import OAuthHandler, API, Cursor
from time import sleep
from os import remove
import requests
from requests_oauthlib import OAuth1
from html import unescape
from datetime import datetime, timezone, timedelta
import re


class Twitter:
    '''
    :param credential: class that contains objects like config -> object
    '''

    def __init__(self, credential):
        '''
        initialize twitter with tweepy
        Attributes:
            - credential
            - api
            - AdminCmd
            - UserCmd
            - me
            - follower
            - followed
            - random_time
            - db_sent
            - day
            - db_received
            - indicator_start
            - db_intervalTime
        
        :param credential: class that contains objects like config -> object
        '''
        self.credential = credential

        print("Initializing twitter...")
        auth = OAuthHandler(
            credential.CONSUMER_KEY, credential.CONSUMER_SECRET)
        auth.set_access_token(
            credential.ACCESS_KEY, credential.ACCESS_SECRET)
        self.api = API(
            auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        
        self.AdminCmd = AdminCommand(self.api, credential)
        self.UserCmd = UserCommand(self.api, credential)

        self.me = self.api.me()
        self.follower = list() # list of integer
        self.followed = list() # list of integer
        self.db_sent = dict() # dict of sender and his postid, update every midnight with self.day
        self.day = (datetime.now(timezone.utc) + timedelta(hours=credential.Timezone)).day
        self.db_intervalTime = dict()
    

    def get_all_followers(self, user_id, first_delay=True):
        '''Return all followers ids
        Twitter API limiting to get 5000 followers/minute
        :param user_id: User id -> int or str
        :param first_delay: False: delete delay for first operation -> bool
        :returns: list of followers ids integer
        '''
        try:
            print("Getting all followers ids...")
            ids = list()
            for page in Cursor(self.api.followers_ids, user_id=user_id).pages():
                ids.extend(page)
                if first_delay is False:
                    first_delay = True
                    continue
                sleep(60)
            return ids

        except Exception as ex:
            pass
            print(ex)
            sleep(60)
            return list()

    
    def get_all_followed(self, user_id, first_delay=True):
        '''Get all account ids that followed by screen_name
        Twitter api limiting to get 5000 followed/minute
        :param user_id: user id -> str or int
        :param first_delay: False: delete delay for first operation -> bool
        :returns: list of followers ids integer
        '''
        try:
            print("Getting all friends ids...")
            ids = list()
            for page in Cursor(self.api.friends_ids, user_id=user_id).pages():
                ids.extend(page)
                if first_delay is False:
                    first_delay = True
                    continue
                sleep(60)
            return ids

        except Exception as ex:
            pass
            print(ex)
            sleep(60)
            return list()
    

    def db_sent_updater(self, action, sender_id=None, postid=None):
        '''Update self.db_sent
        :param action: 'update','add' or 'delete' -> str
        :param sender_id: sender id who has sent the menfess -> str
        :param postid: tweet id or (sender_id, tweet id) -> str or tuple
        '''
        try:
            if action == 'update':
                day = (datetime.now(timezone.utc) + timedelta(hours=self.credential.Timezone)).day
                if day != self.day:
                    self.day = day
                    self.db_sent.clear()
            
            elif action == 'add':
                if sender_id not in self.db_sent:
                    self.db_sent[sender_id] = [postid]
                else: self.db_sent[sender_id] += [postid]
            
            elif action == 'delete':
                self.db_sent[sender_id].remove(postid)
                if len(self.db_sent[sender_id]) == 0:
                    del self.db_sent[sender_id]

        except Exception as ex:
            pass
            print(ex)


    def delete_dm(self, id):
        '''Delete a DM
        :param id: message id -> int or str
        '''
        try:
            self.api.destroy_direct_message(id)
        except Exception as ex:
            print(ex)
            sleep(60)
            pass
    
    
    def send_dm(self, recipient_id, text):
        '''Send DM and automatically delete the sent DM
        :param recipient_id: -> str or int
        :param text: -> str
        '''
        try:
            self.api.send_direct_message(recipient_id=recipient_id, text=text)
        except Exception as ex:
            pass
            print(ex)
            sleep(60)


    def get_user_screen_name(self, id):
        '''Get username
        :param id: account id -> int
        :returns: username -> str
        '''
        try:
            user = self.api.get_user(id)
            return user.screen_name

        except Exception as ex:
            pass
            print(ex)
            sleep(60)
            return "Exception"


    def download_media(self, media_url, filename=None):
        '''Download media from url
        :param media_url: url -> string
        :param filename: None (default) or filename --> str
        :returns: file name (when filename=None) -> str
        '''
        print("Downloading media...")
        oauth = OAuth1(client_key=self.credential.CONSUMER_KEY,
                       client_secret=self.credential.CONSUMER_SECRET,
                       resource_owner_key=self.credential.ACCESS_KEY,
                       resource_owner_secret=self.credential.ACCESS_SECRET)

        r = requests.get(media_url, auth=oauth)

        if filename == None:
            for i in re.sub("[/?=]", " ", media_url).split():
                if re.search(r"\.mp4$|\.gif$|\.jpg$|\.jpeg$|\.png$|\.webp$", i):
                    filename = i
                    break
            if filename == None:
                raise Exception("filename is not supported, please check the link")

        with open(filename, 'wb') as f:
            f.write(r.content)
            f.close()

        print("Download media successfully")
        return filename
    

    def add_watermark(self, filename, output=None):
        '''Add watermark to photo, then save as output
        Only support photo, if other, nothing will happen
        :param filename: file name -> str
        :param output: output name -> str
        :returns: output name -> str
        '''
        try:
            if output == None:
                output = filename

            file_type = filename.split('.')[-1]
            if file_type in "jpg jpeg png webp":
                print("Adding watermark...")
                adm = self.credential
                watermark.watermark_text_image(filename, text=adm.Watermark_text, font=adm.Watermark_font,
                ratio=adm.Watermark_ratio, pos=adm.Watermark_position,
                output=output, color=adm.Watermark_textColor,
                stroke_color=adm.Watermark_textStroke, watermark=adm.Watermark_image)
            
            return output

        except Exception as ex:
            pass
            print(ex)
            return filename


    def upload_media_tweet(self, media_tweet_url):
        '''Upload media with (from) media tweet url
        Usually when sender want to post more than one media, he will attachs media tweet url.
        But the sender's username is mentioned on the bottom of the media.
        This method intended to make sender anonym. This return list of media_ids, then
        you can add media_ids to other method. Contains watermark module
        :param media_tweet_url: media tweet url e.g https://twitter.com/username/status/123/photo/1 -> str
        :returns: [(media_id, media_type),] a.k.a media_idsAndTypes -> list
        '''
        try:
            postid = re.sub(r"[/\.:]", " ", media_tweet_url).split()[-3]
            status = self.api.get_status(postid)
            media_idsAndTypes = list()

            if 'extended_entities' not in status._json:
                return list()
            print("Uploading media tweet...")
            
            for media in status._json['extended_entities']['media']:
                media_type = media['type']

                if media_type == 'photo':
                    media_url = media['media_url']

                elif media_type == 'video':
                    media_urls = media['video_info']['variants']
                    temp_bitrate = list()
                    for varian in media_urls:
                        if varian['content_type'] == "video/mp4":
                            temp_bitrate.append((varian['bitrate'], varian['url']))
                    # sort to choose the highest bitrate
                    temp_bitrate.sort()
                    media_url = temp_bitrate[-1][1]

                elif media_type == 'animated_gif':
                    media_url = media['video_info']['variants'][0]['url']

                filename = self.download_media(media_url)

                # Add watermark
                if self.credential.Watermark is True:
                    self.add_watermark(filename)

                media_id, media_type = self.upload_media(filename)
                remove(filename)
                media_idsAndTypes.append((media_id, media_type))
        
            return media_idsAndTypes # e.g [(media_id, media_type), (media_id, media_type), ]

        except Exception as ex:
            pass
            print(ex)
            sleep(60)
            return list()


    def upload_media(self, filename, media_category='tweet'):
        '''Upload media with chunk
        This method are needed when you want to use media to do something on
        twitter. This returns list of media_id, you can attach it to other method
        that require media id.
        :param filename: -> str
        :param media_category: 'tweet' or 'dm'. default to 'tweet'
        :returns: media id, media_type -> tuple
        '''
        mediaupload = MediaUpload(self.credential, filename, media_category)
        media_id, media_type = mediaupload.upload_init()
        mediaupload.upload_append()
        mediaupload.upload_finalize()
        return media_id, media_type



    def post_tweet(self, tweet, sender_id, media_url=None, attachment_url=None,
                media_idsAndTypes=list(), possibly_sensitive=False):
        '''Post a tweet, contains watermark module and self.db_sent updater
        Per tweet delay is 30s + self.random_time, but the last delay is deleted
        :param tweet: -> str
        :param sender_id: -> str or int
        :param media_url: media url that will be posted -> str
        :param attachment_url: url -> str
        :param media_idsAndTypes: [(media_ids, media_type),] -> list
        :param possibly_sensitive: True when menfess contains sensitive contents -> bool
        :returns: tweet id -> str
        '''
        try:
            #### ADD MEDIA_ID AND MEDIA_TYPE TO LIST_MEDIA_IDS ####
            # mediaIdsAndTypes e.g. [(media_id, media_type), (media_id, media_type), ]
            if media_url != None:
                tweet = tweet.split()
                tweet = " ".join(tweet[:-1])
                filename = self.download_media(media_url)

                # Add watermark
                if self.credential.Watermark is True:
                    self.add_watermark(filename)

                media_id, media_type = self.upload_media(filename)
                # Add attachment media from DM to the first order
                media_idsAndTypes.insert(0, (media_id, media_type))
                remove(filename)

            list_media_ids = [[]] # e.g. [[media_ids],[media_ids],[media_ids]]
            temp = 0
            while len(media_idsAndTypes) != 0:
                if temp == 0:
                    temp = 1
                    list_media_ids = list()
                media_ids = list()
                added = 0
                for media_id, media_type in media_idsAndTypes[:4]:
                    if media_type == 'video' or media_type == 'animated_gif':
                        if added == 0:
                            media_ids.append(media_id)
                            added += 1
                        break
                    media_ids.append(media_id)
                    added += 1

                list_media_ids.append(media_ids)
                # media_idsAndTypes are dynamic here
                media_idsAndTypes = media_idsAndTypes[added:]
            
            #### POST TWEET ####
            postid = 0
            # postid is the first tweet of the tweets thread
            while len(tweet) > 280:
            # Making a Thread.
                limit = 272

                # some emoticons count as 2 char
                EMOJI = re.compile("["
                    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
                    "\U0001F300-\U0001F5FF"  # symbols & pictographs
                    "\U0001F600-\U0001F64F"  # emoticons
                    "\U0001F680-\U0001F6FF"  # transport & map symbols
                    "\U0001F700-\U0001F77F"  # alchemical symbols
                    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                    "\U0001FA00-\U0001FA6F"  # Chess Symbols
                    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                    "\U00002702-\U000027B0"  # Dingbats
                    "\U000024C2-\U0001F251" 
                    "]+")
                len_emoji = len(re.findall(EMOJI, tweet[:limit]))
                limit -= round(len_emoji / 2)

                check = tweet[:limit].split()                             
                if len(check) == 1:
                    # avoid error when user send 272 char in one word
                    separator = 0
                else:
                    separator = len(check[-1])
                    if tweet[limit-1] == " ":
                        separator += 1

                tweet1 = unescape(tweet[:limit-separator]) + '-cont-'
                
                if postid == 0:
                    print("Making a thread...")
                    # postid is static after first update.
                    postid = self.api.update_status(
                        tweet1, attachment_url=attachment_url, media_ids=list_media_ids[:1][0],
                        possibly_sensitive=possibly_sensitive).id
                    postid1 = postid
                else:
                    postid1 = self.api.update_status(
                        tweet1, in_reply_to_status_id=postid1, auto_populate_reply_metadata=True,
                        media_ids=list_media_ids[:1][0], possibly_sensitive=possibly_sensitive).id
                
                list_media_ids = list_media_ids[1:] + [[]]
                sleep(36+self.credential.Delay_time)
                # tweet are dynamic here
                tweet = tweet[limit-separator:]
            
            # Above and below operation differences are on tweet1 and unescape(tweet), also tweet[limit-separator:]
            # It's possible to change it to be one function
            if postid == 0:
                # postid is static after first update.
                postid = self.api.update_status(
                        unescape(tweet), attachment_url=attachment_url, media_ids=list_media_ids[:1][0],
                        possibly_sensitive=possibly_sensitive).id
                postid1 = postid        
            else:
                postid1 = self.api.update_status(
                    unescape(tweet), in_reply_to_status_id=postid1, auto_populate_reply_metadata=True,
                    media_ids=list_media_ids[:1][0], possibly_sensitive=possibly_sensitive).id
            
            list_media_ids = list_media_ids[1:] + [[]]

            # When media_ids still exists, It will be attached to the subsequent tweets
            while len(list_media_ids[0]) != 0: # Pay attention to the list format, [[]]
                sleep(36+self.credential.Delay_time)

                print("Posting the rest of media...")
                postid1 = self.api.update_status(
                    in_reply_to_status_id=postid1,
                    auto_populate_reply_metadata=True, media_ids=list_media_ids[:1][0],
                    possibly_sensitive=possibly_sensitive).id

                list_media_ids = list_media_ids[1:] + [[]]

            print('Menfess is posted -> postid:', str(postid))

            # ADD TO DB SENT
            self.db_sent_updater('add', sender_id, str(postid))
            
            return postid

        except Exception as ex:
            pass
            print(ex)
            sleep(60)
            return None
