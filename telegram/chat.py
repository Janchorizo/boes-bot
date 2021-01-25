'''Higher-level functions for Telegram bot messaging.'''
import json
from . import methods


def kick_member(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': chat_id}
    status, _ = methods.kickChatMember(token, params=params, verbose=verbose)
    return status


def unban_member(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': chat_id}
    status, _ = methods.unbanChatMember(token, params=params, verbose=verbose)
    return status


def restrict_member(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': chat_id}
    status, _ = methods.restrictChatMember(token, params=params, verbose=verbose)
    return status


def promote_member(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': chat_id}
    status, _ = methods.promoteChatMember(token, params=params, verbose=verbose)
    return status


def set_administrator_custom_title(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': chat_id}
    status, _ = methods.setChatAdministratorCustomTitle(token, params=params, verbose=verbose)
    return status


def set_permissions(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': chat_id}
    status, _ = methods.setChatPermissions(token, params=params, verbose=verbose)
    return status


def export_invite_link(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': chat_id}
    status, _ = methods.exportChatInviteLink(token, params=params, verbose=verbose)
    return status


def set_photo(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': chat_id}
    status, _ = methods.setChatPhoto(token, params=params, verbose=verbose)
    return status


def delete_photo(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': chat_id}
    status, _ = methods.deleteChatPhoto(token, params=params, verbose=verbose)
    return status


def set_title(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': chat_id}
    status, _ = methods.setChatTitle(token, params=params, verbose=verbose)
    return status


def set_description(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': chat_id}
    status, _ = methods.setChatDescription(token, params=params, verbose=verbose)
    return status


def pin_message(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': chat_id}
    status, _ = methods.pinChatMessage(token, params=params, verbose=verbose)
    return status


def unpin_message(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': chat_id}
    status, _ = methods.unpinChatMessage(token, params=params, verbose=verbose)
    return status


def unpin_all_messages(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': chat_id}
    status, _ = methods.unpinAllChatMessages(token, params=params, verbose=verbose)
    return status


def leave(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': chat_id}
    status, _ = methods.leaveChat(token, params=params, verbose=verbose)
    return status


def get(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': chat_id}
    status, _ = methods.getChat(token, params=params, verbose=verbose)
    return status


def get_administrators(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': chat_id}
    status, _ = methods.getChatAdministrators(token, params=params, verbose=verbose)
    return status


def get_members_count(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': chat_id}
    status, _ = methods.getChatMembersCount(token, params=params, verbose=verbose)
    return status


def get_member(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': chat_id}
    status, _ = methods.getChatMember(token, params=params, verbose=verbose)
    return status


def set_sticker_set(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': chat_id}
    status, _ = methods.setChatStickerSet(token, params=params, verbose=verbose)
    return status


def delete_sticker_set(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': chat_id}
    status, _ = methods.deleteChatStickerSet(token, params=params, verbose=verbose)
    return status
