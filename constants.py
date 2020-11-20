# ADMINISTRATOR DATA
CONSUMER_KEY = "45zUTBVu6nm1MlQJUH4bMDHGH"
CONSUMER_SECRET = "9dbYhPMz4oxmDSOnB7hsL7q0SV55IjS8sFAh7wXiAbwiPcHZJU"
ACCESS_KEY = "1251147003897118721-bBN7hLdCVr18eqpJeEYC4UDWmp5F55"
ACCESS_SECRET = "PYwH4s05xMQrhw43KZObBeFsF1gM9wwc3UxkC4yPbBo69"


database = False # False = off, True = on. put False if you won't to use database (optional)
# Github_token and Github_repo are not required when database is off
Github_token = "786958f436d746a34a683a6406607f637606974e"
# get it from https://github.com/settings/tokens , set allow for editing repo
Github_repo = "fakhrirofi/database"  # use another repo instead of primary repo


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


Admin_id = "1607653778"
# Admin id is like sender id. To check it, send a menfess from your admin account
Timezone = 7
