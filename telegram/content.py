'''Higher-level functions for Telegram bot messaging.'''
import json
from . import methods


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


class Update:
    def __init__(self, update_dict):
        if len(update_dict) != 2:
            raise ValueError('An update dict must only consist of "update_id" and an optional parameter.')
        self.id = update_dict['update_id']
        self.type = [k for k in update_dict.keys() if k != 'update_id'][0]
        self.content = update_dict[self.type]
        
        if self.type in {'message', 'edited_message', 'channel_post', 'edited_channel_post'}:
            self.cid = self.content['chat']['id']
        elif self.type == 'callback_query':
            self.cid = self.content['message']['chat']['id']

