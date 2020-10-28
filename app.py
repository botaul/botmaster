from twitter import Twitter
# from media import Media
from time import sleep
from threading import Thread
from github import Github
from datetime import datetime
import constants
from os.path import exists
from os import remove

tw = Twitter()
# media = Media()
github = Github(constants.Github_token)


def start():
    print("Starting program...")
    dms = list()
    api = tw.api
    me = api.me()
    tw.bot_id = me.id
    open('follower_data.txt', 'w').truncate()
    first = open('follower_data.txt').read()
    # sent = api.send_direct_message(recipient_id=constants.Admin_id, text="Twitter autobase is starting...!").id
    # tw.delete_dm(sent)

    while True:
        print("Updating followers...")
        follower = api.followers_ids(user_id=me.id)
        if len(follower) != 0:
            tw.follower = follower

            if len(first) <= 3:
                str_follower = [str(i) for i in follower]
                data = " ".join(str_follower)
                open("follower_data.txt", "w").write(data)
                first = "checked"
                del str_follower

            data = open('follower_data.txt').read()
            data = data.split()
            data1 = str()
            data2 = data.copy()

            for i in follower:
                if str(i) not in data:
                    data1 += " " + str(i)
                    notif = "[BOT]\nYEAY! Sekarang kamu bisa mengirim menfess, jangan lupa baca peraturan base yaa!"
                    sent = api.send_direct_message(
                        recipient_id=i, text=notif).id
                    tw.delete_dm(sent)

            for i in data2:
                if int(i) not in follower:
                    data.remove(i)

            if data != data2:
                data = " ".join(data)
                data = data + data1
                new = open("follower_data.txt", "w")
                new.write(data)
                new.close()
            elif data == data2 and len(data1) != 0:
                new = open("follower_data.txt", "a")
                new.write(data1)
                new.close()

            del data
            del data1
            del data2

        else:
            print("error when get follower from API")
            pass

        if len(dms) != 0:
            for i in range(len(dms)):
                try:
                    message = dms[i]['message']
                    sender_id = dms[i]['sender_id']
                    id = dms[i]['id']
                    screen_name = tw.get_user_screen_name(sender_id)
                    open(filename_github, 'a').write(
                        "\n\"" + message + "\" " + screen_name + " " + sender_id)
                    print("Heroku Database saved")

                    notif = f"Yeay, Menfess kamu telah terkirim! https://twitter.com/{me.screen_name}/status/"
                    if constants.First_Keyword in message:
                        if dms[i]['media'] is None:
                            print("DM will be posted")
                            if 'urls' not in dms[i]:
                                postid = tw.post_tweet(message)
                            else:
                                message = message.split()
                                message = " ".join(message[:-1])
                                if constants.Sub1_keyword in message:
                                    message = message.replace(constants.Sub1_keyword, "")
                                    postid = tw.post_multiple_media(
                                        message, dms[i]['urls'])
                                else:
                                    postid = tw.post_tweet(
                                        message, attachment_url=dms[i]['urls'])

                            if postid == "not_available":
                                message = message.split()
                                message = " ".join(message[:-1])
                                postid = tw.post_tweet(
                                    message, attachment_url=dms[i]['urls'])
                                text = notif + str(postid)
                                sent = api.send_direct_message(
                                    recipient_id=sender_id, text=text).id
                            elif postid != None:
                                text = notif + str(postid)
                                sent = api.send_direct_message(
                                    recipient_id=sender_id, text=text).id
                            else:
                                sent = api.send_direct_message(
                                    recipient_id=sender_id, text="[BOT]\nMaaf ada kesalahan pada sistem :(\ntolong screenshot & laporkan kepada admin").id
                            tw.delete_dm(id)
                            tw.delete_dm(sent)
                        else:
                            print("DM will be posted with media.")
                            postid = tw.post_tweet_with_media(
                                message, dms[i]['media'], dms[i]['type'])
                            if postid != None:
                                text = notif + str(postid)
                                sent = api.send_direct_message(
                                    recipient_id=sender_id, text=text).id
                            else:
                                sent = api.send_direct_message(
                                    recipient_id=sender_id, text="[BOT]\nMaaf ada kesalahan pada sistem :(\ntolong screenshot & laporkan kepada admin").id
                            tw.delete_dm(id)
                            tw.delete_dm(sent)

                    # elif constants.Second_Keyword in message and "https://" not in message and "http://" not in message and "twitter.com" not in message and len(message) <= 500:
                    #     message = message.replace(
                    #         constants.Second_Keyword, "")
                    #     if constants.Sub2_Keyword in message:
                    #         message = message.replace(
                    #             constants.Sub2_Keyword, "")
                    #         media.download_image()
                    #         media.process_image(message, screen_name)
                    #         postid = tw.post_tweet_quote(screen_name)
                    #         if postid != None:
                    #             text = notif + str(postid)
                    #             sent = api.send_direct_message(
                    #                 recipient_id=sender_id, text=text).id
                    #         else:
                    #             sent = api.send_direct_message(
                    #                 recipient_id=sender_id, text="[BOT]\nMaaf ada kesalahan pada sistem :(\ntolong screenshot & laporkan kepada admin").id
                    #         tw.delete_dm(id)
                    #         tw.delete_dm(sent)
                    #     else:
                    #         media.download_image()
                    #         media.process_image(message, None)
                    #         postid = tw.post_tweet_quote(name=None)
                    #         if postid != None:
                    #             text = notif + str(postid)
                    #             sent = api.send_direct_message(
                    #                 recipient_id=sender_id, text=text).id
                    #         else:
                    #             sent = api.send_direct_message(
                    #                 recipient_id=sender_id, text="[BOT]\nMaaf ada kesalahan pada sistem :(\ntolong screenshot & laporkan kepada admin").id
                    #         tw.delete_dm(id)
                    #         tw.delete_dm(sent)

                    # elif constants.Third_keyword in message:
                    #     message = message.replace(constants.Third_keyword, "")
                    #     if dms[i]['media'] is None:
                    #         sent1 = tw.ASK(message, screen_name)
                    #     elif dms[i]['type'] != 'photo':
                    #         print("asking with video")
                    #         message = message.split()
                    #         message = " ".join(message[:-1])
                    #         tw.download_media(dms[i]['media'], "video.mp4")
                    #         media_id = tw.media_upload_chunk(
                    #             "video.mp4", False)
                    #         remove("video.mp4")
                    #         sent1 = api.send_direct_message(sender_id, str(message + " @" + screen_name),
                    #                                         None, 'media', media_id).id
                    #     else:
                    #         print("asking with photo")
                    #         message = message.split()
                    #         message = " ".join(message[:-1])
                    #         tw.download_media(dms[i]['media'], "photo.jpg")
                    #         media_id = api.media_upload("photo.jpg")
                    #         remove("photo.jpg")
                    #         sent1 = api.send_direct_message(sender_id, str(message + " @" + screen_name),
                    #                                         None, 'media', media_id.media_id_string).id

                    #     sent = api.send_direct_message(
                    #         recipient_id=sender_id, text="[BOT]\nPesan kamu telah dikirimkan ke admin").id
                    #     tw.delete_dm(sent1)
                    #     tw.delete_dm(sent)
                    #     tw.delete_dm(id)

                    else:
                        sent = api.send_direct_message(
                            sender_id, "ketentuan keyword menfess kamu tidak sesuai!").id
                        tw.delete_dm(sent)
                        tw.delete_dm(id)

                except Exception as ex:
                    print(ex)
                    sleep(30)
                    pass

            dms = list()
            globals()['ACTION'] = 1
            print("waiting Github threading...")
            sleep(30)
            globals()['ACTION'] = 0

        else:
            print("Direct message is empty...")
            dms = tw.read_dm()
            if len(dms) == 0:
                sleep(30)


def Check_file_github(new=True):
    print("checking github file...")
    try:
        globals()['filename_github'] = "Database {}-{}-{}.txt".format(
            datetime.now().day, datetime.now().month, datetime.now().year)
        contents = repo.get_contents("")
        if any(filename_github == content.name for content in contents):
            print(f"filename_github detected, set: {str(new)}")
            if new == False:
                return
            else:
                contents = repo.get_contents(filename_github)
                contents = contents.decoded_content.decode()
                if contents[-1] == "\n":
                    contents = contents[:-1]

        else:
            print("filename_github not detected")
            repo.create_file(filename_github, "first commit",
                             "MESSAGE USERNAME SENDER_ID")
            contents = "MESSAGE USERNAME SENDER_ID"

        open(filename_github, 'w').write(contents)
        try:
            remove("Database {}-{}-{}.txt".format(
                datetime.now().day - 1, datetime.now().month, datetime.now().year))
            print("Yesterday's database has been deleted (UTC)")
        except:
            pass
            print("Heroku Yesterday's database doesn't exist (UTC)")

    except Exception as ex:
        pass
        print(ex)


def database():
    while True:
        try:
            if ACTION == 1:
                globals()['ACTION'] = 0
                print("Github threading active...")
                contents = repo.get_contents(filename_github)
                repo.update_file(contents.path, "updating database", open(
                    filename_github).read(), contents.sha)
                Check_file_github(new=False)
                print("Github Database updated")
                sleep(3600)

            else:
                sleep(10)

        except Exception as ex:
            print(ex)
            print("Github threading failed..")
            sleep(720)
            pass


if __name__ == "__main__":
    global filename_github, repo, ACTION
    filename_github = "Database {}-{}-{}.txt".format(
        datetime.now().day, datetime.now().month, datetime.now().year)
    repo = github.get_repo(constants.Github_repo)
    ACTION = 0

    Check_file_github(new=True)
    Thread(target=start).start()
    Thread(target=database).start()
