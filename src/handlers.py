'''Update handlers for boes_bot.'''
import json

from telegram import messages
from telegram import types
from telegram import methods


class DayHandler:
    def handles(self, update):
        if update.type != types.CallbackQuery:
            return False
        if update.content['data'].startswith(self.__class__.__name__):
            return True
        return False

    def __call__(self, update, token):
        msg = messages.CaptionReplacementContent(
            message_id=update.content['message']['message_id'],
            caption='[TODO] ' + self.__class__.__name__,
            parse_mode='MarkdownV2',
            reply_markup='')
        msg.apply(token, update.content.cid, verbose=True)


class DayInputHandler:
    def handles(self, update):
        if update.type != types.CallbackQuery:
            return False
        if update.content['data'].startswith(self.__class__.__name__):
            return True
        return False

    def __call__(self, update, token):
        msg = messages.CaptionReplacementContent(
            message_id=update.content['message']['message_id'],
            caption='[TODO] ' + self.__class__.__name__,
            parse_mode='MarkdownV2',
            reply_markup='')
        msg.apply(token, update.content.cid, verbose=True)


class SearchButtonHandler:
    def handles(self, update):
        if update.type != types.CallbackQuery:
            return False
        if update.content['data'].startswith(self.__class__.__name__):
            return True
        return False

    def __call__(self, update, token):
        msg = messages.CaptionReplacementContent(
            message_id=update.content['message']['message_id'],
            caption='[TODO] ' + self.__class__.__name__,
            parse_mode='MarkdownV2',
            reply_markup='')
        msg.apply(token, update.content.cid, verbose=True)


class SuscriptionHandler:
    def handles(self, update):
        if update.type != types.CallbackQuery:
            return False
        if update.content['data'].startswith(self.__class__.__name__):
            return True
        return False
    
    def __call__(self, update, token):
        msg = messages.CaptionReplacementContent(
            message_id=update.content['message']['message_id'],
            caption='[TODO] ' + self.__class__.__name__,
            parse_mode='MarkdownV2',
            reply_markup='')
        msg.apply(token, update.content.cid, verbose=True)


help_text = (
    '@boes\\_bot recopila las entradas del [BOE](https://boe\\.es) para que puedas:\n\n'
    ' ❉ Ver resúmenes gráficos diarios del BOE\\.\n'
    ' ❉ Explorar interactivamente las secciones y departamentos\\.\n'
    ' ❉ Buscar entradas por texto\\.\n\n'
    '*¿Cómo usar el bot?*\n'
    'Puedes usar las opciones del menú:\n'
    ' ➥ Escribe @boes\\_bot ó /menu para ver las opciones\\.\n\n'
    'O ejecutar los comandos correspondientes:\n'
    ' ➥ El comando /ultimo muestra el último BOE\\.\n'
    ' ➥ El comando /otro\\_dia permite elegir el BOE de otro día\\.\n'
    ' ➥ Usa el comando /buscar buscar en el BOE\\.\n\n'
    'Si el chat se te hace pequeño, prueba la [applicación web](boesbot\\.jancho\\.es)\\.\n\n'
    'Si quieres apoyar el proyecto puedes '
    '[pagarme un café en BuyMeACoffee](https://www\\.buymeacoffee\\.com/janchorizo)\\.\n\n'
    'Para ver otra vez este mensaje usa el comando /help\\.'
)


class HelpHandler:
    def handles(self, update):
        if update.type == types.Message:
            if update.content.is_command('/help') or update.content.is_command('/start'):
                return True
        return False
    
    def __call__(self, update, token):
        with open('static/header.png', 'rb') as p:
            start_msg = messages.PhotoContent(
                photo=p,
                parse_mode='MarkdownV2',
                caption=help_text)
            start_msg.send(token, update.content.cid, verbose=True)


menu_text = (
    '@boes\\_bot recopila diariamente las entradas del [BOE](https://boe\\.es)\\. Puedes\n'
    'suscribirte para que te actualice aquí automáticamente\\.\n\n'
    'Si el chat se te hace pequeño, prueba la [applicación web](boesbot\\.jancho\\.es)\\.\n'
    'Puedes apoyar el proyecto en'
    '[pagarme un café en BuyMeACoffee](https://www\\.buymeacoffee\\.com/janchorizo)\\.'
)


menu_options = json.dumps({'inline_keyboard': [
    [{'text': 'Ver el último BOE', 'callback_data': DayHandler.__name__}],
    [{'text': 'Ver otro día', 'callback_data': DayInputHandler.__name__}],
    [{'text': 'Buscar en el BOE', 'callback_data': SearchButtonHandler.__name__}],
    [{'text': 'Suscribirse al BOE', 'callback_data': SuscriptionHandler.__name__}],
    ]})


class MenuHandler:
    def handles(self, update):
        if update.type == types.Message:
            if update.content.is_command('/menu') or update.content.mentions('@boes_bot'):
                return True
        return False
    
    def __call__(self, update, token):
        with open('static/header.png', 'rb') as p:
            start_msg = messages.PhotoContent(
                photo=p,
                parse_mode='MarkdownV2',
                caption=menu_text,
                reply_markup=menu_options)
            start_msg.send(token, update.content.cid, verbose=True)


handlers = [
    MenuHandler(),
    DayHandler(),
    DayInputHandler(),
    SearchButtonHandler(),
    SuscriptionHandler(),
    HelpHandler(),
]

