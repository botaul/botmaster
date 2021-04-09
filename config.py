NGROK_AUTH_TOKEN = ""
# sign up for ngrok. then copy the auth token from https://dashboard.ngrok.com/get-started/your-authtoken

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_KEY = ""
ACCESS_SECRET = ""
ENV_NAME = ""
# create Account Activity API (AAPI) dev env on https://developer.twitter.com/en/account/environments
# ENV_NAME is the same as Dev environment label
# Check your AAPI subcription renewal date on https://developer.twitter.com/en/account/subscriptions

Admin_id = [""] # list of str
# Admin id is like sender id. To check it, send a menfess from your admin account.
# or you can use api.get_user(screen_name="usernameoftheaccount")
# IF YOU WANT TO TEST THE CONFIG, REMEMBER THIS! USERS IN ADMIN_ID PASS ALL USER'S FILTERS, you should delete your id on Admin_id

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

Interval_perSender = False # bool
Interval_time = 0 # int
# Interval time (in minutes) of sending menfess per sender, Admin pass this filter
Notify_intervalPerSender = f"Mengirim menfess dibatasi! silakan coba sekitar {Interval_time} menit lagi"

Delay_time = 0 # int, seconds
# Twitter API limits user to post tweet. System will delay 36s per/tweet. You can add it by input
# seconds in Delay_time. e.g Delay_time = 60, it means system will delay 96 seconds per tweet

# Welcome message to new followers
Greet_newFollower = True
Notif_newFollower = "Makasih yaa udah follow base ini :) \nJangan lupa baca peraturan base!"

Keyword_deleter = False # Trigger word deleter
# bool, True: Delete keyword from menfess before uploaded

# send notif to user that followed by bot
Greet_followed = True
Notif_followed = "Yeay! kamu udah difollow base ini. Jangan lupa baca peraturan sebelum mengirim menfess yaa!"

Minimum_lenMenfess = 0 # length of the menfess
Maximum_lenMenfess = 9999999
Notify_lenMenfess = f"Maksimum jumlah karakter: {Maximum_lenMenfess}, Minimum jumlah karakter {Minimum_lenMenfess}"

Sender_requirements = False
# bool, True: sender should passes the following requirements:   (admin pass this filter)
Only_followed = False
Notif_notFollowed = "Hmm, kamu belum difollow base ini. Jadi ga bisa ngirim menfess dehh :("
# Minimum_followers and Minimum_day is (automatically) required when Sender_requirements is True.
Minimum_followers = 0 # int
# Minimum-account-created-at
Minimum_day = 0 # e.g 100, it means sender account must be created at 100 days ago
Notify_senderRequirements = f"Kamu harus punya {Minimum_followers} followers dan umur akun kamu harus\
     lebih dari {Minimum_day} hari biar bisa ngirim menfess :("

Private_mediaTweet = False
# bool, True: Delete username on the bottom of the attached media tweet.
# Usually when sender want to attach more than one media, they will attach a media url
# from tweet. But the username of the sender is mentioned on the bottom of media. With this
# when sender attach (media and/or media tweet) and if total of media ids are more than
# 4 media or the space is not available, THE REST OF THE MEDIA WILL BE ATTACHED TO THE
# SUBSEQUENT TWEETS IN SORTED ORDER.

Watermark = False
# bool, True: Add watermark text to sender's photo
Watermark_image = "twitter_autobase/watermark/photo.png" # bool or str
# bool, True: Add watermark using default image. str, file_path e.g 'twitter_autobase/watermark/photo.png'
# Watermark image's size must be square
Watermark_text = "lorem ipsum"
# If you won't to add text, fill str() or "" to Watermark_text.
# You can add enter "\n", maximum: 2 lines
Watermark_font = "twitter_autobase/watermark/FreeMono.ttf"
Watermark_textColor = (100,0,0,1)
Watermark_textStroke = (0,225,225,1)
# RGBA color format, you can search it on google
Watermark_ratio = 0.103 # float number under 1
# Ratio between watermark and sender's photo
Watermark_position = ('right', 'bottom') # (x, y)
# x: 'left', 'center', 'right'
# y: 'top', 'center', 'bottom'


Database = False
# bool, True: Using database (Make json file in local)
Github_database = False # Push json file to Github
# bool, True: using github to save database, False: database only in local
# Github_token and Github_repo are not required when Github_database is False
# You can directly update Github database using '#db_update' command from DM
Github_token = ""
# get it from https://github.com/settings/tokens , set allow for editing repo
Github_repo = "username/your_repo"
# Make a repository first, then fill the Github_repo
# use another repo instead of primary repo

Account_status = True
# bool, True: Turn on the automenfess. If it turned into False, this bot won't
# post menfess. You can switch it using '#switch on/off' command from DM
Notify_accountStatus = "Automenfess sedang dimatikan oleh admin, silakan cek tweet terbaru atau \
    hubungi admin untuk informasi lebih lanjut"

Trigger_word = ["fess!", "blablabla!"]
Notify_wrongTriggerUser = True # Will be send to user
Notify_wrongTriggerAdmin = False # menfess will be sent to admin
Notify_wrongTriggerMsg = "Trigger menfess tidak terdeteksi, pesan kamu akan dikirimkan ke admin"

Sensitive_word = "/sensitive"
# Used when sender send sensitive content, order them to use this word
# But I advise against sending sensitive content, Twitter may ban your account,
# And using this bot for 'adult' base is strictly prohibited.
Blacklist_words = ['covid', 'blablabla'] 
# hashtags and mentions will be changed into "#/" and "@/" in app.py to avoid ban
Notify_blacklistWords = "di menfess kamu terdapat blacklist words, jangan lupa baca peraturan base yaa!"
Notify_blacklistWordsAdmin = False # menfess will be sent to admin

# Please set Admin_cmd and User_cmd in lowercase
# If you want to modify command, don't edit #switch

Admin_cmd = {
    '#add_blacklist'    : 'AdminCmd.add_blacklist(arg)',
    '#rm_blacklist'     : 'AdminCmd.rm_blacklist(arg)',
    '#display_blacklist': 'AdminCmd.display_blacklist(sender_id) #no_notif',
    '#db_update'        : 'AdminCmd.db_update()',
    '#rm_followed'      : 'AdminCmd.rm_followed(selfAlias.followed, arg)',
    '#who'              : 'AdminCmd.who(selfAlias, sender_id, urls) #no_notif',
    '#add_admin'        : 'AdminCmd.add_admin(arg)',
    '#rm_admin'         : 'AdminCmd.rm_admin(arg)',
    '#switch'           : 'AdminCmd.switch(arg)',
}
# #no_notif is an indicator to skip send notif to admin
# db_update is not available when Database set to False
# rm_followed is not available when Only_followed is False
# who is only available for one day (reset every midnight or heroku dyno cycling)


User_cmd = {
    '#delete'           : 'UserCmd.delete(selfAlias, sender_id, urls)',
}
# delete is not available for user when bot was just started and user id not in db_sent
# delete & db_sent are only available for one day (reset every midnight or heroku dyno cycling)
Notify_userCmdDelete = "Yeay! Menfess kamu sudah berhasil dihapus"
Notify_userCmdDeleteFail = "Duh! Menfess ini ngga bisa kamu hapus :("
# Notify above are only for user
