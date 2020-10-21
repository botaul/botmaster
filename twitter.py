import tweepy
import constants
import time
import _json
from requests_oauthlib import OAuth1
import os
from os.path import exists
import requests
from async_upload import VideoTweet
import moviepy.editor as mp
from PIL import Image


class Twitter:
    def __init__(self):
        print("Initializing twitter...")
        self.auth = tweepy.OAuthHandler(
            constants.CONSUMER_KEY, constants.CONSUMER_SECRET)
        self.auth.set_access_token(
            constants.ACCESS_KEY, constants.ACCESS_SECRET)
        self.api = tweepy.API(
            self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        self.follower = list()
        self.bot_id = None

    def read_dm(self):
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
                if str(sender_id) not in self.follower and str(sender_id) != str(constants.Admin_id):
                    if str(sender_id) == str(self.bot_id):
                        print("deleting bot messages")
                        self.delete_dm(id)

                    else:
                        try:
                            print("sender not in follower")
                            notif = "[BOT]\nHmm kayaknya kamu belum follow base ini. Follow dulu ya biar bisa ngirim menfess"
                            sent = api.send_direct_message(
                                recipient_id=sender_id, text=notif)
                            self.delete_dm(id)
                            self.delete_dm(sent.id)
                        except Exception as ex:
                            print(ex)
                            time.sleep(30)
                            pass

                    continue

                # muted words
                elif any(i in message for i in constants.Muted_words) and str(sender_id) != str(constants.Admin_id):
                    try:
                        print("deleting muted menfess")
                        notif = "[BOT]\nMenfess kamu mengandung muted words, jangan lupa baca peraturan base yaa!"
                        sent = api.send_direct_message(
                            recipient_id=sender_id, text=notif)
                        self.delete_dm(id)
                        self.delete_dm(sent.id)
                    except Exception as ex:
                        time.sleep(60)
                        print(ex)
                        pass

                    continue

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
                        notif = "some commands failed" + f"\n{ex}" + f"\n{notif}"
                        print(ex)
                        pass

                    finally:
                        print(notif)
                        sent = api.send_direct_message(
                            recipient_id=sender_id, text=notif)
                        self.delete_dm(id)
                        self.delete_dm(sent.id)
                        
                    continue

                keywords = [constants.First_Keyword, constants.Second_Keyword,
                            constants.Third_keyword, constants.Set_keyword]
                if any(i in message for i in keywords):
                    print("Getting message -> by sender id " + str(sender_id))
                    if 'attachment' not in json_data:
                        print("DM does not have any media..")
                        d = dict(message=message, sender_id=sender_id,
                                 id=dm[x].id, media=None)
                        dms.append(d)

                    else:
                        print("DM have an attachment")
                        media_type = dm[x].message_create['message_data']['attachment']['media']['type']
                        if media_type == 'photo':
                            attachment = dm[x].message_create['message_data']['attachment']
                            photo_url = attachment['media']['media_url']
                            d = dict(message=message, sender_id=sender_id,
                                     id=dm[x].id, media=photo_url, type=media_type)
                            dms.append(d)

                        elif media_type == 'video':
                            media = dm[x].message_create['message_data']['attachment']['media']
                            temp_bitrate = list()
                            media_url = media['video_info']['variants']
                            for varian in media_url:
                                if varian['content_type'] == "video/mp4":
                                    temp_bitrate.append((varian['bitrate'], varian['url']))
                            temp_bitrate.sort()
                            temp_bitrate.reverse()
                            video_url = temp_bitrate[0][1]
                            temp_bitrate.clear()
                            d = dict(message=message, sender_id=sender_id,
                                     id=dm[x].id, media=video_url, type=media_type)
                            dms.append(d)

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
                            recipient_id=sender_id, text=notif)
                        self.delete_dm(id)
                        self.delete_dm(sent.id)

                    except Exception as ex:
                        time.sleep(60)
                        print(ex)
                        pass

            print(str(len(dms)) + " collected")
            if len(dms) > 1:
                dms.reverse()

            time.sleep(60)
            return dms

        except Exception as ex:
            print(ex)
            time.sleep(60)
            return dms
            pass

    def delete_dm(self, id):
        print("Deleting dm with id = " + str(id))
        try:
            self.api.destroy_direct_message(id)
        except Exception as ex:
            print(ex)
            time.sleep(60)
            pass

    def ASK(self, message, screen_name):
        print("ASKING")
        try:
            message = message + " @" + screen_name
            sent = self.api.send_direct_message(
                recipient_id=constants.Admin_id, text=message)
            return sent

        except Exception as ex:
            print(ex)
            time.sleep(60)
            pass

    def get_user_screen_name(self, id):
        try:
            print("Getting username")
            user = self.api.get_user(id)
            return user.screen_name

        except Exception as ex:
            print(ex)
            user = "Exception"
            time.sleep(60)
            return user
            pass

    def Thread(self, name, type, tweet):
        try:
            left = 0
            right = 272
            leftcheck = 260
            check = tweet[leftcheck:right].split(' ')
            separator = len(check[-1])
            tweet1 = tweet[left:right-separator] + '(cont..)'
            if type == 'photo' or type == 'animated_gif':
                complete = self.api.update_with_media(
                    filename=name, status=tweet1).id
                postid = int(complete)
            elif type == 'video':
                videoTweet = VideoTweet(name)
                videoTweet.upload_init()
                videoTweet.upload_append()
                videoTweet.upload_finalize()
                complete = videoTweet.Tweet(tweet1)
                postid = int(complete)
            elif type == 'normal':
                complete = self.api.update_status(tweet1).id
                postid = int(complete)
            time.sleep(20)
            tweet2 = tweet[right-separator:len(tweet)]
            while len(tweet2) > 280:
                leftcheck += 272
                left += 272
                right += 272
                check = tweet[leftcheck:right]
                separator = len(check[-1])
                tweet2 = tweet[left:right-separator] + '(cont..)'
                complete = self.api.update_status(
                    tweet2, in_reply_to_status_id=complete, auto_populate_reply_metadata=True).id
                time.sleep(20)
                tweet2 = tweet[right-separator:len(tweet)]
            self.api.update_status(
                tweet2, in_reply_to_status_id=complete, auto_populate_reply_metadata=True)
            time.sleep(20)
            return postid
        except Exception as ex:
            print(ex)
            time.sleep(30)
            pass

    def post_tweet_quote(self, name):
        print("Uploading..")
        try:
            if name is None:
                tweet = constants.Second_Keyword
            elif name != None:
                tweet = f"{constants.Second_Keyword} by @{name}"
            postid = self.api.update_with_media(
                filename="ready.png", status=tweet).id
            os.remove('ready.png')
            time.sleep(20)
            return postid
        except Exception as ex:
            print(ex)
            time.sleep(60)
            pass

    def post_tweet(self, tweet):
        try:
            if len(tweet) <= 280:
                postid = self.api.update_status(tweet).id
            elif len(tweet) > 280:
                type = "normal"
                postid = self.Thread(None, type, tweet)
            time.sleep(20)
            return postid
        except Exception as ex:
            time.sleep(60)
            print(ex)
            pass

    def download_media(self, media_url, filename):
        '''
        media_url   : url -> string
        filename    : filename with exstension -> string
        '''

        try:
            print("Downloading media...")
            #arr = str(media_url).split('/')
            oauth = OAuth1(client_key=constants.CONSUMER_KEY,
                           client_secret=constants.CONSUMER_SECRET,
                           resource_owner_key=constants.ACCESS_KEY,
                           resource_owner_secret=constants.ACCESS_SECRET)

            r = requests.get(media_url, auth=oauth)
            with open(filename, 'wb') as f:
                f.write(r.content)
                f.close()

            time.sleep(3)
            while exists(filename) == False:
                time.sleep(3)

            print("Download media successfully")

        except Exception as ex:
            print(ex)
            pass

    def post_tweet_with_media(self, tweet, media_url, type):
        try:

            if type == 'photo':
                self.download_media(media_url, 'photo.jpg')

            elif type == 'video':
                self.download_media(media_url, 'video.mp4')

            elif type == 'animated_gif':
                self.download_media(media_url, 'animated_gif.mp4')

            tweet = tweet.split()
            tweet = " ".join(tweet[:len(tweet)-1])

            if type == 'photo':
                try:
                    size = os.path.getsize('photo.jpg')
                    print("Photo size: " + str(size))
                    while size > 3000000:
                        foo = Image.open('photo.jpg')
                        dimension = "{} {}".format(*foo).split(' ')
                        first = str(round(int(dimension[0])*0.8))
                        second = str(round(int(dimension[1])*0.8))
                        foo = foo.resize((first, second), Image.ANTIALIAS)
                        foo.save('photo.jpg', optimize=True, quality=95)
                        time.sleep(3)
                        while exists('photo.jpg') == False:
                            time.sleep(3)
                        size = os.path.getsize('photo.jpg')
                    if len(tweet) <= 280:
                        postid = self.api.update_with_media(
                            filename='photo.jpg', status=tweet).id
                    elif len(tweet) > 280:
                        name = "photo.jpg"
                        postid = self.Thread(name, type, tweet)
                    os.remove('photo.jpg')
                    return postid

                except Exception as ex:
                    print(ex)
                    time.sleep(30)
                    pass

            elif type == 'animated_gif':
                try:
                    clip = mp.VideoFileClip('animated_gif.mp4')
                    clip.subclip((0), (0, 2)).resize(0.2).without_audio()
                    clip.write_gif('animated.gif', fps=12, program='ffmpeg')
                    clip.close()

                    time.sleep(3)
                    while exists('animated.gif') == False:
                        time.sleep(3)

                    print("gif size: " + str(os.path.getsize('animated.gif')))
                    if len(tweet) <= 280:
                        postid = self.api.update_with_media(
                            filename='animated.gif', status=tweet).id
                    elif len(tweet) > 280:
                        name = "animated.gif"
                        postid = self.Thread(name, type, tweet)
                    os.remove('animated_gif.mp4')
                    os.remove('animated.gif')
                    return postid
                except Exception as ex:
                    print(ex)
                    time.sleep(30)
                    pass

            elif type == 'video':
                try:
                    clip = mp.VideoFileClip("video.mp4")
                    width = clip.w
                    height = clip.h
                    if height > width:
                        clip_resized = clip.resize(width=720)
                        clip_resized.write_videofile("output.mp4", fps=20)
                    elif height < width:
                        clip_resized = clip.resize(height=720)
                        clip_resized.write_videofile("output.mp4", fps=20)
                    elif height == width:
                        clip_resized = clip.resize(height=720, width=720)
                        clip_resized.write_videofile("output.mp4", fps=20)

                    clip_resized.close()
                    time.sleep(3)
                    while exists('output.mp4') == False:
                        time.sleep(3)

                    if len(tweet) <= 280:
                        videoTweet = VideoTweet('output.mp4')
                        videoTweet.upload_init()
                        videoTweet.upload_append()
                        videoTweet.upload_finalize()
                        postid = videoTweet.Tweet(tweet)
                    elif len(tweet) > 280:
                        name = 'output.mp4'
                        postid = self.Thread(name, type, tweet)

                    os.remove('video.mp4')
                    os.remove('output.mp4')
                    return postid

                except ValueError as va:
                    print(va)
                    print("Exception Happen")
                    pass
            print("Upload with media success!")
        except Exception as ex:
            time.sleep(60)
            print(ex)
            pass
