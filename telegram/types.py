'''Content types.'''

class Content:
    def __init__(self, data):
        self._data = data
    
    def __getitem__(self, key):
        if key not in self._data:
            raise KeyError()
        else:
            return self._data[key]
    
    def __setitem__(self, key, value):
        raise KeyError(f"Can't set value for {key}")

class Message(Content):
    def __init__(self, data):
        super().__init__(self, data)
        self.cid = self._data['chat']['id']

    def mentions(self, id):
        mentioned_entities = (
            self._data['text'].slice(e['offset'], e['length'])
            for e in self._data['entities']
            if e['type'] == 'mention'
        )

        return any(map(lambda mention: mention == id, mentioned_entities))

class InlineQuery(Content):

class ChosenInlineResult(Content):

class CallbackQuery(Content):
    def __init__(self, data):
        super().__init__(self, data)
        self.cid = self._data['message']['chat']['id']

class ShippingQuery(Content):

class PreCheckoutQuery(Content):

class Poll(Content):

class PollAnswer(Content):
