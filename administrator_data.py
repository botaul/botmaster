CONSUMER_KEY = "****"
CONSUMER_SECRET = "****"
ACCESS_KEY = "****"
ACCESS_SECRET = "****"


Admin_id = ["****"] # list of str
# Admin id is like sender id. To check it, send a menfess from your admin account.
# or you can use api.get_user(screen_name="usernameoftheaccount")
# This is used to giving access to pass some message filters & admin command

Timezone = 7

Notify_queue = True
# bool, True: Send the menfess queue to sender
# The first sender in queue won't be notified. Because the delay is very quick.
Notify_queueMessage = "Menfess kamu berada pada urutan ke-{}, akan terkirim sekitar pukul {}"
# Please keep the "{}" format -> .format(queue, time)

Notify_sent = True
# bool, True: Send menfess tweet link to sender when menfess sent
Notify_sentMessage = "Yeay! Menfess kamu telah terkirim! https://twitter.com/{}/status/"
# Please keep the "{}" format -> .format(bot username) + postid
Notify_sentFail1 = "Maaf ada kesalahan pada sistem :( \ntolong screenshot & laporkan kepada admin"
# Used when error is happened in system
Notify_sentFail2 = "ketentuan Triggerword menfess kamu tidak sesuai!"
# Used when sender sends menfess that ignored by algorithms

Interval_perSender = False # bool
Interval_time = 0 # int
# Interval time (in seconds) of sending menfess per sender, Admin pass this filter

Delay_time = 0 # int, seconds
# Twitter API limiting to post tweet. System will delay 30s per/tweet. You can add it by input
# seconds in Delay_time. e.g Delay_time = 60, it means system will delay 90 seconds per tweet

# Welcome message to new followers
Notify_acceptMessage = "Makasih yaa udah follow base ini :) \nJangan lupa baca peraturan base!"

Keyword_deleter = False # Trigger word deleter
# bool, True: Delete keyword from menfess before uploaded

Only_followed = False
# bool, True: only sender that followed by bot that can sends menfess
# delay in the beginning will be added, based on your followed accounts
# get 5000 account/minute, you can count it. Admin pass this filter.
# If you want to delete account from followed, send 'Set! rm_followed username1 username2 username-n'
# You can follow the sender as usual
Notify_followed = "Yeay! kamu udah difollow sama base ini. Jangan lupa baca peraturan sebelum mengirim menfess yaa!"
Notify_notFollowed = "Hmm, kamu belum difollow sama base ini. Jadi ga bisa ngirim menfess dehh :("

Minimum_lenMenfess = 0 # length of the menfess

Sender_requirements = False
# bool, True: sender should pass the account requirements. Admin pass this filter
Minimum_followers = 0 # int
# Minimum-account-created-at
Minimum_day = 0 # e.g 100, it means sender account must be created at 100 days ago
Notify_senderRequirements = "Hmm, menfess dan akun kamu ngga sesuai sama peraturan base :("

Private_mediaTweet = True
# bool, True: Delete username on the bottom of the attached media tweet.
# Usually when sender want to attach more than one media, they will attach a media url
# from tweet. But the username of the sender is mentioned on the bottom of media. With this
# when sender attach (media and/or media tweet) and if total of media ids are more than
# 4 media or the space is not available, THE REST OF THE MEDIA WILL BE ATTACHED TO THE
# SUBSEQUENT TWEETS IN SORTED ORDER.

Watermark = False
# bool, True: Add watermark text to sender's photo
Watermark_image = False # bool or str
# bool, True: Add watermark using default image. str, file_path e.g 'watermark/photo.png'
# the default image path is 'watermark/photo.png'
# You can change default image and font in watermark folder
Watermark_text = "lorem ipsum"
# If you won't to add text, fill str() or "" to Watermark_text.
# You can add enter "\n", maximum: 2 lines
Watermark_textColor = (100,0,0,1)
Watermark_textStroke = (0,225,225,1)
# RGBA color format, you can search it on google
Watermark_ratio = 0.103 # float number under 1
# Ratio between watermark and sender's photo
Watermark_position = ('right', 'bottom') # (x, y)
# x: 'left', 'center', 'right'
# y: 'top', 'center', 'bottom'

Keep_DM = False
# bool, True: DMs id will be stored on db_received
# So, the messages are still exist on your DM.
# ONLY MESSAGES SENT BY SENDER that still exist & will be stored.
# Don't delete messages from DM using Twitter app to avoid error.
# Advantages : - Easy to monitor from DM
#              - Heroku or other database is not required
# Disadvantages: - Only messages that received AFTER BOT STARTED that will be processed.
#                - Twitter API only list the 50 most recent messages. So, if there are more
#                  than 50 new (sender) messages in a queue, the rest won't be processed.
# If you want to change keep_DM from True to False, all messages in last month must be deleted
# to avoid repeated messages in the process.
# [[[Example of code to to delete all messages]]]
# from tweepy import API, Cursor, OAuthHandler
# auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
# auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
# api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
# ids = list()
# for page in Cursor(api.list_direct_messages, count=50).pages():
#     ids.extend(page)
#     sleep(60)
# for id in ids: api.destroy_direct_message(id)

Database = False 
# bool, True: Using database (Push simple txt to github every midnight),
# You can directly update using 'set! db_update' command from DM
# Github_token and Github_repo are not required when Database is False
Github_token = "****"
# get it from https://github.com/settings/tokens , set allow for editing repo
Github_repo = "username/your_repo"
# Make a repository first, then fill the Github_repo
# use another repo instead of primary repo

Account_status = True
# bool, True: Turn on the automenfess. If it turned into False, this bot won't
# post menfess. But, accept message & command features are still running
# You can switch it using 'set! switch on/off' command from DM
# If there are messages on DM when turned off, those will be posted when this bot switched to on

Trigger_word = ["fess!", "blablabla!"]
Notify_wrongTrigger = "Keyword yang kamu kirim salah!"
Sensitive_word = "/sensitive"
# Used when sender send sensitive content, order them to use this word
# But I advise against sending sensitive content, Twitter may ban your account,
# And using this bot for 'adult' base is strictly prohibited.
Blacklist_words = ['covid', 'blablabla'] 
# hashtags and mentions will be changed into "#/" and "@/" in app.py to avoid ban
Admin_cmd = "set!"  # exec command in Dict_adminCmd
User_cmd = "user!" # exec command in Dict_userCmd

# Please make Dict_admin/userCmd's command in lowercase
Dict_adminCmd = {
    'add_blacklist': 'administrator_data.Blacklist_words.append("{}")',


    'rm_blacklist': 'administrator_data.Blacklist_words.remove("{}")',


    'display_blacklist': 'self.send_dm(sender_id, str(administrator_data.Blacklist_words))', 


    'db_update': '''
contents = tmp.repo.get_contents(tmp.filename_github)
with open(tmp.filename_github) as f:
    tmp.repo.update_file(contents.path, "updating Database", f.read(), contents.sha)
    f.close()''',


    'rm_followed':'''
user = (api.get_user(screen_name="{}"))._json
self.followed.remove(int(user['id']))
api.destroy_friendship(user['id'])''',


    'who':'''
urls = message_data["entities"]["urls"]
if len(urls) == 0:
    raise Exception("Tweet link is not mentioned")
for i in urls:
    url = i["expanded_url"]
    postid = str()
    if "?" in url:
        postid = sub("[/?]", " ", url).split()[-2]
    else:
        postid = url.split("/")[-1]
    found = 0
    for req_senderId in self.db_sent.keys():
        if found == 1:
            break
        if req_senderId == 'deleted':
            # 'deleted': (req_senderId, postid)
            for x in self.db_sent['deleted']:
                if x[1] == postid:
                    found, req_senderId = 1, x[0]
                    username = self.get_user_screen_name(req_senderId)
                    text = "username: @" + username + "\\nid: " + req_senderId + "\\nstatus: deleted\\nurl: " + url
                    self.send_dm(sender_id, text)
                    break
            continue
        for j in self.db_sent[req_senderId]:
            if j == postid:
                found = 1
                username = self.get_user_screen_name(req_senderId)
                text = "username: @" + username + "\\nid: " + req_senderId + "\\nstatus: exists " + url
                self.send_dm(sender_id, text)
                break
    if found == 0:
        raise Exception("menfess is not found in db_sent")''',


    'add_admin':'''
user = (api.get_user(screen_name="{}"))._json
administrator_data.Admin_id.append(str(user['id']))''',


    'rm_admin':'''
user = (api.get_user(screen_name="{}"))._json
administrator_data.Admin_id.remove(str(user['id']))''',


    'switch':'''
status = "{}"
if status == "on":
    administrator_data.Account_status = True
elif status == "off":
    administrator_data.Account_status = False
else:
    raise Exception("available parameters are on or off")'''
}
# db_update is not available when Database set to False
# rm_followed is not available when Only_followed is False
# who is only available for one day (reset every midnight)

Dict_userCmd = {
    'delete':'''
if sender_id not in self.db_sent and sender_id not in administrator_data.Admin_id:
    raise Exception("sender_id not in db_sent")
urls = message_data["entities"]["urls"]
if len(urls) == 0:
    raise Exception("Tweet link is not mentioned")
for i in urls:
    postid = str()
    if "?" in i["expanded_url"]:
        postid = sub("[/?]", " ", i["expanded_url"]).split()[-2]
    else:
        postid = i["expanded_url"].split("/")[-1]
    found = 0
    if sender_id in self.db_sent: # user has sent menfess
        if postid in self.db_sent[sender_id]: # normal succes
            self.db_sent_updater('add', 'deleted', (sender_id, postid))
            self.db_sent_updater('delete', sender_id, postid)
            found = 1
        elif sender_id not in administrator_data.Admin_id: # normal trying other menfess
            raise Exception("sender doesn't have access to delete postid")
    elif sender_id not in administrator_data.Admin_id: # user hasn't sent menfess
        raise Exception("sender doesn't have access to delete postid")
    if found == 0: # administrator mode
        for req_senderId in self.db_sent.keys():
            if found != 0:
                break
            for j in self.db_sent[req_senderId]:
                if j == postid:
                    found = req_senderId
                    break
        if found != 0:
            self.db_sent_updater('add', 'deleted', (found, postid))
            self.db_sent_updater('delete', found, postid)
        else:
            print("admin mode: directly destroy_status")
    api.destroy_status(id=postid) # It doesn't matter when error happen here'''
}
# delete is not available for user when bot was just started and user id not in db_sent
# delete & db_sent are only available for one day (reset every midnight)
Notify_userCmdDelete = "Yeay! Menfess kamu sudah berhasil dihapus"
Notify_userCmdDeleteFail = "Duh! Menfess ini ngga bisa kamu hapus :("
# Notify above are only for user
