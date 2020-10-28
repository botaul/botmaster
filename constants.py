CONSUMER_KEY = "*********************"
CONSUMER_SECRET = "*********************"
ACCESS_KEY = "*********************"
ACCESS_SECRET = "*********************"


Github_token = "*********************"
# get it from https://github.com/settings/tokens , set allow for editing repo
Github_repo = "yourgithubusername/database"  # use another repo instead of primary repo


First_Keyword = "fess!"  # primary keyword for tweet, video, and image
Sub1_keyword = "attach"  # upload media from tweet url
# Second_Keyword = "[quote]"  # for make image quoted
# Sub2_Keyword = "-s"  # give image quoted name
# Third_keyword = "[ask]"  # ask admin
Muted_words = ['covid', 'blablabla']
Set_keyword = "set!"  # set muted_words and etc.
Dict_set_keyword = {
    'add_muted': 'constants.Muted_words.append({})',
    'rm_muted': 'constants.Muted_words.remove({})'
}


Admin_id = "*********************"
# Admin id is like sender id. To check it, send a menfess from your admin account