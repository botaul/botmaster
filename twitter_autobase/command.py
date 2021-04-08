from re import sub

class AdminCommand:
    '''
    :param api: tweepy api object -> object
    :param credential: class (administrator_data) -> object
    '''

    def __init__(self, api, credential):
        '''
        Attributes:
            - credential
            - api
            - repo
            - filename_github

        :param api: tweepy api object -> object
        :param credential: class (administrator_data) -> object
        '''
        self.credential = credential
        self.api = api
        self.repo = lambda x: None
        self.repo.indicator = False # indicator for db_update method
        self.filename_github = str()
    
    def add_blacklist(self, word):
        '''
        :param word: word that will be added to Blacklist_words -> str
        '''
        word = word.replace("_", " ")
        self.credential.Blacklist_words.append(word)
    
    def rm_blacklist(self, word):
        '''
        :param word: word that will be deleted from Blacklist_words -> str
        '''
        word = word.replace("_", " ")
        self.credential.Blacklist_words.remove(word)

    def display_blacklist(self, sender_id):
        '''
        :param sender_id: id who was sent the command -> str or int
        '''
        sent = self.api.send_direct_message(recipient_id=sender_id, text=str(self.credential.Blacklist_words))
        self.api.destroy_direct_message(sent.id)

    def db_update(self):
        '''Update Github database
        '''
        if self.repo.indicator is False:
            raise Exception("Github database is disabled")
        contents = self.repo.get_contents(self.filename_github)
        with open(self.filename_github) as f:
            self.repo.update_file(contents.path, "updating Database", f.read(), contents.sha)
            f.close()
    
    def rm_followed(self, followed, username):
        '''Delete id from followed database
        :param followed: list of followed -> list
        :param username: username of the account -> str
        '''
        user = (self.api.get_user(screen_name=username))._json
        self.api.destroy_friendship(user['id'])
        if int(user['id']) in followed:
            followed.remove(int(user['id']))
        else:
            raise Exception("Only_followed is disabled, but destroy_friendship is succeeded")
    
    def who(self, selfAlias, sender_id, urls):
        '''Check who was sent the menfess
        :param sender_id: id of sender -> str
        :param db_sent: dictionary of db_sent -> dict
        :param urls: list of urls from dm -> list
        '''
        if len(urls) == 0:
            raise Exception("Tweet link is not mentioned")
        
        for i in urls:
            url = i["expanded_url"]
            postid = str()

            if "?" in url:
                postid = sub("[/?]", " ", url).split()[-2]
            else:
                postid = url.split("/")[-1]

            for req_senderId in selfAlias.db_sent.keys():
                if postid in selfAlias.db_sent[req_senderId].keys():
                    username = selfAlias.get_user_screen_name(req_senderId)
                    text = f"username: @{username}\nid: {req_senderId}\nstatus: exists {url}"
                    selfAlias.send_dm(sender_id, text)
                    return
            
            for req_senderId in selfAlias.db_deleted.keys():
                if postid in selfAlias.db_deleted[req_senderId]:
                    username = selfAlias.get_user_screen_name(req_senderId)
                    text = f"username @{username}\nid: {req_senderId}\nstatus: deleted\nurl: {url}"
                    selfAlias.send_dm(sender_id, text)
                    return

            raise Exception("menfess is not found in db_sent or db_deleted")
        
    def add_admin(self, username):
        '''
        :param username: username without '@' -> str
        '''
        user = (self.api.get_user(screen_name=username))._json
        self.credential.Admin_id.append(str(user['id']))
    
    def rm_admin(self, username):
        '''
        :param username: username without '@' -> str
        '''
        user = (self.api.get_user(screen_name=username))._json
        self.credential.Admin_id.remove(str(user['id']))

    def switch(self, arg):
        '''
        :param arg: 'on' or 'off'
        '''
        if arg.lower() == "on":
            self.credential.Account_status = True
        elif arg.lower() == "off":
            self.credential.Account_status = False
        else:
            raise Exception("available parameters are on or off")
    

class UserCommand:
    '''
    Attributes:
        - Admin_id
        - api
    
    :param api: tweepy api object -> object
    :param credential: class (administrator_data) -> object
    '''
    def __init__(self, api, credential):
        '''
        :param api: tweepy api object -> object
        :param credential: class (administrator_data) -> object
        '''
        self.Admin_id = credential.Admin_id
        self.api = api


    def delete(self, selfAlias, sender_id, urls):
        '''Access to user is limited
        :param sender_id: id of the sender -> str
        :param db_sent: dictionary of db_sent -> dict
        :param urls: list of urls from dm -> list
        '''
        if sender_id not in selfAlias.db_sent and sender_id not in self.Admin_id:
            raise Exception("sender_id not in db_sent")

        if len(urls) == 0:
            raise Exception("Tweet link is not mentioned")
        
        for i in urls:
            if "?" in i["expanded_url"]:
                postid = sub("[/?]", " ", i["expanded_url"]).split()[-2]
            else:
                postid = i["expanded_url"].split("/")[-1]
            
            def delete_tweet(postid, list_postid_thread):
                try:
                    for postidx in [postid] + list_postid_thread:
                        self.api.destroy_status(id=postidx) # It doesn't matter when error happen here
                except Exception as ex:
                    raise Exception(f"You can't delete this tweet. Error: {ex}")   

            if sender_id in selfAlias.db_sent: # user has sent menfess
                if postid in selfAlias.db_sent[sender_id]: # normal succes
                    list_postid_thread = selfAlias.db_sent[sender_id][postid]
                    
                    selfAlias.db_sent_updater('add_deleted', sender_id, postid)
                    selfAlias.db_sent_updater('delete_sent', sender_id, postid)
                    
                    delete_tweet(postid, list_postid_thread)
                    return

                elif sender_id not in self.Admin_id: # normal trying other menfess
                    raise Exception("sender doesn't have access to delete postid")
            
            elif sender_id not in self.Admin_id: # user hasn't sent menfess
                raise Exception("sender doesn't have access to delete postid")
            
            # administrator mode
            found = 0 # sender_id that will be searched
            for req_senderId in selfAlias.db_sent.keys():
                if postid in selfAlias.db_sent[req_senderId].keys():
                    found = req_senderId
                    break

            if found != 0:
                list_postid_thread = selfAlias.db_sent[found][postid]
                selfAlias.db_sent_updater('add_deleted', found, postid)
                selfAlias.db_sent_updater('delete_sent', found, postid)
            else:
                list_postid_thread = list()
                print("admin mode: directly destroy_status")
            
            delete_tweet(postid, list_postid_thread)
