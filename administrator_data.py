CONSUMER_KEY = "***************"
CONSUMER_SECRET = "***************"
ACCESS_KEY = "***************"
ACCESS_SECRET = "***************"


Database = False # False = off, True = on. put False if you won't to use Database (optional)
# Github_token and Github_repo are not required when Database is off
Github_token = "***************"
# get it from https://github.com/settings/tokens , set allow for editing repo
Github_repo = "yourusername/Database"  # use another repo instead of primary repo


Trigger_word = ["fess!", "blablabla!"]  # trigger word

Muted_words = ['covid', 'blablabla']
Set_word = "set!"  # set muted_words and etc.
Dict_set = {
    'add_muted': 'administrator_data.Muted_words.append({})',

    'rm_muted': 'administrator_data.Muted_words.remove({})',

    'display_muted': '''
sent = temp.api.send_direct_message(recipient_id=administrator_data.Admin_id, text=str(administrator_data.Muted_words))
temp.api.destroy_direct_message(sent.id)''',

    'db_update': '''
contents = temp.repo.get_contents(temp.filename_github)
temp.repo.update_file(contents.path, "updating Database", open(
    temp.filename_github).read(), contents.sha)'''
} # db_update is not available when Database set to False


Admin_id = ""
# Admin id is like sender id. To check it, send a menfess from your admin account
Timezone = 7
