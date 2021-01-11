# Original code by Prieyudha Akadita S.
#     Source: https://https://github.com/ydhnwb/autodm_base
# Re-code by Fakhri Catur Rofi under MIT License
#     Source: https://github.com/fakhrirofi/twitter_autobase

from command import AdminCommand, UserCommand
from tweepy import OAuthHandler, API, Cursor
from time import sleep
from os import remove
from requests import get
from requests_oauthlib import OAuth1
from async_upload import MediaUpload
from html import unescape
from datetime import datetime, timezone, timedelta
from re import sub, search
from watermark import app as wm


class Twitter:
    '''
    :param credential: class that contains objects like administrator_data -> object
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
        
        :param credential: class that contains objects like administrator_data -> object
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
        self.random_time = credential.Delay_time
        self.db_sent = dict() # dict of sender and his postid, update every midnight with self.day
        self.day = (datetime.now(timezone.utc) + timedelta(hours=credential.Timezone)).day
        self.db_received = list() # list of 55 received menfess's message id
        self.indicator_start = False
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


    def read_dm(self):
        '''Read and filter DMs
        This method contains AdminCmd and UserCmd that can do exec and
        self.db_sent updater.
        Filters:
            - received dm
            - admin & user command
            - interval per sender
            - account status
            - blacklist words
            - only followed
            - sender requirements
            - menfess trigger
                - attachment_url
                - photo
                - video
                - animated_gif
        :returns: list of dict filtered DMs
        '''
        # Update db_sent
        self.db_sent_updater('update')

        print("Getting direct messages...")
        dms = list()
        try:
            api = self.api
            dm = api.list_direct_messages(count=50)

            # FILL DB_RECEIVED WHEN BOT WAS JUST STARTED (Keep_DM)
            if self.indicator_start is False:
                self.indicator_start = True

                if self.credential.Keep_DM is True:
                    for x in dm:
                        self.db_received.append(x.id)
                    # Ignore messages that received before bot started
                    return dms
            
            # Check Account_status to make process (after Turned off) faster
            if self.credential.Account_status is True:
                dm.reverse()
            else:
                for x in range(len(dm)):
                    message = dm[x].message_create['message_data']['text'].lower()
                    if "#switch on" in message:
                        self.credential.Account_status = True
                        self.delete_dm(dm[x].id)
                        self.send_dm(dm[x].message_create['sender_id'],"processed: #switch on")
                        del dm[x]
                        dm.reverse()
                        break

                    elif any(i in message for i in self.credential.Admin_cmd):
                        dm.reverse()
                        break

                else:
                    print("Account status: False; AdminCmd not found")
                    return dms

            for x in range(len(dm)):
                sender_id = dm[x].message_create['sender_id'] # str
                message_data = dm[x].message_create['message_data']
                message = message_data['text']
                id = dm[x].id

                # Message id is already stored on db_received, the message will be skipped (Keep_DM)
                if id in self.db_received:
                    continue

                # Avoid keyword error by skipping bot messages
                if sender_id == str(self.me.id):
                    self.delete_dm(id)
                    continue

                # ADMIN & USER COMMAND
                list_command = list(self.credential.Admin_cmd) + list(self.credential.User_cmd)
                command = message.split()[0].lower()
                if any(i == command for i in list_command):
                    # delete DM to avoid repeated command
                    self.delete_dm(id)

                    AdminCmd = self.AdminCmd #pylint: disable=unused-variable
                    UserCmd = self.UserCmd #pylint: disable=unused-variable
                    command, *contents = message.split()
                    notif = str()
                    
                    if command.lower() in self.credential.Admin_cmd:
                        # Manage admin access
                        if sender_id not in self.credential.Admin_id:
                            notif = self.credential.Notify_wrongTrigger
                            self.send_dm(recipient_id=sender_id, text=notif)
                            continue
                        else:
                            pass
                    print(f"command {command} {str(contents)} in progress...")

                    dict_command = self.credential.Admin_cmd.copy()
                    dict_command.update(self.credential.User_cmd)

                    if len(contents) != 0:
                        urls = message_data["entities"]["urls"]
                        for arg in contents:
                            try:
                                notif += f"\nprocessed: {command} {arg}"
                                fix_command = dict_command[command.lower()]
                                exec(fix_command)
                                if "urls" in fix_command:
                                    break

                            except Exception as ex:
                                pass
                                print(ex)
                                notif += f"\nException: {ex}"
                    else:
                        try:
                            notif += f"\nprocessed: {command}"
                            exec(dict_command[command.lower()])
                        except Exception as ex:
                            pass
                            print(ex)
                            notif += f"\nException: {ex}"
                    
                    # Skip notif if '#no_notif' in command's comment
                    if "#no_notif" in dict_command[command.lower()]:
                        if "Exception" not in notif:
                            continue
                    
                    # Manage notification for user
                    if sender_id not in self.credential.Admin_id:
                        if "Exception" not in notif:
                            notif = self.credential.Notify_userCmdDelete
                        else:
                            notif = self.credential.Notify_userCmdDeleteFail
                    
                    self.send_dm(sender_id, notif)
                    continue
                
                # ACCOUNT STATUS
                if self.credential.Account_status is False:
                    continue

                # Interval time per sender
                if self.credential.Interval_perSender is True and sender_id not in self.credential.Admin_id:
                    date_now = datetime.now(timezone.utc) + timedelta(hours=self.credential.Timezone)
                    for i in list(self.db_intervalTime):
                        # cleaning self.db_intervalTime
                        if self.db_intervalTime[i] < date_now:
                            del self.db_intervalTime[i]

                    if sender_id in self.db_intervalTime:
                        continue
                    else:
                        self.db_intervalTime[sender_id] = date_now + timedelta(seconds=self.credential.Interval_time)

                # Delete or store message id to avoid repeated menfess (Keep_DM)
                if self.credential.Keep_DM is True:     
                    if len(self.db_received) > 55:
                        self.db_received.pop(0)
                    self.db_received.append(id)

                else:
                    self.delete_dm(id)

                # ONLY FOLLOWED
                if self.credential.Only_followed is True and sender_id not in self.credential.Admin_id:
                    if int(sender_id) not in self.followed:
                        self.send_dm(sender_id, self.credential.Notify_notFollowed)
                        continue

                # Minimum lenMenfess
                if len(message) < self.credential.Minimum_lenMenfess and sender_id not in self.credential.Admin_id:
                    self.send_dm(sender_id, self.credential.Notify_senderRequirements)
                    continue

                # SENDER REQUIREMENTS
                if self.credential.Sender_requirements is True and sender_id not in self.credential.Admin_id:
                    indicator = 0
                    user = (api.get_user(sender_id))._json
                    # minimum followers
                    if user['followers_count'] < self.credential.Minimum_followers:
                        indicator = 1
                    # minimum age
                    created_at = datetime.strptime(user['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                    now = (datetime.now(timezone.utc) + timedelta(hours=self.credential.Timezone)).replace(tzinfo=None)

                    if (now-created_at).days < self.credential.Minimum_day:
                        indicator = 1
                    
                    if indicator == 1:
                        self.send_dm(sender_id, self.credential.Notify_senderRequirements)
                        continue

                # BLACKLIST WORDS
                list_blacklist = [i.lower() for i in self.credential.Blacklist_words]
                if any(i in message.lower() for i in list_blacklist) and sender_id not in self.credential.Admin_id:
                    try:
                        print("Skipping blacklist menfess")
                        notif = self.credential.Notify_blacklistWords
                        self.send_dm(recipient_id=sender_id, text=notif)
                    except Exception as ex:
                        sleep(60)
                        print(ex)
                        pass

                    continue

                # MENFESS TRIGGER
                if any(j.lower() in message.lower() for j in self.credential.Trigger_word):

                    print("Getting message -> sender_id: " + str(sender_id))
                    dict_dms = dict(message=message, sender_id=sender_id,
                        media_url=None, attachment_urls={'tweet':(None, None),
                                                         'media':list()})

                    # attachment url
                    urls = message_data['entities']['urls']
                    for i in urls:
                        if "twitter.com/" in i['expanded_url'] and "/status/" in i['expanded_url']:
                            # i['url]: url in text message                          
                            # Media
                            if any(j in i['expanded_url'] for j in ['/video/', '/photo/', '/media/']):
                                dict_dms['attachment_urls']['media'].append((i['url'], i['expanded_url']))
                                #i['expanded_url'] e.g https://twitter.com/username/status/123/photo/1
                            
                            # Tweet
                            else:
                                dict_dms['attachment_urls']['tweet'] = (i['url'], i['expanded_url'])
                                #i['expanded_url'] e.g https://twitter.com/username/status/123?s=19

                    # attachment media
                    if 'attachment' in message_data:
                        media = message_data['attachment']['media']
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
                        
                        dict_dms['media_url'] = media_url

                    dms.append(dict_dms)

                # WRONG TRIGGER
                else:
                    notif = self.credential.Notify_wrongTrigger
                    self.send_dm(recipient_id=sender_id, text=notif)

                    # Send wrong menfess to admin
                    username = self.get_user_screen_name(sender_id)
                    notif = message + f"\nstatus: wrong trigger\nfrom: @{username}\nid: {sender_id}"

                    for admin in self.credential.Admin_id:
                        self.send_dm(recipient_id=admin, text=notif)
            
            print(str(len(dms)) + " messages collected")
            return dms

        except Exception as ex:
            pass
            print(ex)
            sleep(60)
            return dms


    def notify_queue(self, dms):
        """Notify the menfess queue to sender
        :param dms: dms that returned from self.read_dm -> list of dict
        """
        try:
            print("Notifying the queue to sender")
            x, y, z = -1, 0, 0
            # x is primary time (30 sec); y is queue; z is addition time for media
            time = datetime.now(timezone.utc) + timedelta(hours=self.credential.Timezone)
            for i in dms:
                y += 1
                x += (len(i['message']) // 272) + 1
                if i['media_url'] != None:
                    z += 3
                
                if self.credential.Private_mediaTweet is True:
                    z += len(i['attachment_urls']['media']) * 4

                # Delay for the first sender is very quick, so, it won't be notified
                if x == 0:
                    continue

                sent_time = time + timedelta(seconds= x*(32+self.random_time) + z)
                sent_time = datetime.strftime(sent_time, '%H:%M')
                notif = self.credential.Notify_queueMessage.format(str(y), sent_time)
                self.send_dm(recipient_id=i['sender_id'], text=notif)

        except Exception as ex:
            pass
            print(ex)
            sleep(60)


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
            sent = self.api.send_direct_message(recipient_id=recipient_id, text=text)
            self.delete_dm(sent.id)
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

        r = get(media_url, auth=oauth)

        if filename == None:
            for i in sub("[/?=]", " ", media_url).split():
                if search(r"\.mp4$|\.gif$|\.jpg$|\.jpeg$|\.png$|\.webp$", i):
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
                wm.watermark_text_image(filename, text=adm.Watermark_text,
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
            postid = sub(r"[/\.:]", " ", media_tweet_url).split()[-3]
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
                check = tweet[:limit].split()
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
                sleep(30+self.random_time)
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
                sleep(30+self.random_time)

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
