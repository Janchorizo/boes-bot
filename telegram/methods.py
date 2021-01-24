'''Wrapper around the HTTP API for bot interacting.

It provides an abstraction over the HTTP protocol that
allows to interact with the bot services.
These functions are really low-level. It best to use
the abstractions provided in the other modules:
admin, chats, messages, content
'''
from .base import method_factory, MethodDesc

_methods = (
    MethodDesc(
        'GET', #verb
        'getMe', #method
        tuple(), #required
        tuple(), #default
        tuple(), #optional
        'Retrieves basic information about the bot.', #doc
    ),
    MethodDesc(
        'GET', #verb
        'logOut', #method
        tuple(), #required
        tuple(), #default
        tuple(), #optional
        'You must log out the bot before running it locally.', #doc
    ),
    MethodDesc(
        'GET', #verb
        'close', #method
        tuple(), #required
        tuple(), #default
        tuple(), #optional
        ('Closes the bot instance before moving it from\n'
         ' one local server to another.'), #doc
    ),
    MethodDesc(
        'POST', #verb
        'sendMessage', #method
        ('chat_id', 'text'), #required
        ('@', '""'), #default
        ('parse_mode', 'entities', 'disable_web_page_preview',
         'disable_notification', 'reply_to_message_id',
         'allow_sending_without_reply', 'reply_markup'), #optional
        'Sends text messages. On success, the sent Message is returned', #doc
    ),
    MethodDesc(
        'POST', #verb
        'forwardMessage', #method
        ('chat_id', 'from_chat_id', 'message_id'), #required
        ('@', '#', '&'), #default
        ('disable_notification'), #optional
        ('Forwards messages of any kind. On success,\n'
         ' the sent Message is returned.'), #doc
    ),
    MethodDesc(
        'POST', #verb
        'copyMessage', #method
        ('chat_id', 'from_chat_id', 'message_id'), #required
        ('@', '#', '&'), #default
        ('caption', 'parse_mode', 'caption_entities',
         'disable_notification', 'reply_to_message_id',
         'allow_sending_without_reply', 'reply_markup'), #optional
        ('Analogous to the method forwardMessages, but\n'
         " the copied message doesn't have a link to the\n"
         ' original message. Returns the MessageId of the\n'
         ' sent message on success.'), #doc
    ),
    MethodDesc(
        'POST', #verb
        'sendPhoto', #method
        ('chat_id', 'photo'), #required
        ('@', 'http://...'), #default
        ('caption', 'parse_mode', 'caption_entities',
         'disable_notification', 'reply_to_message_id',
         'allow_sending_without_reply', 'reply_markup'), #optional
        'Send photos. On success, the sent Message is returned.', #doc
    ),
    MethodDesc(
        'POST', #verb
        'sendAudio', #method
        ('chat_id', 'audio'), #required
        ('@', 'http://...'), #default
        ('caption', 'parse_mode', 'caption_entities',
         'duration', 'performer', 'title', 'thumb',
         'disable_notification', 'reply_to_message_id',
         'allow_sending_without_reply', 'reply_markup'), #optional
        ('Use this method to send audio (.MP3 or .M4A format)\n'
         ' files, if you want Telegram clients to display them\n'
         ' in the music player.'), #doc
    ),
    MethodDesc(
        'POST', #verb
        'sendDocument', #method
        ('chat_id', 'document'), #required
        ('@', 'http://...'), #default
        ('caption', 'parse_mode', 'caption_entities',
         'duration', 'performer', 'thumb',
         'disable_notification', 'reply_to_message_id',
         'allow_sending_without_reply', 'reply_markup',
         'disable_content_type_detection'), #optional
        'Use this method to general files.', #doc
    ),
    MethodDesc(
        'POST', #verb
        'sendVideo', #method
        ('chat_id', 'video'), #required
        ('@', 'http://...'), #default
        ('duration', 'width', 'height', 'thumb', 'caption',
         'parse_mode', 'caption_entities', 'supports_streaming',
         'disable_notification', 'reply_to_message_id',
         'allow_sending_without_reply', 'reply_markup'), #optional
        ('Use this method to send video files, Telegram'
         ' clients support mp4 videos (other formats may'
         ' be sent as Document).'), #doc
    ),
    MethodDesc(
        'POST', #verb
        'sendAnimation', #method
        ('chat_id', 'animation'), #required
        ('@', 'http://...'), #default
        ('duration', 'width', 'height', 'thumb', 'caption',
         'parse_mode', 'caption_entities', 'disable_notification',
         'reply_to_message_id', 'allow_sending_without_reply',
         'reply_markup'), #optional
        ('Use this method to send animation files (GIF or\n'
         ' H.264/MPEG-4 AVC video without sound)'), #doc
    ),
    MethodDesc(
        'POST', #verb
        'sendVoice', #method
        ('chat_id', 'voice'), #required
        ('@', 'http://...'), #default
        ('caption', 'parse_mode', 'caption_entities', 'duration',
         'disable_notification', 'reply_to_message_id',
         'allow_sending_without_reply', 'reply_markup'), #optional
        'Use this method to send audio files in an .OGG file encoded with OPUS.', #doc
    ),
    MethodDesc(
        'POST', #verb
        'sendVideoNote', #method
        ('chat_id', 'video_note'), #required
        ('@', 'http://...'), #default
        ('duration', 'length', 'thumb', 'disable_notification',
         'reply_to_message_id', 'allow_sending_without_reply',
         'reply_markup'), #optional
        ('As of v.4.0, Telegram clients support rounded square\n'
         ' mp4 videos of up to 1 minute long.'), #doc
    ),
    MethodDesc(
        'POST', #verb
        'sendMediaGroup', #method
        ('chat_id', 'media'), #required
        ('@', 'http://...'), #default
        ('disable_notification', 'reply_to_message_id',
         'allow_sending_without_reply'), #optional
        'Send a group of photos, videos, documents or audios as an album.', #doc
    ),
    MethodDesc(
        'POST', #verb
        'sendLocation', #method
        ('chat_id', 'latitude', 'longitude'), #required
        ('@', 'y', 'x'), #default
        ('horizontal_accuracy', 'live_period', 'heading',
         'proximity_alert_radius', 'disable_notification',
         'reply_to_message_id', 'allow_sending_without_reply',
         'reply_markup'), #optional
        'Send a point on the map.', #doc
    ),
    MethodDesc(
        'POST', #verb
        'editMessageLiveLocation', #method
        ('longitude', 'latitude'), #required
        ('x', 'y'), #default
        ('chat_id', 'message_id', 'inline_message_id',
         'horizontal_accuracy', 'heading', 'proximity_alert_radius',
         'reply_markup'), #optional
        ('Edit live location messages. A location can be edited\n'
         ' until its live_period expires or editing is explicitly\n'
         ' disabled by a call to stopMessageLiveLocation.'), #doc
    ),
    MethodDesc(
        'POST', #verb
        'stopMessageLiveLocation', #method
        tuple(), #required
        tuple(), #default
        ('chat_id', 'message_id', 'inline_message_id', 'reply_markup'), #optional
        'Stop updating a live location message before live_period expires.', #doc
    ),
    MethodDesc(
        'POST', #verb
        'sendVenue', #method
        ('chat_id', 'longitude', 'latitude', 'title', 'address'), #required
        ('@', 'x', 'y', '', ''), #default
        ('foursquare_id', 'foursquare_type', 'google_place_id',
         'google_place_type', 'disable_notiication', 'reply_to_message_id',
         'allow_sending_without_reply', 'reply'), #optional
        'Use this method to send information about a venue.', #doc
    ),
    MethodDesc(
        'POST', #verb
        'sendContact', #method
        ('chat_id', 'phone_number', 'first_name'), #required
        ('@', '', ''), #default
        ('last_name', 'vcard', 'disable_notification',
         'repy_to_message_id', 'allow_sending_without_reply',
         'reply_markup'), #optional
        'Use this method to send phone contacts.', #doc
    ),
    MethodDesc(
        'POST', #verb
        'sendPoll', #method
        ('chat_id', 'question', 'options'), #required
        ('@', '', '[]'), #default
        ('is_anonymous', 'type', 'allows_multiple_answers',
         'correct_option_id', 'explanation', 'explanation_parse_mode',
         'explanation_entities', 'open_period', 'close_date', 'is_closed',
         'is_closed', 'disable_notification', 'reply_to_message_id',
         'allow_sending_without_reply', 'reply_markup'), #optional
        'Use this method to send a native poll.', #doc
    ),
    MethodDesc(
        'POST', #verb
        'sendDice', #method
        ('chat_id'), #required
        ('@'), #default
        ('emoji', 'disable_notification', 'reply_to_message_id',
         'allow_sending_without_reply', 'reply_markup'), #optional
        'Use this method to send an animated emoji that will display a random value.', #doc
    ),
    MethodDesc(
        'POST', #verb
        'sendChatAction', #method
        ('chat_id', 'action'), #required
        ('@', ''), #default
        tuple(), #optional
        'Tell the user that something is happening on the bot\'s side.', #doc
    ),
    MethodDesc(
        'GET', #verb
        'getUserProfilePhotos', #method
        ('user_id',), #required
        ('@'), #default
        ('offset', 'limit'), #optional
        'Get a list of profile pictures for a user.', #doc
    ),
    MethodDesc(
        'GET', #verb
        'getFile', #method
        ('file_id',), #required
        tuple(), #default
        tuple(), #optional
        'For the moment, bots can download files of up to 20MB in size.', #doc
    ),
    MethodDesc(
        'GET', #verb
        'getUpdates', #method
        tuple(), #required
        tuple(), #default
        tuple(), #optional
        "Get a list of the bots' latest updates.", #doc
    ),
    MethodDesc(
        'POST', #verb
        'kickChatMember', #method
        ('chat_id', 'user_id'), #required
        ('@', '#'), #default
        ('until_date',), #optional
        'Kick a user from a group, a supergroup or a channel.', #doc
    ),
    MethodDesc(
        'POST', #verb
        'unbanChatMember', #method
        ('chat_id', 'user_id'), #required
        ('@', '#'), #default
        ('only_if_banned',), #optional
        ('Unban a previously kicked user in a supergroup or channel.\n'
         ' The user will not return to the group or channel automatically'), #doc
    ),
    MethodDesc(
        'POST', #verb
        'restrictChatMember', #method
        ('chat_id', 'user_id', 'permissions'), #required
        ('@', '#', '{}'), #default
        ('permissions', 'until_date'), #optional
        'Use this method to restrict a user in a supergroup.', #doc
    ),
    MethodDesc(
        'POST', #verb
        'promoteChatMember', #method
        ('chat_id', 'user_id'), #required
        ('@', '#'), #default
        ('is_anonymous', 'can_change_info', 'can_post_messages',
         'can_edit_messages', 'can_delete_messages', 'can_invite_users',
         'can_restrict_members', 'can_pin_messages', 'can_promote_members'), #optional
        'Promote or demote a user in a supergroup or a channel.', #doc
    ),
    MethodDesc(
        'POST', #verb
        'setChatAdministratorCustomTitle', #method
        ('chat_id', 'user_id', 'custom_title'), #required
        ('@', '#', ''), #default
        tuple(), #optional
        'Set a custom title for an administrator in a supergroup promoted by the bot.', #doc
    ),
    MethodDesc(
        'POST', #verb
        'setChatPermissions', #method
        ('chat_id', 'permissions'), #required
        ('@', '{}'), #default
        tuple(), #optional
        'Set default chat permissions for all members.', #doc
    ),
    MethodDesc(
        'POST', #verb
        'exportChatInviteLink', #method
        ('chat_id',), #required
        ('@',), #default
        tuple(), #optional
        ('Generate a new invite link for a chat; any previously\n'
         'generated link is revoked.'), #doc
    ),
    MethodDesc(
        'POST', #verb
        'setChatPhoto', #method
        ('chat_id', 'photo'), #required
        ('@', ''), #default
        tuple(), #optional
        'Set a new profile photo for the chat.', #doc
    ),
    MethodDesc(
        'POST', #verb
        'deleteChatPhoto', #method
        ('chat_id',), #required
        ('@',), #default
        tuple(), #optional
        ("Use this method to delete a chat photo. Photos\n"
         " can't be changed for private chats."), #doc
    ),
    MethodDesc(
        'POST', #verb
        'setChatTitle', #method
        ('chat_id', 'title'), #required
        ('@', ''), #default
        tuple(), #optional
        'Use this method to change the title of a chat.', #doc
    ),
    MethodDesc(
        'POST', #verb
        'setChatDescription', #method
        ('chat_id',), #required
        ('@',), #default
        ('description',), #optional
        ('Use this method to change the description of a group,\n'
         ' a supergroup or a channel.'), #doc
    ),
    MethodDesc(
        'POST', #verb
        'pinChatMessage', #method
        ('chat_id', 'message_id'), #required
        ('@', ''), #default
        ('disable_notification',), #optional
        ('Use this method to add a message to the list of\n'
         ' pinned messages in a chat.'), #doc
    ),
    MethodDesc(
        'POST', #verb
        'unpinChatMessage', #method
        ('chat_id',), #required
        ('@',), #default
        ('message_id',), #optional
        'Remove a message from the list of pinned messages in a chat.', #doc
    ),
    MethodDesc(
        'POST', #verb
        'unpinAllChatMessages', #method
        ('chat_id',), #required
        ('@',), #default
        tuple(), #optional
        'Clear the list of pinned messages in a chat.', #doc
    ),
    MethodDesc(
        'POST', #verb
        'leaveChat', #method
        ('chat_id',), #required
        ('@',), #default
        tuple(), #optional
        'Leave a group, supergroup or channel.', #doc
    ),
    MethodDesc(
        'POST', #verb
        'getChat', #method
        ('chat_id',), #required
        ('@',), #default
        tuple(), #optional
        'Get up to date information about the chat', #doc
    ),
    MethodDesc(
        'POST', #verb
        'getChatAdministrators', #method
        ('chat_id',), #required
        ('@',), #default
        tuple(), #optional
        'Get a list of administrators in a chat.', #doc
    ),
    MethodDesc(
        'POST', #verb
        'getChatMembersCount', #method
        ('chat_id',), #required
        ('@',), #default
        tuple(), #optional
        'Use this method to get the number of members in a chat.', #doc
    ),
    MethodDesc(
        'POST', #verb
        'getChatMember', #method
        ('chat_id', 'user_id'), #required
        ('@', '#'), #default
        tuple(), #optional
        'Get information about a member of a chat.', #doc
    ),
    MethodDesc(
        'POST', #verb
        'setChatStickerSet', #method
        ('chat_id', 'sticker_set_name'), #required
        ('@', ''), #default
        tuple(), #optional
        'Use this method to set a new group sticker set for a supergroup.', #doc
    ),
    MethodDesc(
        'POST', #verb
        'deleteChatStickerSet', #method
        ('chat_id',), #required
        ('@',), #default
        tuple(), #optional
        'Use this method to delete a group sticker set from a supergroup.', #doc
    ),
    MethodDesc(
        'POST', #verb
        'answerCallbackQuery', #method
        ('callback_query_id',), #required
        ('@',), #default
        ('text', 'show_alert', 'url', 'cache_time'), #optional
        ('Use this method to send answers to callback queries sent from\n'
         'inline keyboards. The answer will be displayed to the user as\n'
         'a notification at the top of the chat screen or as an alert.'), #doc
    ),
    MethodDesc(
        'POST', #verb
        'setMyCommands', #method
        ('commands',), #required
        ('[]',), #default
        tuple(), #optional
        "Use this method to change the list of the bot's commands.", #doc
    ),
    MethodDesc(
        'POST', #verb
        'getMyCommands', #method
        tuple(), #required
        tuple(), #default
        tuple(), #optional
        "Use this method to retrieve the list of the bot's commands.", #doc
    ),
    MethodDesc(
        'POST', #verb
        'editMessageText', #method
        ('text',), #required
        ('',), #default
        ('chat_id', 'message_id', 'inline_message_id',
         'parse_mode', 'entities', 'disable_web_page_preview',
         'reply_markup'), #optional
        ('Edit text and game messages. On success, if the edited\n'
         'message is not an inline message, the edited Message is\n'
         'returned, otherwise True is returned.'), #doc
    ),
    MethodDesc(
        'POST', #verb
        'editMessageCaption', #method
        tuple(), #required
        tuple(), #default
        ('chat_id', 'message_id', 'inline_message_id',
         'caption', 'parse_mode', 'caption_entities',
         'reply_markup'), #optional
        ('Use this method to edit captions of messages. On success,\n'
         'if the edited message is not an inline message, the edited\n'
         'Message is returned, otherwise True is returned.'), #doc
    ),
    MethodDesc(
        'POST', #verb
        'editMessageMedia', #method
        ('media',), #required
        ('{}',), #default
        ('chat_id', 'message_id', 'inline_message_id',
         'reply_markup'), #optional
        ('Use this method to edit animation, audio,\n'
         'document, photo, or video messages.'), #doc
    ),
    MethodDesc(
        'POST', #verb
        'editMessageReplyMarkup', #method
        tuple(), #required
        tuple(), #default
        ('chat_id', 'message_id', 'inline_message_id',
         'reply_markup'), #optional
        ('Use this method to edit only the reply markup of messages.'), #doc
    ),
    MethodDesc(
        'POST', #verb
        'stopPoll', #method
        ('chat_id', 'message_id'), #required
        ('@', '#'), #default
        ('reply_markup'), #optional
        ('Use this method to stop a poll which was sent by the bot.'), #doc
    ),
    MethodDesc(
        'POST', #verb
        'deleteMessage', #method
        ('chat_id', 'message_id'), #required
        ('@', '#'), #default
        tuple(), #optional
        ('Use this method to delete a message, including service messages.'), #doc
    ),
    MethodDesc(
        'POST', #verb
        'setWebhook', #method
        ('url',), #required
        ('https://...',), #default
        ('certificate', 'ip_address', 'max_connections',
         'allowed_updates', 'drop_pending_updates'), #optional
        ('Specify a url and receive incoming updates via an outgoing webhook.\n',
         'Whenever there is an update for the bot, we will send an HTTPS POST\n'
         'request to the specified url, containing a JSON-serialized Update.\n'
         'Pass an empty url to remove webhook integration.'), #doc
    ),
    MethodDesc(
        'POST', #verb
        'deleteWebhook', #method
        tuple(), #required
        tuple(), #default
        ('drop_pending_updates',), #optional
        'Remove webhook integration.', #doc
    ),
    MethodDesc(
        'GET', #verb
        'getWebhookInfo', #method
        tuple(), #required
        tuple(), #default
        tuple(), #optional
        ('Use this method to get current webhook status. Requires no parameters.\n'
         'On success, returns a WebhookInfo object. If the bot is using getUpdates,\n'
         'will return an object with the url field empty.'), #doc
    ),
)

for method in _methods:
    try:
        cls = method_factory(method)
    except ValueError as e:
        print(e)
    else:
        vars()[method.method] = cls()
