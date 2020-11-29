CONSUMER_KEY = "0uUBrW6eS70TCG6ARbc5CGTAm"
CONSUMER_SECRET = "x1Rj5WEyNIjFMUiV4pEC97B1LuLslb9WLFT3EcYIBOTxGJ27VX"
ACCESS_KEY = "1251147003897118721-ODhZ1ooTAZQNcAiYZ5cNX2W8tljmDe"
ACCESS_SECRET = "TiIi94r044O189z6Ct94MkCJlwDAQOkYE8AxMRUOnV42m"


Admin_id = ["1607653778"] # list of str 
# Admin id is like sender id. To check it, send a menfess from your admin account.
# or you can use api.get_user(screen_name="usernameoftheaccount")
# This is used to giving access to pass some message filters

Timezone = 7

Notify_queue = True
# bool, True: Send the menfess queue to sender
Notify_queueMessage = "Menfess kamu berada pada urutan ke-{}, akan terkirim sekitar pukul {}"
# Please keep the "{}" format -> .format(queue, time)

Notify_sent = True
# bool, True: Send menfess tweet link to sender when menfess sent
Notify_sentMessage = "Yeay! Menfess kamu telah terkirim! https://twitter.com/{}/status/"
# Please keep the "{}" format -> .format(post id)
Notify_sentFail1 = "Maaf ada kesalahan pada sistem :( \ntolong screenshot & laporkan kepada admin"
# Used when error is happened in system
Notify_sentFail2 = "ketentuan Triggerword menfess kamu tidak sesuai!"
# Used when sender sends menfess that ignored by algorithms

Delay_time = 0 # int, seconds
# Twitter API limiting to post tweet. System will delay 30s per/tweet. You can add it by input
# seconds in Delay_time. e.g Delay_time = 60, it means system will delay 90 seconds per tweet

Accept_message = True # For open DM
# bool, True: Auto accept message requests. make it False if you want to close your DM
Notify_acceptMessage = "Yeay! Sekarang kamu bisa mengirim menfess, jangan lupa baca peraturan base yaa!"

Keyword_deleter = True
# bool, True: Delete keyword from menfess before uploaded

Only_followed = True
# bool, True: only sender that followed by bot that can sends menfess
# delay in the beginning will be added, based on your followed accounts
# get 5000 account/minute, you can count it. Admin pass this filter.
# If you want to delete account from followed, send 'Set! rm_followed username1 username2 username-n'
# You can follow the sender as usual
Notify_followed = "Yeay! kamu udah difollow sama base ini. Jangan lupa baca peraturan sebelum mengirim menfess yaa!"
Notify_notFollowed = "Hmm, kamu belum difollow sama base ini. Jadi ga bisa ngirim menfess dehh :("

Sender_requirements = False
# bool, True: sender should pass the requirements. Admin pass this filter
Minimum_lenMenfess = 0 # the length of menfess
Minimum_followers = 0 # int
# Minimum-account-created-at
Minimum_year = 0 # e.g 1, it means sender account's should be created at 1 year ago
Minimum_month = 0
Minimum_day = 0
Notify_senderRequirements = "Hmm, menfess dan akun kamu ngga sesuai sama peraturan base :("

Private_mediaTweet = True
# bool, True: Remove a username on the bottom of the attached media tweet.
# Usually when sender wants to attachs more than one media, he will attach a media url
# from tweet. But the username of the sender is mentioned on the bottom of media. With this
# when sender attachs (media and/or media tweet) and if total of media ids are more than
# 4 media or the space is not available, THE REST OF THE MEDIA WILL BE ATTACHED TO THE
# SUBSEQUENT TWEETS IN SORTED ORDER.

Watermark = True
# bool, True: Add watermark text to sender's photo
Watermark_image = False 
# bool, True: Add watermark image
# You can change image and font in watermark folder
Watermark_text = "autobase_reborn"
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

Database = False 
# bool, True: Using database (Push simple txt to github)
# Github_token and Github_repo are not required when Database is False
Github_token = "****"
# get it from https://github.com/settings/tokens , set allow for editing repo
Github_repo = "username/your_repo"
# Make a repository first, then fill the Github_repo
# use another repo instead of primary repo

Trigger_word = ["fess!", "blablabla!"]
Notify_wrongTrigger = "Keyword yang kamu kirim salah!"
Sensitive_word = "/sensitive"
# Used when sender send sensitive content, order them to use this word
# But I advise against sending sensitive content, Twitter may ban your account,
# And using this bot for 'adult' base is strictly prohibited.
Blacklist_words = ['covid', 'blablabla']
Admin_cmd = "set!"  # exec command in Dict_adminCmd
User_cmd = "user!" # exec command in Dict_userCmd

# Please make Dict_admin/userCmd's command in lowercase
Dict_adminCmd = {
    'add_blacklist': 'administrator_data.Blacklist_words.append("{}")',


    'rm_blacklist': 'administrator_data.Blacklist_words.remove("{}")',


    'display_blacklist': 'self.send_dm(sender_id, str(administrator_data.Blacklist_words))', 


    'db_update': '''
contents = tmp.repo.get_contents(tmp.filename_github)
tmp.repo.update_file(contents.path, "updating Database", open(
    tmp.filename_github).read(), contents.sha)''',


    'rm_followed':'''
user = (api.get_user(screen_name="{}"))._json
api.destroy_friendship(user['id'])
self.followed.remove(int(user['id']))''',


    'who':'''
urls = message_data["entities"]["urls"]
if len(urls) == 0:
    raise Exception("Tweet link is not mentioned")
for i in urls:
    url = i["expanded_url"]
    postid = sub("[/.=?]", " ", url).split()[-3]
    found = 0
    for req_senderId in self.db_sent.keys():
        if found == 1:
            break
        for j in self.db_sent[req_senderId]:
            if j == postid:
                found = 1
                username = self.get_user_screen_name(req_senderId)
                text = "username: @" + username + "\\nid: " + req_senderId + " " + url
                self.send_dm(sender_id, text)
                break
    if found == 0:
        raise Exception("menfess is not found in db_sent")''',


    'add_admin':'''
user = (api.get_user(screen_name="{}"))._json
administrator_data.Admin_id.append(str(user['id']))''',


    'rm_admin':'''
user = (api.get_user(screen_name="{}"))._json
administrator_data.Admin_id.remove(str(user['id']))'''
}
# db_update is not available when Database set to False
# rm_followed is not available when Only_followed is False

Dict_userCmd = {
    'delete':'''
if sender_id not in self.db_sent and sender_id not in administrator_data.Admin_id:
    raise Exception("sender_id not in db_sent")
urls = message_data["entities"]["urls"]
if len(urls) == 0:
    raise Exception("Tweet link is not mentioned")
for i in urls:
    url = i["expanded_url"]
    postid = sub("[/.=?]", " ", url).split()[-3]
    if postid not in self.db_sent[sender_id] and sender_id not in administrator_data.Admin_id:
        raise Exception("sender doesn't have access to delete postid")
    elif postid in self.db_sent[sender_id]:
        self.db_sent_updater('delete', sender_id, postid)
    api.destroy_status(postid)
    '''
}
# delete is not available for user when bot was just started and user id not in db_sent
Notify_userCmdDelete = "Yeay! Menfess kamu sudah berhasil dihapus"
Notify_userCmdDeleteFail = "Duh! Menfess ini ngga bisa kamu hapus :("
