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
