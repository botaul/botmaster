NGROK_AUTH_TOKEN = ""
# copy the auth token from https://dashboard.ngrok.com/get-started/your-authtoken

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
Interval_time = 5 # int
# Interval time (in minutes) of sending menfess per sender, Admin pass this filter
Notify_intervalPerSender = "Mengirim menfess dibatasi! silakan coba lagi setelah pukul {}"
# Please keep the "{}".format(time)

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
Maximum_lenMenfess = 1120
Notify_lenMenfess = f"Maksimum jumlah karakter: {Maximum_lenMenfess}, Minimum jumlah karakter {Minimum_lenMenfess}"

Only_QRTBaseTweet = False
Notif_QRTBaseTweet = "Kamu hanya bisa mengirim url tweet dari base ini :("

Only_twitterUrl = True
Notif_twitterUrl = "Kamu hanya bisa mengirim url yang berasal dari twitter :("

Sender_requirements = False
# bool, True: sender should passes the following requirements:   (admin pass this filter)
Only_followed = False
Notif_notFollowed = "Hmm, kamu belum difollow base ini. Jadi ga bisa ngirim menfess dehh :("
# Minimum_followers and Minimum_day is (automatically) required when Sender_requirements is True.
Minimum_followers = 0 # int
# Minimum-account-created-at
Minimum_day = 0 # e.g 100, it means sender account must be created at 100 days ago
Notify_senderRequirements = f"Kamu harus punya {Minimum_followers} followers dan umur akun kamu harus \
lebih dari {Minimum_day} hari biar bisa ngirim menfess :("

Private_mediaTweet = False
# bool, True: Delete username on the bottom of the attached video tweet.
# Usually when sender want to attach video (from tweet), they will attach a media url
# But the username of the (VIDEO) OWNER is mentioned on the bottom of video. With this
# when sender attach (media and/or media tweet) and if total of media ids are more than
# 4 or the space is not available, THE REST OF THE MEDIA WILL BE ATTACHED TO THE
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
Watermark_ratio = 0.15 # float number under 1 , ratio between watermark and sender's photo
Watermark_position = ('right', 'bottom') # (x, y)
# x: 'left', 'center', 'right'
# y: 'top', 'center', 'bottom'

Account_status = True
# bool, True: Turn on the automenfess. If it turned into False, this bot won't
# post menfess. You can switch it using '/switch on/off' command from DM
Notify_accountStatus = "Automenfess sedang dimatikan oleh admin, silakan cek tweet terbaru atau \
hubungi admin untuk informasi lebih lanjut"

Off_schedule = False
# schedule automenfess to turned off
Off_scheduleData = {
    'start'         : ('21', '06'), # ('hour', 'minute')
    'different_day' : True,
    'end'           : ('04', '36'), # ('hour', 'minute')
}
Off_scheduleMsg = f"Automenfess dimatikan setiap pukul {Off_scheduleData['start'][0]}:{Off_scheduleData['start'][1]} \
sampai dengan pukul {Off_scheduleData['end'][0]}:{Off_scheduleData['end'][1]}"

Trigger_word = ["fess!", "blablabla!"]
Notify_wrongTriggerUser = True # Will be sent to user
Notify_wrongTriggerAdmin = False # Will be sent to admin
Notify_wrongTriggerMsg = "Trigger menfess tidak terdeteksi"

Sensitive_word = "/sensitive"
# Used when sender send sensitive content, order them to use this word
# But I advise against sending sensitive content, Twitter may ban your account,
# And using this bot for 'adult' base is strictly prohibited.
Blacklist_words = ['covid', 'blablabla'] 
# hashtags and mentions will be changed to "#." and "@."
Notify_blacklistWords = "di menfess kamu terdapat blacklist words, jangan lupa baca peraturan base yaa!"
Notify_blacklistWordsAdmin = False # Will be sent to admin

# Please set Admin_cmd and User_cmd in lowercase
# Read README.md for the DMs examples
# You can move Admin_cmd to User_cmd and vice versa

Admin_cmd = {
    '/add_blacklist'    : 'self._add_blacklist(arg)', # /add_blacklist word1 word2 word-n
    '/rm_blacklist'     : 'self._rm_blacklist(arg)', # /rm_blacklist word1 word2 wordn
    '/display_blacklist': 'self._display_blacklist(sender_id) #no_notif', # /display_blacklist
    '/who'              : 'self._who_sender(sender_id, urls) #no_notif', # /who tweet_url
    '/add_admin'        : 'self._add_admin(arg)', # /add_admin username1 username2 username-n
    '/rm_admin'         : 'self._rm_admin(arg)', # /rm_admin username username2 username-n
    '/switch'           : 'self._switch_status(arg)', # /switch on | /switch off
    '/block'            : 'self._block_user(sender_id, urls) #no_notif', # /block tweet_url
    '/unfoll'           : 'self._unfoll_user(sender_id, urls) #no_notif', # /unfoll tweet_url
}
# #no_notif is an indicator to skip send notif to admin
# who is only available for one day (reset every midnight or heroku dyno cycling)

User_cmd = {
    '/delete'           : 'self._delete_menfess(sender_id, urls)', # /delete tweet_url
    '/unsend'           : 'self._unsend_menfess(sender_id)', # /unsend
    '/menu'             : 'self._menu_dm(sender_id) #no_notif', # /menu
    '/cancel'           : 'self._cancel_menfess(sender_id) #no_notif', # /cancel
}
# delete and unsend is not available for user when bot was just started and user id not in db_sent
# delete & db_sent are only available for one day (reset every midnight or heroku dyno cycling)
Notif_DMCmdDelete = {
    'succeed'   : 'Yeay! Menfess kamu sudah berhasil dihapus',
    'failed'    : 'Duh! Menfess ini ngga bisa kamu hapus :('
}
# Notif_DMCmdDelete is only for user, '/unsend' using this notif too
Notif_DMCmdCancel = {
    'succeed'   : 'Yeay! Menfess kamu berhasil di-cancel',
    'failed'    : 'Duh! Menfess kamu ngga bisa di-cancel'
}

DMCmdMenu = '''\
/menu : Menampilkan pesan ini
/unsend : Menghapus menfess terakhir yang sudah ter-post
/cancel : Menghapus menfess terakhir yang sedang dalam antrian
/delete (tweet_url) : Menghapus menfess tertentu dengan menyertakan url
'''
