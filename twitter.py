from tweepy import OAuthHandler, API
import constants
from time import sleep
from os import remove
from os.path import exists
from requests import get
from requests_oauthlib import OAuth1
from async_upload import MediaUpload
from html import unescape
from datetime import datetime, timezone, timedelta
from random import randrange


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
            constants.CONSUMER_KEY, constants.CONSUMER_SECRET)
        self.auth.set_access_token(
            constants.ACCESS_KEY, constants.ACCESS_SECRET)
        self.api = API(
            self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        self.follower = list()
        self.bot_id = int()

    def read_dm(self):
        '''
        read and filter DMs
        filters:
            - set from DM
            - check follower (exception for admin)
            - muted words (exception for admin)
            - primary keywords
                - attachment
                    - attachment_url
                    - photo
                    - video
                    - animated_gif
        return list of filtered DMs
        '''
        print("Get direct messages...")
        dms = list()
        try:
            api = self.api
            dm = api.list_direct_messages()
            for x in range(len(dm)):
                sender_id = dm[x].message_create['sender_id']
                message = dm[x].message_create['message_data']['text']
                message_data = dm[x].message_create['message_data']
                id = dm[x].id

                self.delete_dm(id)

                # set from DM
                if constants.Set_keyword in message:
                    print("command in progress...")
                    try:
                        message = message.split()
                        command, *content = message[1:]

                        if type(content) == list:
                            pass
                        else:
                            content = content.split()

                        notif = "commands:"
                        if command in constants.Dict_set_keyword.keys():
                            command1 = constants.Dict_set_keyword[command]
                            if len(content) != 0:
                                for data in content:
                                    try:
                                        command1 = command1.format(f"\"{data}\"")
                                        notif += f"\nprocessing {command} {data}"
                                        exec(command1)
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

                # check follower
                elif int(sender_id) not in self.follower and sender_id != constants.Admin_id:
                    print("sender not in follower")
                    try:
                        notif = "Hmm kayaknya kamu belum follow base ini. Follow dulu ya biar bisa ngirim menfess"
                        sent = api.send_direct_message(
                            recipient_id=sender_id, text=notif).id
                        self.delete_dm(sent)
                    except Exception as ex:
                        print(ex)
                        sleep(30)
                        pass

                    continue

                # muted words
                elif any(i in message for i in constants.Muted_words) and sender_id != constants.Admin_id:
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

                # primary keywords
                keywords = [constants.First_Keyword]
                # keywords = [constants.First_Keyword, constants.Second_Keyword,
                #             constants.Third_keyword]
                if any(i in message for i in keywords):
                    print("Getting message -> by sender id " + str(sender_id))
                    # attachment_url (retweet)
                    url = None
                    urls = message_data['entities']['urls']
                    if len(urls) != 0:
                        for i in urls:
                            if "https://twitter.com/" in i['expanded_url']:
                                if "video" not in i['expanded_url']:
                                    if "photo" not in i['expanded_url']:
                                        if "media" not in i['expanded_url']:
                                            url = (i['url'], i['expanded_url'])
                    # attachment
                    if 'attachment' not in message_data:
                        print("DM does not have any media..")
                        d = dict(message=message, sender_id=sender_id,
                                 id=id, media=None, url=url)
                        dms.append(d)

                    else:
                        print("DM have an attachment")
                        media = message_data['attachment']['media']
                        media_type = media['type']
                        # photo
                        if media_type == 'photo':
                            photo_url = media['media_url']
                            d = dict(message=message, sender_id=sender_id,
                                     id=dm[x].id, media=photo_url, type=media_type, url=url)
                            dms.append(d)
                        # video
                        elif media_type == 'video':
                            media_url = media['video_info']['variants']
                            temp_bitrate = list()
                            for varian in media_url:
                                if varian['content_type'] == "video/mp4":
                                    temp_bitrate.append(
                                        (varian['bitrate'], varian['url']))
                            temp_bitrate.sort()
                            temp_bitrate.reverse()
                            video_url = temp_bitrate[0][1]
                            d = dict(message=message, sender_id=sender_id,
                                     id=dm[x].id, media=video_url, type=media_type, url=url)
                            dms.append(d)
                        # animation_gif
                        elif media_type == 'animated_gif':
                            media_url = media['video_info']['variants'][0]
                            video_url = media_url['url']
                            d = dict(message=message, sender_id=sender_id,
                                     id=dm[x].id, media=video_url, type=media_type, url=url)
                            dms.append(d)

                else:
                    try:
                        print("deleting message (keyword not in message)")
                        notif = "Keyword yang kamu kirim salah!"
                        sent = api.send_direct_message(
                            recipient_id=sender_id, text=notif).id
                        self.delete_dm(sent)

                    except Exception as ex:
                        sleep(60)
                        print(ex)
                        pass

            print(str(len(dms)) + " collected")
            if len(dms) > 1:
                dms.reverse()
            
            x = 0
            time = datetime.now(timezone.utc) + timedelta(hours=constants.Timezone)
            for i in dms:
                x += (len(i['message']) // 270) + 1
                if i['media'] != None:
                    x += 0.2
                sent_time = time + timedelta(minutes=1, seconds= x*26)
                hour = sent_time.hour
                minute = sent_time.minute
                if hour < 10:
                    hour = f"0{hour}"
                if minute < 10:
                    minute = f"0{minute}"
                sent_time = f"{str(hour)}:{str(minute)}"
                notif = f"Menfess kamu akan terkirim sekitar pukul {sent_time}"
                sent = api.send_direct_message(recipient_id=i['sender_id'], text=notif)
                self.delete_dm(sent.id)

            sleep(60+randrange(0,10))
            return dms

        except Exception as ex:
            pass
            print(ex)
            sleep(60)
            return dms

    def delete_dm(self, id):
        '''
        delete a DM
        id: message id -> int or str
        '''
        print("Deleting dm with id = " + str(id))
        try:
            self.api.destroy_direct_message(id)
        except Exception as ex:
            print(ex)
            sleep(60)
            pass

    # def ASK(self, message, screen_name):
    #     '''
    #     Send DMs to admin
    #     message: message -> str
    #     screen_name: sender username -> str
    #     return message id -> str
    #     '''
    #     print("ASKING")
    #     try:
    #         message = message + " @" + screen_name
    #         sent = self.api.send_direct_message(
    #             recipient_id=constants.Admin_id, text=message).id
    #         return sent

    #     except Exception as ex:
    #         print(ex)
    #         sleep(60)
    #         pass

    def get_user_screen_name(self, id):
        '''
        get username
        id: account id -> int
        return username -> str
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

    def Thread(self, name, file_type, tweet, media_ids=None, attachment_url=None):
        '''
        tweet a thread
        name: filename of the file -> str
        file_type: ('photo', 'video', 'animated_gif', 'normal' or 'retweet') -> str
        tweet: -> str
        media_ids: media id -> list
        attachment_url: url -> str
        return tweet id -> str
        '''
        print("Tweeting a Thread")
        try:
            left = 0
            right = 270
            leftcheck = 240
            check = tweet[leftcheck:right].split()
            separator = len(check[-1])
            tweet1 = unescape(tweet[left:right-separator]) + '(cont..)'

            if file_type == 'photo' or file_type == 'animated_gif' or file_type == 'video':
                media_id = self.media_upload_chunk(name)
                media_ids = list()
                media_ids.append(media_id)
                complete = self.api.update_status(
                    tweet1, media_ids=media_ids, attachment_url=attachment_url).id
            elif file_type == 'normal':
                complete = self.api.update_status(
                    tweet1, attachment_url=attachment_url).id
            elif file_type == "retweet":
                complete = self.api.update_status(
                    tweet1, media_ids=media_ids, attachment_url=attachment_url).id

            sleep(25+randrange(0,10))
            postid = str(complete)
            tweet2 = tweet[right-separator:]
            while len(tweet2) > 280:
                leftcheck += 270 - separator
                left += 270 - separator
                right += 270 - separator
                check = tweet[leftcheck:right].split()
                separator = len(check[-1])
                tweet2 = unescape(
                    tweet[left:right-separator]) + '(cont..)'
                complete = self.api.update_status(
                    tweet2, in_reply_to_status_id=complete, auto_populate_reply_metadata=True).id
                sleep(25+randrange(0,10))
                tweet2 = tweet[right-separator:]

            tweet2 = unescape(tweet2)
            self.api.update_status(
                tweet2, in_reply_to_status_id=complete, auto_populate_reply_metadata=True)
            sleep(25+randrange(0,10))
            return postid
        except Exception as ex:
            pass
            print(ex)
            sleep(30)
            return None

    # def post_tweet_quote(self, name):
    #     '''
    #     tweet a quote image (ready.png)
    #     name: username -> string
    #     return tweet id -> str
    #     '''
    #     print("Uploading..")
    #     try:
    #         if name is None:
    #             tweet = constants.Second_Keyword
    #         elif name != None:
    #             tweet = f"{constants.Second_Keyword} by @{name}"
    #         postid = self.api.update_with_media(
    #             filename="ready.png", status=tweet).id
    #         remove('ready.png')
    #         sleep(25+randrange(0,10))
    #         return str(postid)
    #     except Exception as ex:
    #         pass
    #         print(ex)
    #         sleep(60)
    #         return None

    def post_tweet(self, tweet, attachment_url=None):
        '''
        tweet a normal tweet
        tweet: -> str
        attachment_url: url -> str
        return tweet id -> str
        '''
        try:
            max_char = len(tweet)
            if max_char <= 280:
                postid = self.api.update_status(
                    unescape(tweet), attachment_url=attachment_url).id
                sleep(25+randrange(0,10))
            elif max_char > 280:
                postid = self.Thread(None, "normal", tweet,
                                     None, attachment_url)
            return postid
        except Exception as ex:
            pass
            sleep(60)
            print(ex)
            return None

    def download_media(self, media_url, filename=None):
        '''
        download media from url save the filename
        media_url: url -> string
        filename: None (default) or filename --> str
        return file name (when filename=None) -> str
        '''
        try:
            print("Downloading media...")
            oauth = OAuth1(client_key=constants.CONSUMER_KEY,
                           client_secret=constants.CONSUMER_SECRET,
                           resource_owner_key=constants.ACCESS_KEY,
                           resource_owner_secret=constants.ACCESS_SECRET)

            r = get(media_url, auth=oauth)

            if filename == None:
                filename = media_url.replace('/', ' ')
                filename = filename.replace('?', ' ')
                filename = filename.split()
                filename1 = filename[-1]
                if "?" in media_url:
                    filename1 = filename[-2]
                filename = str(filename1)

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

    def media_upload_chunk(self, filename, media_category=True):
        '''
        upload media with chunk
        filename: -> str
        media_category: True for tweet, False for DM
        return media id -> str
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

    def post_tweet_with_media(self, tweet, media_url, file_type, attachment_url=None):
        '''
        tweet a tweet with media
        tweet: -> str
        media_url: url -> str
        file_type: ('photo', 'video', or 'animated_gif') -> str
        return tweet id -> str
        '''
        try:
            tweet = tweet.split()
            tweet = " ".join(tweet[:-1])
            max_char = len(tweet)

            if file_type == 'photo':
                try:
                    filename = self.download_media(media_url)
                    if max_char <= 280:
                        media_id = self.media_upload_chunk(filename)
                        media_ids = list()
                        media_ids.append(media_id)
                        postid = self.api.update_status(
                            unescape(tweet), media_ids=media_ids, attachment_url=attachment_url).id
                        sleep(25+randrange(0,10))
                    elif max_char > 280:
                        postid = self.Thread(
                            filename, file_type, tweet, None, attachment_url)
                    remove(filename)
                    return postid

                except Exception as ex:
                    pass
                    print(ex)
                    sleep(30)
                    return None

            elif file_type == 'video' or file_type == 'animated_gif':
                filename = self.download_media(media_url)
                if max_char <= 280:
                    media_id = self.media_upload_chunk(filename)
                    media_ids = list()
                    media_ids.append(media_id)
                    postid = self.api.update_status(
                        unescape(tweet), media_ids=media_ids, attachment_url=attachment_url).id
                    sleep(25+randrange(0,10))
                elif max_char > 280:
                    file_type = 'video'
                    postid = self.Thread(
                        filename, file_type, tweet, None, attachment_url)
                remove(filename)
                return postid

            print("Upload with media success!")
        except Exception as ex:
            pass
            sleep(60)
            print(ex)
            return None
