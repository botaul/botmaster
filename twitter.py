import tweepy
import constants
from time import sleep
import _json
import os
from os.path import exists
import requests
from requests_oauthlib import OAuth1
from async_upload import MediaUpload
import moviepy.editor as mp
from PIL import Image


class Twitter:
    def __init__(self):
        '''
        initialize tweepy
        objects from this:
            - api
            - follower
            - bot_id
        '''
        print("Initializing twitter...")
        self.auth = tweepy.OAuthHandler(
            constants.CONSUMER_KEY, constants.CONSUMER_SECRET)
        self.auth.set_access_token(
            constants.ACCESS_KEY, constants.ACCESS_SECRET)
        self.api = tweepy.API(
            self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        self.follower = list()
        self.bot_id = int()

    def read_dm(self):
        '''
        read and filter DMs
        filters:
            - check follower (exception for admin)
            - muted words (exception for admin)
            - set muted words from DM
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
                message_data = str(dm[x].message_create['message_data'])
                json_data = _json.encode_basestring(message_data)
                id = dm[x].id

                # check follower
                if int(sender_id) not in self.follower and sender_id != constants.Admin_id:
                    if sender_id == self.bot_id:
                        print("deleting bot messages")
                        self.delete_dm(id)

                    else:
                        try:
                            print("sender not in follower")
                            notif = "[BOT]\nHmm kayaknya kamu belum follow base ini. Follow dulu ya biar bisa ngirim menfess"
                            sent = api.send_direct_message(
                                recipient_id=sender_id, text=notif).id
                            self.delete_dm(id)
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
                        notif = "[BOT]\nMenfess kamu mengandung muted words, jangan lupa baca peraturan base yaa!"
                        sent = api.send_direct_message(
                            recipient_id=sender_id, text=notif).id
                        self.delete_dm(id)
                        self.delete_dm(sent)
                    except Exception as ex:
                        sleep(60)
                        print(ex)
                        pass

                    continue

                # set muted words from DM
                elif constants.Set_keyword in message:
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
                            command = constants.Dict_set_keyword[command]

                            for data in content:
                                try:
                                    command1 = command.format(f"\"{data}\"")
                                    notif = notif + f"\n{command1}"
                                    exec(command1)
                                except Exception as ex:
                                    notif = notif + f"\nexcept: {ex}"
                                    pass

                    except Exception as ex:
                        notif = "some commands failed" + \
                            f"\n{ex}" + f"\n{notif}"
                        print(ex)
                        pass

                    finally:
                        print(notif)
                        sent = api.send_direct_message(
                            recipient_id=sender_id, text=notif).id
                        self.delete_dm(id)
                        self.delete_dm(sent)

                    continue

                # primary keywords
                keywords = [constants.First_Keyword, constants.Second_Keyword,
                            constants.Third_keyword, constants.Set_keyword]
                if any(i in message for i in keywords):
                    print("Getting message -> by sender id " + str(sender_id))
                    # attachment
                    if 'attachment' not in json_data:
                        print("DM does not have any media..")
                        d = dict(message=message, sender_id=sender_id,
                                 id=dm[x].id, media=None)
                        urls = dm[x]._json['message_create']['message_data']['entities']['urls']
                        # attachment_url
                        if len(urls) != 0:
                            urls = dm[x]._json['message_create']['message_data']['entities']['urls'][0]['expanded_url']
                            d['urls'] = urls
                        dms.append(d)

                    else:
                        print("DM have an attachment")
                        media_type = dm[x].message_create['message_data']['attachment']['media']['type']
                        # photo
                        if media_type == 'photo':
                            attachment = dm[x].message_create['message_data']['attachment']
                            photo_url = attachment['media']['media_url']
                            d = dict(message=message, sender_id=sender_id,
                                     id=dm[x].id, media=photo_url, type=media_type)
                            dms.append(d)
                        # video
                        elif media_type == 'video':
                            media = dm[x].message_create['message_data']['attachment']['media']
                            temp_bitrate = list()
                            media_url = media['video_info']['variants']
                            for varian in media_url:
                                if varian['content_type'] == "video/mp4":
                                    temp_bitrate.append(
                                        (varian['bitrate'], varian['url']))
                            temp_bitrate.sort()
                            temp_bitrate.reverse()
                            video_url = temp_bitrate[0][1]
                            d = dict(message=message, sender_id=sender_id,
                                     id=dm[x].id, media=video_url, type=media_type)
                            dms.append(d)
                        # animation_gif
                        elif media_type == 'animated_gif':
                            media = dm[x].message_create['message_data']['attachment']['media']
                            media_url = media['video_info']['variants'][0]
                            video_url = media_url['url']
                            d = dict(message=message, sender_id=sender_id,
                                     id=dm[x].id, media=video_url, type=media_type)
                            dms.append(d)

                else:
                    try:
                        print("deleting message (keyword not in message)")
                        notif = "[BOT]\nKeyword yang kamu kirim salah!"
                        sent = api.send_direct_message(
                            recipient_id=sender_id, text=notif).id
                        self.delete_dm(id)
                        self.delete_dm(sent)

                    except Exception as ex:
                        sleep(60)
                        print(ex)
                        pass

            print(str(len(dms)) + " collected")
            if len(dms) > 1:
                dms.reverse()

            sleep(60)
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

    def ASK(self, message, screen_name):
        '''
        Send DMs to admin
        message: message -> str
        screen_name: sender username -> str
        return message id -> str
        '''
        print("ASKING")
        try:
            message = message + " @" + screen_name
            sent = self.api.send_direct_message(
                recipient_id=constants.Admin_id, text=message).id
            return sent

        except Exception as ex:
            print(ex)
            sleep(60)
            pass

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
            right = 272
            leftcheck = 260
            check = tweet[leftcheck:right].split()
            separator = len(check[-1])
            tweet1 = tweet[left:right-separator] + '(cont..)'
            if file_type == 'photo' or file_type == 'animated_gif':
                complete = self.api.update_with_media(
                    filename=name, status=tweet1).id
            elif file_type == 'video':
                media_id = self.media_upload_chunk(name)
                media_ids = list()
                media_ids.append(media_id)
                complete = self.api.update_status(
                    tweet1, media_ids=media_ids).id
            elif file_type == 'normal':
                complete = self.api.update_status(tweet1, attachment_url=attachment_url).id
            elif file_type == "retweet":
                complete = self.api.update_status(
                    tweet1, media_ids=media_ids).id

            postid = str(complete)
            sleep(20)
            tweet2 = tweet[right-separator:len(tweet)]
            while len(tweet2) > 280:
                leftcheck += 272
                left += 272
                right += 272
                check = tweet[leftcheck:right].split()
                separator = len(check[-1])
                tweet2 = tweet[left:right-separator] + '(cont..)'
                complete = self.api.update_status(
                    tweet2, in_reply_to_status_id=complete, auto_populate_reply_metadata=True).id
                sleep(20)
                tweet2 = tweet[right-separator:len(tweet)]
            self.api.update_status(
                tweet2, in_reply_to_status_id=complete, auto_populate_reply_metadata=True)
            sleep(20)
            return postid
        except Exception as ex:
            pass
            print(ex)
            sleep(30)
            return None

    def post_tweet_quote(self, name):
        '''
        tweet a quote image (ready.png)
        name: username -> string
        return tweet id -> str
        '''
        print("Uploading..")
        try:
            if name is None:
                tweet = constants.Second_Keyword
            elif name != None:
                tweet = f"{constants.Second_Keyword} by @{name}"
            postid = self.api.update_with_media(
                filename="ready.png", status=tweet).id
            os.remove('ready.png')
            sleep(20)
            return str(postid)
        except Exception as ex:
            pass
            print(ex)
            sleep(60)
            return None

    def post_tweet(self, tweet, attachment_url=None):
        '''
        tweet a normal tweet
        tweet: -> str
        attachment_url: url -> str
        return tweet id -> str
        '''
        try:
            if len(tweet) <= 280:
                postid = self.api.update_status(tweet, attachment_url=attachment_url).id
            elif len(tweet) > 280:
                postid = self.Thread(None, "normal", tweet, None, attachment_url=attachment_url)
            sleep(20)
            return postid
        except Exception as ex:
            pass
            sleep(60)
            print(ex)
            return None

    def post_multiple_media(self, tweet, urls):
        '''
        get media from tweet's link and tweet
        tweet: -> str
        urls: -> str
        return tweet id -> str
        '''
        try:
            print("posting multiple media")
            url = urls.replace('/', ' ')
            url = url.replace('?', ' ')
            url = url.split()
            status = self.api.get_status(url[-2])

            if "extended_entities" in status._json:
                media_urls = list()
                filenames = list()
                for media in status._json['extended_entities']['media']:
                    if "video_info" not in media:
                        photo_url = media['media_url']
                        media_urls.append(photo_url)
                        filename = photo_url.replace("/", " ")
                        filename = photo_url.replace("?", " ")
                        filename = filename.split()
                        filename1 = filename[-1]
                        if "?" in photo_url:
                            filename1 = filename[-2]
                        filenames.append(filename1)
                    else:
                        media_url = status._json['extended_entities']['media'][0]['video_info']['variants']
                        temp_bitrate = list()
                        for varian in media_url:
                            if varian['content_type'] == "video/mp4":
                                temp_bitrate.append(
                                    (varian['bitrate'], varian['url']))
                        temp_bitrate.sort()
                        temp_bitrate.reverse()
                        video_url = temp_bitrate[0][1]
                        media_urls.append(video_url)
                        filename = video_url.replace('/', ' ')
                        filename = filename.replace('?', ' ')
                        filename = filename.split()
                        filename1 = filename[-1]
                        if "?" in video_url:
                            filename1 = filename[-2]
                        filenames.append(filename1)

                media_ids = list()
                for i in range(len(media_urls)):
                    self.download_media(media_urls[i], filenames[i])
                    media_id = self.media_upload_chunk(filenames[i])
                    media_ids.append(media_id)
                    os.remove(filenames[i])

                if len(tweet) <= 280:
                    postid = self.api.update_status(
                        tweet, media_ids=media_ids).id
                    sleep(20)
                else:
                    postid = self.Thread(
                        None, 'retweet', tweet, media_ids=media_ids)
                return postid
            else:
                return "not_available"

        except Exception as ex:
            pass
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

            r = requests.get(media_url, auth=oauth)

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

            sleep(3)
            while exists(filename) == False:
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

    def post_tweet_with_media(self, tweet, media_url, file_type):
        '''
        tweet a tweet with media
        tweet: -> str
        media_url: url -> str
        file_type: ('photo', 'video', or 'animated_gif') -> str
        return tweet id -> str
        '''
        try:
            tweet = tweet.split()
            tweet = " ".join(tweet[:len(tweet)-1])

            if file_type == 'photo':
                try:
                    filename = media_url.replace('/', ' ')
                    filename = filename.split()
                    filename = filename[-1]
                    self.download_media(media_url, filename)
                    size = os.path.getsize(filename)
                    print("Photo size: " + str(size))
                    while size > 3000000:
                        foo = Image.open(filename)
                        dimension = "{} {}".format(*foo).split(' ')
                        first = str(round(int(dimension[0])*0.8))
                        second = str(round(int(dimension[1])*0.8))
                        foo = foo.resize((first, second), Image.ANTIALIAS)
                        foo.save(filename, optimize=True, quality=95)
                        sleep(3)
                        while exists(filename) == False:
                            sleep(3)
                    if len(tweet) <= 280:
                        postid = self.api.update_with_media(
                            filename=filename, status=tweet).id
                    elif len(tweet) > 280:
                        postid = self.Thread(filename, file_type, tweet)
                    os.remove(filename)
                    return postid

                except Exception as ex:
                    pass
                    print(ex)
                    sleep(30)
                    return None

            elif file_type == 'animated_gif':
                try:
                    filename = media_url.replace('/', ' ')
                    filename = filename.split()
                    filename = filename[-1]
                    self.download_media(media_url, filename)
                    clip = mp.VideoFileClip(filename)
                    clip.subclip((0), (0, 2)).resize(0.2).without_audio()
                    clip.write_gif(f'{filename}.gif', fps=12, program='ffmpeg')
                    clip.close()

                    sleep(3)
                    while exists(f'{filename}.gif') == False:
                        sleep(3)

                    print("gif size: " +
                          str(os.path.getsize(f'{filename}.gif')))
                    if len(tweet) <= 280:
                        postid = self.api.update_with_media(
                            filename=f'{filename}.gif', status=tweet).id
                    elif len(tweet) > 280:
                        postid = self.Thread(
                            f"{filename}.gif", file_type, tweet)
                    os.remove(filename)
                    os.remove(f'{filename}.gif')
                    return postid
                except Exception as ex:
                    pass
                    print(ex)
                    sleep(30)
                    return None

            elif file_type == 'video':
                filename = media_url.replace('/', ' ')
                filename = filename.replace('?', ' ')
                filename = filename.split()
                filename = filename[-2]
                self.download_media(media_url, filename)
                if len(tweet) <= 280:
                    media_id = self.media_upload_chunk(filename)
                    media_ids = list()
                    media_ids.append(media_id)
                    postid = self.api.update_status(
                        tweet, media_ids=media_ids).id
                elif len(tweet) > 280:
                    postid = self.Thread(filename, file_type, tweet)
                os.remove(filename)
                return postid

            print("Upload with media success!")
        except Exception as ex:
            pass
            sleep(60)
            print(ex)
            return None
