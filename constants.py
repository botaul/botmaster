CONSUMER_KEY = "Ar4PIPg9QaAZ7B0759VrUuqVR"
CONSUMER_SECRET = "qIDndM7ZNevsZ7KMpXDzoX6HJlOiKy7vsJQQPUGyI2VGhQBTWP"
ACCESS_KEY = "1251147003897118721-NE5wee97zNVRxQSzekuluDumTA1oJw"
ACCESS_SECRET = "O6BkVZYCYmOVYtlm89bJPT7w5cufISC3Ws1RcG6GBEWEk"


Github_token = "b5f57bc87595f0a14a0770d116eea6514b97d6df"
# get it from https://github.com/settings/tokens , set allow for editing repo
Github_repo = "fakhrirofi/database"  # use another repo instead of primary repo


First_Keyword = "fess!"  # primary keyword for tweet, video, and image
# Second_Keyword = "[quote]"  # for make image quoted
# Sub2_Keyword = "-s"  # give image quoted name
# Third_keyword = "[ask]"  # ask admin
Muted_words = ['covid', '#']
Set_keyword = "set!"  # set muted_words and etc.
Dict_set_keyword = {
    'add_muted': 'constants.Muted_words.append({})',

    'rm_muted': 'constants.Muted_words.remove({})',

    'display_muted': '''
sent = constants.api.send_direct_message(recipient_id=constants.Admin_id, text=str(constants.Muted_words))
constants.api.destroy_direct_message(sent.id)''',

    'db_update': '''
contents = constants.repo.get_contents(constants.filename_github)
constants.repo.update_file(contents.path, "updating database", open(
    constants.filename_github).read(), contents.sha)'''
}


Admin_id = "1607653778"
# Admin id is like sender id. To check it, send a menfess from your admin account
Timezone = 7
