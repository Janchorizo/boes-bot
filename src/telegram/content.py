'''Higher-level functions for Telegram bot messaging.'''
import json
from . import methods
from . import types


def get_user_profile_photos(
        token:str,
        user_id:str,
        offset=0,
        limit=10,
        verbose=False):
    '''Retrieve the specified user's profile photos.'''
    params = {
        'user_id': user_id,
        'offset': offset,
        'limit': limit
    }
    status, photos = \
        metods.getUserProfilePhotos(token, params=params, verbose=verbose)
    return status, photos


def getFile(token:str, file_id:str, verbose=False):
    '''Fetch a document of 20MB maximum size.'''
    params = {'file_id': file_id}
    status, file = methods.getFile(token, params=params, verbose=verbose)
    return status, file


def get_updates(token:str, verbose=False):
    '''Returns a list of bot updates.'''
    status, updates = methods.getUpdates(token, verbose=verbose)
    return status, updates


field_to_content_type = {
    'message': types.Message,
    'edited_message': types.Message,
    'channel_post': types.Message,
    'edited_channel_post': types.Message,
    'inline_query': types.InlineQuery,
    'chosen_inline_result': types.ChosenInlineResult,
    'callback_query': types.CallbackQuery,
    'shipping_query': types.ShippingQuery,
    'pre_checkout_query': types.PreCheckoutQuery,
    'poll': types.Poll,
    'poll_answer': types.PollAnswer
}


class Update:
    def __init__(self, update_dict):
        if len(update_dict) != 2:
            raise ValueError('An update dict must only consist of "update_id" and an optional parameter.')
        self.id = update_dict['update_id']
        self.field_name = [k for k in update_dict.keys() if k != 'update_id'][0]
        self.type = field_to_content_type[self.field_name]
        self.content = self.type(update_dict[self.field_name])

    @classmethod
    def fromstring(cls, jsonstring):
        return cls(json.loads(jsonstring))

    @classmethod
    def fromraw(cls, rawstring):
        return self.__class__.fromstring(rawstring.decode())

