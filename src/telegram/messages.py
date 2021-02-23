'''Higher-level functions for Telegram bot messaging.

Sending messages is intended to be done by instantiating one
of the content types and use the instance method.
'''
import os
import json
import functools
from . import methods


class ParameterGroup:
    '''Used to hold a valid combination of parameters for a method.
    '''
    method = None

    def __init__(self, *args, **kwargs):
        required = set(self.method.required) - {'chat_id'}
        supported = required | set(self.method.optional)
        missing_required = any(k not in kwargs for k in required)
    
        if missing_required:
            msg = 'Too few arguments. At least {} should be provided.'
            raise ValueError(msg.format(required))

        has_unsupported = any(k not in supported for k in kwargs)

        if has_unsupported:
            msg = 'Invalid argument. Only {} are supported.'
            raise ValueError(msg.format(supported))

        self._params = kwargs

    @property
    def params(self):
        return dict(self._params)

    @property
    def files(self):
        return None

    def _use(self, token, chat_id, verbose=False):
        params = {'chat_id':chat_id, **self.params}
        files = self.files
        print(params, files)
        status, msg = self.method(token, params=params, files=files, verbose=verbose)
        return status, msg


class Content(ParameterGroup):
    '''Syntactic sugar to keep the semantics.
    Represents a "sendable" piece of information.
    '''
    def send(self, token, chat_id, verbose=False):
        return self._use(token, chat_id, verbose)


class ReplacementContent(ParameterGroup):
    '''Syntactic sugar to keep the semantics.
    Represents a piece of content to be replaced in an existing message.
    '''
    def apply(self, token, chat_id, verbose=False):
        return self._use(token, chat_id, verbose)


class MessageContent(Content):
    method = methods.sendMessage


class PhotoContent(Content):
    method = methods.sendPhoto

    @property
    def params(self):
        params_copy = dict(self._params)
        if hasattr(params_copy['photo'], 'read'):
            params_copy.pop('photo')
        return params_copy

    @property
    def files(self):
        if hasattr(self._params['photo'], 'read'):
            return {'photo':
                (self._params['photo'].name, self._params['photo'])}
        return None


class AudioContent(Content):
    method = methods.sendAudio
    
    @property
    def params(self):
        params_copy = dict(self._params)
        if hasattr(params_copy['audio'], 'read'):
            params_copy.pop('audio')
        return params_copy

    @property
    def files(self):
        if hasattr(self._params['audio'], 'read'):
            return {'audio':
                (self._params['audio'].name, self._params['audio'])}
        return None


class DocumentContent(Content):
    method = methods.sendDocument

    @property
    def params(self):
        params_copy = dict(self._params)
        if hasattr(params_copy['document'], 'read'):
            params_copy.pop('document')
        return params_copy

    @property
    def files(self):
        if hasattr(self._params['document'], 'read'):
            return {'document':
                (self._params['document'].name, self._params['document'])}
        return None


class VideoContent(Content):
    method = methods.sendVideo

    @property
    def params(self):
        params_copy = dict(self._params)
        if hasattr(params_copy['video'], 'read'):
            params_copy.pop('video')
        return params_copy

    @property
    def files(self):
        if hasattr(self._params['video'], 'read'):
            return {'video':
                (self._params['video'].name, self._params['video'])}
        return None


class AnimationContent(Content):
    method = methods.sendAnimation

    @property
    def params(self):
        params_copy = dict(self._params)
        if hasattr(params_copy['animation'], 'read'):
            params_copy.pop('animation')
        return params_copy

    @property
    def files(self):
        if hasattr(self._params['animation'], 'read'):
            return {'animation':
                (self._params['animation'].name, self._params['animation'])}
        return None


class VoiceContent(Content):
    method = methods.sendVoice

    @property
    def params(self):
        params_copy = dict(self._params)
        if hasattr(params_copy['voice'], 'read'):
            params_copy.pop('voice')
        return params_copy

    @property
    def files(self):
        if hasattr(self._params['voice'], 'read'):
            return {'voice':
                (self._params['voice'].name, self._params['voice'])}
        return None


class VideoNoteContent(Content):
    method = methods.sendVideoNote

    @property
    def params(self):
        params_copy = dict(self._params)
        if hasattr(params_copy['video_note'], 'read'):
            params_copy.pop('video_note')
        return params_copy

    @property
    def files(self):
        if hasattr(self._params['video_note'], 'read'):
            return {'video_note':
                (self._params['video_note'].name, self._params['video_note'])}
        return None


class MediaGroupContent(Content):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError()


class LocationContent(Content):
    method = methods.sendLocation


class VenueContent(Content):
    method = methods.sendVenue


class ContactContent(Content):
    method = methods.sendContact


class DiceContent(Content):
    method = methods.sendDice


class ChatActionContent(Content):
    method = methods.sendChatAction


class TextReplacementContent(ReplacementContent):
    method = methods.editMessageText


class CaptionReplacementContent(ReplacementContent):
    method = methods.editMessageCaption


class MediaReplacementContent(ReplacementContent):
    # See how to support the different media types
    # InputMediaAnimation
    # InputMediaDocument
    # InputMediaAudio
    # InputMediaPhoto
    # InputMediaVideo
    method = methods.editMessageMedia
    type_ = 'document'

    @property
    def params(self):
        params_copy = dict(self._params)

        media = {
            k: v 
            for k,v
            in params_copy['media'].items()
            if k != 'content'
        }
        media['type'] = self.type_

        if hasattr(params_copy['media']['content'], 'read'):            
            media['media'] = f'attach://{self._params["media"]["content"].name}'
        else:
            media['media'] = params_copy['media']['content']

        params_copy['media'] = json.dumps(media)
        return params_copy

    @property
    def files(self):
        if hasattr(self._params['media']['content'], 'read'):
            return {self._params['media']['content'].name:
                (self._params['media']['content'].name, self._params['media']['content'])}
        return None

class PhotoReplacementContent(MediaReplacementContent):
    type_ = 'photo'

class MarkupReplacementContent(ReplacementContent):
    method = methods.editMessageReplyMarkup

#forward_message
#copy_message
#startPoll
#stopPoll
