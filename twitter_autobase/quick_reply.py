from abc import abstractmethod, ABC
from typing import NoReturn

class ProcessQReply(ABC):
    '''
    Ref: https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/quick-replies/api-reference/options
    '''
    _tmp_dms: list = None
    dms: list = None
    credential: object = None

    @abstractmethod
    def transfer_dm(self, dm) -> NoReturn:
        pass

    @abstractmethod
    def send_dm(self, recipient_id, text, quick_reply_type=None, quick_reply_data=None,
                attachment_type=None, attachment_media_id=None) -> NoReturn:
        pass
    
    def _quick_reply_manager(self, sender_id, metadata) -> NoReturn:
        '''
        Manage dm buttons
        '''
        def accept_menfess():
            for x in self._tmp_dms.copy()[::-1]:
                if x['sender_id'] == sender_id:
                    self.transfer_dm(x)
                    self._tmp_dms.remove(x)
                    break

        def reject_menfess():
            for x in self._tmp_dms.copy()[::-1]:
                if x['sender_id'] == sender_id:
                    self._tmp_dms.remove(x)
                    break
                    
        dict_meta = {
            'accept_send_menfess'   : accept_menfess,
            'reject_send_menfess'   : reject_menfess,
        }
        dict_meta[metadata]()

    def send_verif_button(self, dm) -> NoReturn:
        data = self.credential.Verify_beforeSentData
        self.send_dm(dm['sender_id'], data['text'], quick_reply_type='options',
                     quick_reply_data=data['options'])
    