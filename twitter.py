# Original code by Prieyudha Akadita S.
#     Source: https://https://github.com/ydhnwb/autodm_base
# Re-code by Fakhri Catur Rofi under MIT License
#     Source: https://github.com/fakhrirofi/twitter_autobase

import administrator_data
import temp
from tweepy import OAuthHandler, API, Cursor
from time import sleep
from os import remove
from os.path import exists
from requests import get
from requests_oauthlib import OAuth1
from async_upload import MediaUpload
from html import unescape
from datetime import datetime, timezone, timedelta
from random import randrange
from difflib import SequenceMatcher
from re import sub, search


class Twitter:

    def __init__(self):
        '''
        initialize tweepy
        objects:
            - api
            - follower
            - bot_id
            - day
        '''
        print("Initializing twitter...")
        self.auth = OAuthHandler(
            administrator_data.CONSUMER_KEY, administrator_data.CONSUMER_SECRET)
        self.auth.set_access_token(
            administrator_data.ACCESS_KEY, administrator_data.ACCESS_SECRET)
        self.api = API(
            self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        self.follower = list()
        self.bot_id = int()
        self.message_db = tuple()
        self.day = (datetime.now(timezone.utc) + timedelta(hours=administrator_data.Timezone)).day
    

    def get_all_followers(self, screen_name):
        # Twitter API limiting get 5000 followers/minute
        print("getting all followers...")
        ids = []
        for page in Cursor(self.api.followers_ids, screen_name=screen_name).pages():
            ids.extend(page)
            sleep(60)
        return ids


    def read_dm(self):
        '''
        Read and filter DMs
        Filters:
            - set from DM
            - check follower (exception for admin)
            - muted words (exception for admin)
            - similiarity checker
            - primary keywords
                - attachment
                    - attachment_url
                    - photo
                    - video
                    - animated_gif
        :returns: list of filtered DMs
        '''
        print("Get direct messages...")
        dms = list()
        try:
            api = self.api
            dm = list(reversed(api.list_direct_messages()))
            for x in range(len(dm)):
                sender_id = dm[x].message_create['sender_id']
                message = dm[x].message_create['message_data']['text']
                message_data = dm[x].message_create['message_data']
                id = dm[x].id

                self.delete_dm(id)
                # Avoid keyword error by skipping bot messages
                if int(sender_id) == self.bot_id:
                    continue

                # set from DM
                if administrator_data.Set_word.lower() in message.lower():
                    print("command in progress...")
                    try:
                        message = message.split()
                        command, *content = message[1:]
                        notif = "commands:"
                        if command in administrator_data.Dict_set.keys():
                            command1 = administrator_data.Dict_set[command]
                            if len(content) != 0:
                                for data in content:
                                    try:
                                        data = (unescape(data)).replace("_", " ")
                                        command2 = command1.format(f"\"{data}\"")
                                        notif += f"\nprocessing {command} \"{data}\""
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
                        sent = api.send_direct_message(
                            recipient_id=sender_id, text=notif).id
                        self.delete_dm(sent)

                    continue

                # check follower (Disable it when your followers are more than 5K)
                # elif int(sender_id) not in self.follower and sender_id != administrator_data.Admin_id:
                #     print("sender not in follower")
                #     try:
                #         notif = "Hmm kayaknya kamu belum follow base ini. Follow dulu ya biar bisa ngirim menfess"
                #         sent = api.send_direct_message(
                #             recipient_id=sender_id, text=notif).id
                #         self.delete_dm(sent)
                #     except Exception as ex:
                #         print(ex)
                #         sleep(30)
                #         pass
 
                #     continue

                # muted words
                list_muted = [i.lower() for i in administrator_data.Muted_words]
                if any(i in message.lower() for i in list_muted) and sender_id != administrator_data.Admin_id:
                    try:
                        print("deleting muted menfess")
                        notif = "Menfess kamu mengandung muted words, jangan lupa baca peraturan base yaa!"
                        sent = api.send_direct_message(
                            recipient_id=sender_id, text=notif).id
                        self.delete_dm(sent)
                    except Exception as ex:
                        sleep(60)
                        print(ex)
                        pass

                    continue

                # Message filter
                # Based on Twitter rules https://help.twitter.com/en/rules-and-policies/twitter-search-policies
                # Similiarity checker
                notif_temp = 0
                date_now = (datetime.now(timezone.utc) + timedelta(hours=administrator_data.Timezone)).day
                if date_now != self.day:
                    self.day = date_now
                    self.message_db = tuple()

                for i in self.message_db:
                    similiarity = SequenceMatcher(None, message, i).ratio()
                    if similiarity == 1:
                        print("Message similiarity is duplicate")
                        sent = api.send_direct_message(recipient_id=sender_id, text="Menfess kamu sama dengan menfess lain (hari ini). Coba gunakan pilihan kata yang lain!\nNote: Abaikan jika mendapat pesan ini setelah menfess terkirim.")
                        self.delete_dm(sent.id)
                        notif_temp = 1
                        break

                    elif similiarity > 0.9:
                        print("Message similiarity is more than 0.9")
                        sent = api.send_direct_message(recipient_id=sender_id, text="Menfess kamu mirip dengan menfess lain (hari ini). Coba gunakan pilihan kata yang lain!")
                        self.delete_dm(sent.id)
                        notif_temp = 1
                        break

                # primary keywords
                if any(j.lower() in message.lower() for j in administrator_data.Trigger_word):

                    if notif_temp == 0:
                        self.message_db += (message,)
                    else:
                        continue

                    print("Getting message -> sender_id: " + str(sender_id))
                    dict_dms = dict(message=message, sender_id=sender_id,
                             media_url=None, attachment_urls=(None, None))

                    # attachment_url (retweet)
                    urls = message_data['entities']['urls']
                    for i in urls:
                        if "https://twitter.com/" in i['expanded_url'] and "/status/" in i['expanded_url']:
                            if any(j in i['expanded_url'] for j in ['video', 'photo', 'media']) == False:
                                dict_dms['attachment_urls'] = (i['url'], i['expanded_url'])

                    # attachment
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
                            temp_bitrate.sort()
                            temp_bitrate.reverse()
                            media_url = temp_bitrate[0][1]

                        elif media_type == 'animated_gif':
                            media_url = media['video_info']['variants'][0]['url']
                        
                        dict_dms['media_url'] = media_url

                    dms.append(dict_dms)

                else:
                    try:
                        print("deleting message (keyword not in message)")
                        notif = "Keyword yang kamu kirim salah!"
                        sent = api.send_direct_message(recipient_id=sender_id, text=notif).id
                        self.delete_dm(sent)

                    except Exception as ex:
                        sleep(60)
                        print(ex)
                        pass

            # Notify the queue to sender
            print(str(len(dms)) + " collected")
            self.random_time = randrange(0,5)
            x = 0
            y = 0
            time = datetime.now(timezone.utc) + timedelta(hours=administrator_data.Timezone)
            for i in dms:
                y += 1
                x += (len(i['message']) // 272) + 1
                if i['media_url'] != None:
                    x += 0.2
                sent_time = time + timedelta(minutes=1, seconds= 3 + x*(25+self.random_time))
                hour = sent_time.hour
                minute = sent_time.minute
                if hour < 10:
                    hour = f"0{hour}"
                if minute < 10:
                    minute = f"0{minute}"
                sent_time = f"{str(hour)}:{str(minute)}"
                notif = f"Menfess kamu berada pada urutan ke-{str(y)}, akan terkirim sekitar pukul {sent_time}"
                sent = api.send_direct_message(recipient_id=i['sender_id'], text=notif)
                self.delete_dm(sent.id)

            sleep(60+self.random_time)
            return dms

        except Exception as ex:
            pass
            print(ex)
            sleep(60)
            return dms


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


    def get_user_screen_name(self, id):
        '''Get username
        :param id: account id -> int
        :returns: username -> str
        '''
        try:
            print("Getting username")
            user = self.api.get_user(id)
            return user.screen_name

        except Exception as ex:
            pass
            print(ex)
            user = "Exception"
            sleep(60)
            return user


    def download_media(self, media_url, filename=None):
        '''Download media from url, save the filename
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

            if exists(filename) == False:
                sleep(3)

            print("Download media successfully")
            return filename

        except Exception as ex:
            print(ex)
            pass


    def media_upload_chunk(self, filename, media_category='tweet'):
        '''Upload media with chunk
        :param filename: -> str
        :param media_category: 'tweet' or 'dm'
        :returns: media id -> str
        '''
        try:
            mediaupload = MediaUpload(filename, media_category)
            media_id = mediaupload.upload_init()
            mediaupload.upload_append()
            mediaupload.upload_finalize()
            return str(media_id)

        except Exception as ex:
            print(ex)
            pass


    def post_tweet(self, tweet, media_url=None, attachment_url=None):
        '''Post a tweet
        :param tweet: -> str
        :param attachment_url: url -> str
        :param media_url: media url that will be posted -> str
        :returns: tweet id -> str
        '''
        try:
            media_id = None
            if media_url != None:
                tweet = tweet.split()
                tweet = " ".join(tweet[:-1])
                filename = self.download_media(media_url)
                media_id = [self.media_upload_chunk(filename)]
                remove(filename)

            postid = 0
            while len(tweet) > 280:
                limit = 272
                check = tweet[:limit].split()
                separator = len(check[-1])
                if tweet[limit-1] == " ":
                    separator += 1
                tweet1 = unescape(tweet[:limit-separator]) + '-cont-'
                
                if postid == 0:
                    print("Making a thread...")
                    postid = self.api.update_status(
                        tweet1, attachment_url=attachment_url, media_ids=media_id).id
                    postid1 = postid
                else:
                    postid1 = self.api.update_status(
                        tweet1, in_reply_to_status_id=postid1, auto_populate_reply_metadata=True).id
                
                sleep(25+self.random_time)
                tweet = tweet[limit-separator:]
            
            if postid == 0:
                postid = self.api.update_status(
                        unescape(tweet), attachment_url=attachment_url, media_ids=media_id).id         
            else:
                self.api.update_status(
                    unescape(tweet), in_reply_to_status_id=postid1, auto_populate_reply_metadata=True).id
            
            sleep(25+self.random_time)
            return postid

        except Exception as ex:
            pass
            sleep(60)
            print(ex)
            return None