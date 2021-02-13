'''Content types.'''
from collections import UserDict


class Message(UserDict):
    def __init__(self, data):
        super().__init__(data)
        self.cid = self.data['chat']['id']

    def mentions(self, entity_id):
        if 'entities' not in self:
            return False

        mentioned_entities = tuple(
            self['text'][e['offset']: e['offset'] + e['length']]
            for e in self['entities']
            if e['type'] == 'mention'
        )

        return any(map(lambda mention: mention == entity_id, mentioned_entities))

class InlineQuery(UserDict):
    pass

class ChosenInlineResult(UserDict):
    pass

class CallbackQuery(UserDict):
    def __init__(self, data):
        super().__init__(data)
        self.cid = self.data['message']['chat']['id']

class ShippingQuery(UserDict):
    pass

class PreCheckoutQuery(UserDict):
    pass

class Poll(UserDict):
    pass

class PollAnswer(UserDict):
    pass

