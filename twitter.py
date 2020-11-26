# Original code by Prieyudha Akadita S.
#     Source: https://https://github.com/ydhnwb/autodm_base
# Re-code by Fakhri Catur Rofi under MIT License
#     Source: https://github.com/fakhrirofi/twitter_autobase

import administrator_data
import tmp
from tweepy import OAuthHandler, API, Cursor
from time import sleep
from os import remove
from requests import get
from requests_oauthlib import OAuth1
from async_upload import MediaUpload
from html import unescape
from datetime import datetime, timezone, timedelta
from re import sub, search


class Twitter:

    def __init__(self):
        '''
        initialize twitter with tweepy
        Attributes:
            - api
            - follower
            - bot_id
            - random_time
        '''
        print("Initializing twitter...")
        self.auth = OAuthHandler(
            administrator_data.CONSUMER_KEY, administrator_data.CONSUMER_SECRET)
        self.auth.set_access_token(
            administrator_data.ACCESS_KEY, administrator_data.ACCESS_SECRET)
        self.api = API(
            self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        self.follower = list() # list of integer
        self.followed = list() # list of integer
        self.bot_id = int() 
        self.random_time = administrator_data.Delay_time
    

    def get_all_followers(self, user_id, first_delay=True):
        '''Return all followers ids
        Twitter API limiting to get 5000 followers/minute
        :param screen_name: User id -> int or str
        :param first_delay: False: delete delay for first get -> bool
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
        :param screen_name: user id -> str or int
        :param first_delay: False: delete delay for first get -> bool
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


    def read_dm(self):
        '''Read and filter DMs
        Delay +- 60 seconds because of Twitter API limit.
        This method contains Set word that can do exec.
        Filters:
            - set from DM
            - blacklist words
            - only followed
            - sender requirements
            - primary keywords
                - attachment_url
                - photo
                - video
                - animated_gif
        :returns: list of filtered DMs
        '''
        print("Getting direct messages...")
        dms = list()
        try:
            api = self.api
            dm = list(reversed(api.list_direct_messages()))
            for x in range(len(dm)):
                sender_id = dm[x].message_create['sender_id'] # str
                message = dm[x].message_create['message_data']['text']
                message_data = dm[x].message_create['message_data']
                id = dm[x].id

                self.delete_dm(id)
                # Avoid keyword error by skipping bot messages
                if sender_id == self.bot_id:
                    continue

                # set from DM
                if administrator_data.Set_word.lower() in message.lower() and sender_id == administrator_data.Admin_id:
                    print("command in progress...")
                    try:
                        message = message.split()
                        command, *content = message[1:]
                        notif = "commands:"
                        if command.lower() in administrator_data.Dict_set.keys():
                            command1 = administrator_data.Dict_set[command.lower()]
                            if len(content) != 0:
                                for word in content:
                                    try:
                                        # Don't escape the word that will be Added to muted list
                                        if any(command.lower() == i for i in ['add_muted', 'rm_muted']):
                                            word = word.replace("_", " ")
                                        command2 = command1.format(f"{word}")
                                        notif += f"\nprocessing {command} {unescape(word)}"
                                        exec(command2)
                                    except Exception as ex:
                                        notif += f"\nexcept: {ex}"
                                        pass
                            else:
                                try:
                                    notif += f"\nprocessing {command}"
                                    exec(command1)
                                except Exception as ex:
                                    notif += f"\nexcept: {ex}"
                                    pass

                    except Exception as ex:
                        notif = "some commands failed" + \
                            f"\n{ex}" + f"\n{notif}"
                        print(ex)
                        pass

                    finally:
                        self.send_dm(recipient_id=sender_id, text=notif)

                    continue

                # only followed
                if administrator_data.Only_followed is True and sender_id != administrator_data.Admin_id:
                    if int(sender_id) not in self.followed:
                        self.send_dm(sender_id, administrator_data.Notify_notFollowed)
                        continue

                # sender requirements
                if administrator_data.Sender_requirements is True and sender_id != administrator_data.Admin_id:
                    indicator = 0
                    user = (api.get_user(sender_id))._json
                    # len menfess
                    if len(message) < administrator_data.Minimum_lenMenfess:
                        indicator = 1
                    # minimum followers
                    if user['followers_count'] < administrator_data.Minimum_followers:
                        indicator = 1
                    # minimum age
                    created_at = datetime.strptime(user['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                    now = (datetime.now(timezone.utc) + timedelta(hours=administrator_data.Timezone)).replace(tzinfo=None)
                    required_day = (administrator_data.Minimum_year * 365) + \
                                    (administrator_data.Minimum_month * 30) + \
                                    (administrator_data.Minimum_day)
                    if (now-created_at).days < required_day:
                        indicator = 1
                    
                    if indicator == 1:
                        self.send_dm(sender_id, administrator_data.Notify_senderRequirements)
                        continue

                # blacklist words
                list_blacklist = [i.lower() for i in administrator_data.Blacklist_words]
                if any(i in message.lower() for i in list_blacklist) and sender_id != administrator_data.Admin_id:
                    try:
                        print("Deleting muted menfess")
                        notif = "Menfess kamu mengandung muted words, jangan lupa baca peraturan base yaa!"
                        self.send_dm(recipient_id=sender_id, text=notif)
                    except Exception as ex:
                        sleep(60)
                        print(ex)
                        pass

                    continue

                # primary keywords
                if any(j.lower() in message.lower() for j in administrator_data.Trigger_word):

                    print("Getting message -> sender_id: " + str(sender_id))
                    dict_dms = dict(message=message, sender_id=sender_id,
                        media_url=None, attachment_urls={'tweet':(None, None),
                                                         'media':list()})

                    # attachment url
                    urls = message_data['entities']['urls']
                    for i in urls:
                        if "https://twitter.com/" in i['expanded_url'] and "/status/" in i['expanded_url']:
                            # i['url]: url in text message                          
                            # Media
                            if any(j in i['expanded_url'] for j in ['/video/', '/photo/', '/media/']):
                                dict_dms['attachment_urls']['media'].append((i['url'], i['expanded_url']))
                                #i['expanded_url'] e.g https://twitter.com/username/status/123/photo/1
                            
                            # Tweet
                            elif not any(j in i['expanded_url'] for j in ['/video/', '/photo/', '/media/']):
                                dict_dms['attachment_urls']['tweet'] = (i['url'], i['expanded_url'])
                                #i['expanded_url'] e.g https://twitter.com/username/status/123

                    # attachment media
                    if 'attachment' in message_data:
                        print("DM have an attachment")
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

                else:
                    try:
                        print("deleting message (keyword not in message)")
                        notif = administrator_data.Notify_wrongTrigger
                        self.send_dm(recipient_id=sender_id, text=notif)

                    except Exception as ex:
                        sleep(60)
                        print(ex)
                        pass
            
            print(str(len(dms)) + " messages collected")
            sleep(60)
            return dms

        except Exception as ex:
            pass
            print(ex)
            sleep(60)
            return dms


    def notify_queue(self, dms):
        """Notify the menfess queue to sender
        :param dms: dms that returned from self.read_dm -> dict
        """
        try:
            print("Notifying the queue to sender")
            x, y = 0, 0
            time = datetime.now(timezone.utc) + timedelta(hours=administrator_data.Timezone)
            for i in dms:
                y += 1
                x += (len(i['message']) // 272) + 1
                if i['media_url'] != None:
                    x += 0.2
                sent_time = time + timedelta(seconds= x*(30+self.random_time))
                sent_time = datetime.strftime(sent_time, '%H:%M')
                notif = administrator_data.Notify_queueMessage.format(str(y), sent_time)
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
            sleep(60)
            print(ex)


    def get_user_screen_name(self, id):
        '''Get username
        :param id: account id -> int
        :returns: username -> str
        '''
        try:
            print("Getting username...")
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
        try:
            print("Downloading media...")
            oauth = OAuth1(client_key=administrator_data.CONSUMER_KEY,
                           client_secret=administrator_data.CONSUMER_SECRET,
                           resource_owner_key=administrator_data.ACCESS_KEY,
                           resource_owner_secret=administrator_data.ACCESS_SECRET)

            r = get(media_url, auth=oauth)

            if filename == None:
                for i in sub("[/?=]", " ", media_url).split():
                    if search(r"\.mp4$|\.gif$|\.jpg$|\.png$|\.webp$", i):
                        filename = i
                        break
                if filename == None:
                    raise Exception("filename is not supported, please check the link")

            with open(filename, 'wb') as f:
                f.write(r.content)
                f.close()

            print("Download media successfully")
            return filename

        except Exception as ex:
            print(ex)
            pass
    

    def upload_media_tweet(self, media_tweet_url):
        '''Upload media with (from) media tweet url
        Usually when sender want to post more than one media, he will attachs media tweet url.
        But the sender's username is mentioned on the bottom of the media.
        This method intended to make sender anonym. This return list of media_ids, then
        you can add media_ids to other method.
        :param media_tweet_url: media tweet url e.g https://twitter.com/username/status/123/photo/1 -> str
        :returns: list of (media_id, media_type) a.k.a media_idsAndTypes -> list
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
        try:
            mediaupload = MediaUpload(filename, media_category)
            media_id, media_type = mediaupload.upload_init()
            mediaupload.upload_append()
            mediaupload.upload_finalize()
            return media_id, media_type

        except Exception as ex:
            pass
            print(ex)
            sleep(60)


    def post_tweet(self, tweet, media_url=None, attachment_url=None,
                media_idsAndTypes=list(), possibly_sensitive=False):
        '''Post a tweet
        :param tweet: -> str
        :param attachment_url: url -> str
        :param media_url: media url that will be posted -> str
        :param media_idsAndTypes: list of (media_ids, media_type) -> list
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
            sleep(30+self.random_time)

            # When media_ids still exists, It will be attached to the subsequent tweets
            while len(list_media_ids[0]) != 0: # Pay attention to the list format, [[]]
                print("Posting the rest of media...")
                postid1 = self.api.update_status(
                    f"Rest of media: {str(len(list_media_ids))}", in_reply_to_status_id=postid1,
                    auto_populate_reply_metadata=True, media_ids=list_media_ids[:1][0],
                    possibly_sensitive=possibly_sensitive).id

                list_media_ids = list_media_ids[1:] + [[]]
                sleep(30+self.random_time)

            print('Menfess\'s posted -> postid: ', str(postid))
            return postid

        except Exception as ex:
            pass
            print(ex)
            sleep(60)
            return None