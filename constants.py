# ADMINISTRATOR DATA
CONSUMER_KEY = "*****"
CONSUMER_SECRET = "*****"
ACCESS_KEY = "*****"
ACCESS_SECRET = "*****"


database = False # False = off, True = on. put False if you won't to use database (optional)
# Github_token and Github_repo are not required when database is off
Github_token = "*****"
# get it from https://github.com/settings/tokens , set allow for editing repo
Github_repo = "yourusername/database"  # use another repo instead of primary repo


First_Keyword = "fess!"  # trigger word

Muted_words = ['covid', 'blablabla']
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
} # db_update is not available when database set to False


Admin_id = "*****"
# Admin id is like sender id. To check it, send a menfess from your admin account
Timezone = 7
