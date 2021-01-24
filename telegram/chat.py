'''Higher-level functions for Telegram bot messaging.'''
import json
from . import methods


def kick_chat_member(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': kickChatMember}
    status, _ = methods.kickChatMember(token, params=params, verbose=verbose)
    return status


def unban_chat_member(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': unbanChatMember}
    status, _ = methods.unbanChatMember(token, params=params, verbose=verbose)
    return status


def restrict_chat_member(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': restrictChatMember}
    status, _ = methods.restrictChatMember(token, params=params, verbose=verbose)
    return status


def promote_chat_member(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': promoteChatMember}
    status, _ = methods.promoteChatMember(token, params=params, verbose=verbose)
    return status


def set_chat_administrator_custom_title(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': setChatAdministratorCustomTitle}
    status, _ = methods.setChatAdministratorCustomTitle(token, params=params, verbose=verbose)
    return status


def set_chat_permissions(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': setChatPermissions}
    status, _ = methods.setChatPermissions(token, params=params, verbose=verbose)
    return status


def export_chat_invite_link(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': exportChatInviteLink}
    status, _ = methods.exportChatInviteLink(token, params=params, verbose=verbose)
    return status


def set_chat_photo(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': setChatPhoto}
    status, _ = methods.setChatPhoto(token, params=params, verbose=verbose)
    return status


def delete_chat_photo(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': deleteChatPhoto}
    status, _ = methods.deleteChatPhoto(token, params=params, verbose=verbose)
    return status


def set_chat_title(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': setChatTitle}
    status, _ = methods.setChatTitle(token, params=params, verbose=verbose)
    return status


def set_chat_description(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': setChatDescription}
    status, _ = methods.setChatDescription(token, params=params, verbose=verbose)
    return status


def pin_chat_message(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': pinChatMessage}
    status, _ = methods.pinChatMessage(token, params=params, verbose=verbose)
    return status


def unpin_chat_message(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': unpinChatMessage}
    status, _ = methods.unpinChatMessage(token, params=params, verbose=verbose)
    return status


def unpin_all_chat_messages(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': unpinAllChatMessages}
    status, _ = methods.unpinAllChatMessages(token, params=params, verbose=verbose)
    return status


def leave_chat(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': leaveChat}
    status, _ = methods.leaveChat(token, params=params, verbose=verbose)
    return status


def get_chat(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': getChat}
    status, _ = methods.getChat(token, params=params, verbose=verbose)
    return status


def get_chat_administrators(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': getChatAdministrators}
    status, _ = methods.getChatAdministrators(token, params=params, verbose=verbose)
    return status


def get_chat_members_count(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': getChatMembersCount}
    status, _ = methods.getChatMembersCount(token, params=params, verbose=verbose)
    return status


def get_chat_member(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': getChatMember}
    status, _ = methods.getChatMember(token, params=params, verbose=verbose)
    return status


def set_chat_sticker_set(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': setChatStickerSet}
    status, _ = methods.setChatStickerSet(token, params=params, verbose=verbose)
    return status


def delete_chat_sticker_set(token:str, chat_id:str, verbose=False):
    '''_'''
    params = {'chat_id': deleteChatStickerSet}
    status, _ = methods.deleteChatStickerSet(token, params=params, verbose=verbose)
    return status
