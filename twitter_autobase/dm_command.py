import re
from typing import NoReturn


class DMCommand:
    '''
    Command that can be accessed from direct message, you can manage command on config.py
    :param api: tweepy api object
    :param credential: object that contains attributes like config.py
    Attributes:
        - credential
        - api
        - repo
        - filename_github
    '''

    def __init__(self, api: object, credential: object):
        '''
        :param api: tweepy api object
        :param credential: object that contains attributes like config.py
        '''
        self.credential = credential
        self.api = api
        self.repo = lambda x: None
        self.repo.indicator = False # indicator for db_update method
        self.filename_github = str()


    def add_blacklist(self, word: str) -> NoReturn:
        '''
        :param word: word that will be added to Blacklist_words
        '''
        word = word.replace("_", " ")
        self.credential.Blacklist_words.append(word)


    def rm_blacklist(self, word: str) -> NoReturn:
        '''
        :param word: word that will be deleted from Blacklist_words
        '''
        word = word.replace("_", " ")
        self.credential.Blacklist_words.remove(word)


    def display_blacklist(self, sender_id: str) -> NoReturn:
        '''
        Send list of blacklist words to sender
        '''
        self.api.send_direct_message(recipient_id=sender_id, text=str(self.credential.Blacklist_words))


    def db_update(self) -> NoReturn:
        '''Update Github database
        '''
        if self.repo.indicator is False:
            raise Exception("Github database is disabled")
        contents = self.repo.get_contents(self.filename_github)
        with open(self.filename_github) as f:
            self.repo.update_file(contents.path, "updating Database", f.read(), contents.sha)
            f.close()


    def who(self, selfAlias: object, sender_id: str, urls: list) -> NoReturn:
        '''Check who was sent the menfess
        :param selfAlias: an alias of self from Autobase class
        :param urls: list of urls from dm
        '''
        if len(urls) == 0:
            raise Exception("Tweet link is not mentioned")
        
        for i in urls:
            url = i["expanded_url"]
            postid = str()

            if "?" in url:
                postid = re.sub("[/?]", " ", url).split()[-2]
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


    def add_admin(self, username: str) -> NoReturn:
        '''
        Add (append) user to credential.Admin_id
        :param username: username without '@'
        '''
        user = (self.api.get_user(screen_name=username))._json
        self.credential.Admin_id.append(str(user['id']))


    def rm_admin(self, username: str) -> NoReturn:
        '''
        :param username: username without '@'
        '''
        user = (self.api.get_user(screen_name=username))._json
        self.credential.Admin_id.remove(str(user['id']))


    def switch(self, arg: str) -> NoReturn:
        '''
        :param arg: 'on' or 'off'
        '''
        if arg.lower() == "on":
            self.credential.Account_status = True
        elif arg.lower() == "off":
            self.credential.Account_status = False
        else:
            raise Exception("available parameters are on or off")
    

    def _delete_tweet(self, postid: str, list_postid_thread: list) -> NoReturn:
        try:
            for postidx in [postid] + list_postid_thread:
                self.api.destroy_status(id=postidx) # It doesn't matter when error happen here
        except Exception as ex:
            raise Exception(f"You can't delete this tweet. Error: {ex}")


    def delete(self, selfAlias: object, sender_id: str, urls: list):
        '''Delete tweet
        :param selfAlias: an alias of self from Autobase class
        :param urls: list of urls from dm
        '''
        if sender_id not in selfAlias.db_sent and sender_id not in self.credential.Admin_id:
            raise Exception("sender_id not in db_sent")

        if len(urls) == 0:
            raise Exception("Tweet link is not mentioned")
        
        for i in urls:
            if "?" in i["expanded_url"]:
                postid = re.sub("[/?]", " ", i["expanded_url"]).split()[-2]
            else:
                postid = i["expanded_url"].split("/")[-1]   

            if sender_id in selfAlias.db_sent: # user has sent menfess
                if postid in selfAlias.db_sent[sender_id]: # normal succes
                    list_postid_thread = selfAlias.db_sent[sender_id][postid]
                    
                    selfAlias.db_sent_updater('add_deleted', sender_id, postid)
                    selfAlias.db_sent_updater('delete_sent', sender_id, postid)
                    
                    self._delete_tweet(postid, list_postid_thread)
                    return

                elif sender_id not in self.credential.Admin_id: # normal trying other menfess
                    raise Exception("sender doesn't have access to delete postid")
            
            elif sender_id not in self.credential.Admin_id: # user hasn't sent menfess
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
            
            self._delete_tweet(postid, list_postid_thread)
    
    
    def unsend(self, selfAlias: object, sender_id: str) -> NoReturn:
        '''
        :param selfAlias: an alias of self from Autobase class
        Delete the last tweet that sent by sender
        '''
        last_postid = list(selfAlias.db_sent[sender_id])[-1]
            
        list_postid_thread = selfAlias.db_sent[sender_id][last_postid]
        selfAlias.db_sent_updater('add_deleted', sender_id, last_postid)
        selfAlias.db_sent_updater('delete_sent', sender_id, last_postid)

        self._delete_tweet(last_postid, list_postid_thread)
