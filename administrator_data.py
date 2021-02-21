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
# The first tweet in queue won't be notified to sender (the delay is very quick).
Notify_queueMessage = "Menfess kamu berada pada urutan ke-{}, akan terkirim sekitar pukul {}"
# Please keep the "{}" format -> .format(queue, time)

Notify_sent = True
# bool, True: Send menfess tweet link to sender when menfess sent
Notify_sentMessage = "Yeay! Menfess kamu telah terkirim! https://twitter.com/{}/status/"
# Please keep the "{}" format -> .format(bot_username) + postid
Notify_sentFail1 = "Maaf ada kesalahan pada sistem :( \ntolong screenshot & laporkan kepada admin"
# Used when error is happened in system
Notify_sentFail2 = "ketentuan Triggerword menfess kamu tidak sesuai!"
# Used when sender sends menfess that ignored by algorithms

Interval_perSender = False # bool
Interval_time = 0 # int
# Interval time (in seconds) of sending menfess per sender, Admin pass this filter

Delay_time = 0 # int, seconds
# Twitter API limits user to post tweet. System will delay 30s per/tweet. You can add it by input
# seconds in Delay_time. e.g Delay_time = 60, it means system will delay 90 seconds per tweet

# Welcome message to new followers
Notify_acceptMessage = "Makasih yaa udah follow base ini :) \nJangan lupa baca peraturan base!"

Keyword_deleter = False # Trigger word deleter
# bool, True: Delete keyword from menfess before uploaded

Only_followed = False
# bool, True: only sender that followed by bot that can sends menfess
# delay in the beginning will be added, based on your followed accounts
# get 5000 account/minute, you can count it. Admin pass this filter.
# If you want to delete account from followed, send '#rm_followed username1 username2 username-n'
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

Private_mediaTweet = False
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
# bool, True: Using database (Make json file in local)
Github_database = False # Push json file to Github
# bool, True: using github to save database, False: database only in local
# Github_token and Github_repo are not required when Github_database is False
# You can directly update Github database using '#db_update' command from DM
Github_token = "****"
# get it from https://github.com/settings/tokens , set allow for editing repo
Github_repo = "username/your_repo"
# Make a repository first, then fill the Github_repo
# use another repo instead of primary repo

Account_status = True
# bool, True: Turn on the automenfess. If it turned into False, this bot won't
# post menfess. But, accept message & admin command are still running
# You can switch it using '#switch on/off' command from DM
# If there are messages on DM when turned off, those will be posted when this bot switched to on

Trigger_word = ["fess!", "blablabla!"]
Notify_wrongTrigger = "Trigger menfess tidak terdeteksi, pesan kamu akan dikirimkan ke admin"
# Message will be sent to admin
notifyWrongTrigger = False

Sensitive_word = "/sensitive"
# Used when sender send sensitive content, order them to use this word
# But I advise against sending sensitive content, Twitter may ban your account,
# And using this bot for 'adult' base is strictly prohibited.
Blacklist_words = ['covid', 'blablabla'] 
# hashtags and mentions will be changed into "#/" and "@/" in app.py to avoid ban
Notify_blacklistWords = "di menfess kamu terdapat blacklist words, jangan lupa baca peraturan base yaa!"

# Please set Admin_cmd and User_cmd in lowercase
# If you want to modify command, don't edit #switch

Admin_cmd = {
    '#add_blacklist'    : 'AdminCmd.add_blacklist(arg)',
    '#rm_blacklist'     : 'AdminCmd.rm_blacklist(arg)',
    '#display_blacklist': 'AdminCmd.display_blacklist(sender_id) #no_notif',
    '#db_update'        : 'AdminCmd.db_update()',
    '#rm_followed'      : 'AdminCmd.rm_followed(self.followed, arg)',
    '#who'              : 'AdminCmd.who(sender_id, self.db_sent, urls) #no_notif',
    '#add_admin'        : 'AdminCmd.add_admin(arg)',
    '#rm_admin'         : 'AdminCmd.rm_admin(arg)',
    '#switch'           : 'AdminCmd.switch(arg)',
}
# #no_notif is an indicator to skip send notif to admin
# db_update is not available when Database set to False
# rm_followed is not available when Only_followed is False
# who is only available for one day (reset every midnight or heroku dyno cycling)


User_cmd = {
    '#delete'           : 'UserCmd.delete(sender_id, self.db_sent, urls)',
}
# delete is not available for user when bot was just started and user id not in db_sent
# delete & db_sent are only available for one day (reset every midnight or heroku dyno cycling)
Notify_userCmdDelete = "Yeay! Menfess kamu sudah berhasil dihapus"
Notify_userCmdDeleteFail = "Duh! Menfess ini ngga bisa kamu hapus :("
# Notify above are only for user
