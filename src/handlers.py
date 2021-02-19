'''Update handlers for boes_bot.'''
import os
import datetime, calendar
import locale
import json

from telegram import messages
from telegram import types
from telegram import methods


locale.setlocale(locale.LC_ALL,"es_ES.UTF-8")


basedir = os.path.dirname(os.path.abspath(__file__))


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
            caption='[TODO] ' + update.content['data'],
            parse_mode='MarkdownV2',
            reply_markup='')
        msg.apply(token, update.content.cid, verbose=True)


def get_arranged_buttons(year, month, fmt, fallback):
    c = calendar.TextCalendar()
    f_width = 3
    weeks = c.formatmonth(year, month, w=f_width).split('\n')[2:-1] # remove headers
    arranged_days = [
        [week[i*(f_width+1):i*(f_width+1)+(f_width+1)].strip() for i in range(7)]
        for week
        in weeks
    ]
    arranged_buttons = [
        [
            fallback if day == '' else {'text': day, 'callback_data': fmt.format(year, month, day)}
            for day
            in week
        ]
        for week
        in arranged_days
    ]
    return arranged_buttons


class DayInputHandler:
    def handles(self, update):
        if update.type != types.CallbackQuery:
            return False
        if update.content['data'].startswith(self.__class__.__name__):
            return True
        return False

    def __call__(self, update, token):
        fields = update.content['data'].split(':')
        field_count = len(fields) - 1
        year = None if field_count == 0 else int(fields[1])
        month = None if field_count < 2 else int(fields[2])

        if field_count == 0: # select a year
            years = (2021,)
            caption = 'Selecciona el año que quieres consultar\\.'
            options = json.dumps({'inline_keyboard': [
                [{'text': y, 'callback_data': f'{DayInputHandler.__name__}:{y}'}
                    for y in years]
            ]})

        if field_count == 1: # select the month
            months = tuple(range(1,13))
            arranged_months = [months[i*3:i*3+3] for i in range(len(months)//3)]
            caption = (f'Selecciona el mes de *{year}* que quieres consultar\\.\n'
                        '_También puedes volver atrás para cambiar de año_\\.')
            options = json.dumps({'inline_keyboard': [
                *[[{
                    'text': calendar.month_name[m].capitalize(),
                    'callback_data': f'{DayInputHandler.__name__}:{year}:{m}'
                  } for m in row]
                for row in arranged_months],
                [{'text': 'Atrás', 'callback_data': DayInputHandler.__name__}]
            ]})
            

        if field_count == 2: # select the day
            fmt = DayHandler.__name__+':{}:{}:{}'
            fallback = {'text': ' ', 'callback_data': f'{DayInputHandler.__name__}:{year}:{month}'}
            
            caption = (f'Selecciona el día de *{calendar.month_name[month].capitalize()}*, *{year}*'
                        ' que quieres consultar\\.\n'
                        '_También puedes volver atrás para cambiar de mes_\\.')
            
            buttons = get_arranged_buttons(year, month, fmt, fallback)
            buttons.append([{'text': 'Atrás', 'callback_data': f'{DayInputHandler.__name__}:{year}'}])
            options = json.dumps({'inline_keyboard': buttons})
            
        
        msg = messages.CaptionReplacementContent(
                message_id=update.content['message']['message_id'],
                caption=caption,
                parse_mode='MarkdownV2',
                reply_markup=options)
        msg.apply(token, update.content.cid, verbose=True)


class SearchHandler:
    def handles(self, update):
        if update.type != types.Message:
            return False
        if update.content.is_command('/buscar'):
            return True
        return False

    def __call__(self, update, token):
        search_string = update.content["text"].split('/buscar')[1].strip()
        msg = messages.MessageContent(
            text=f'_Buscando_ {search_string} \\. \\. \\.',
            parse_mode='MarkdownV2')
        msg.send(token, update.content.cid, verbose=True)


class SuscriptionHandler:
    def handles(self, update):
        if (update.type == types.CallbackQuery and
                update.content['data'].startswith(self.__class__.__name__)):
            return True
        if (update.type == types.Message and 
                update.content.is_command('/suscribirse')):
            return True
        if (update.type == types.Message and 
                update.content.is_command('/desuscribirse')):
            return True
        return False
    
    def __call__(self, update, token):
        if (update.type == types.CallbackQuery):
            msg = messages.CaptionReplacementContent(
                message_id=update.content['message']['message_id'],
                caption='A partir de ahora *sí* recibirás el BOE automáticamente\\.',
                parse_mode='MarkdownV2',
                reply_markup='')
            msg.apply(token, update.content.cid, verbose=True)
        else:
            option = 'sí' if update.content.is_command('/suscribirse') else 'no'
            msg = messages.MessageContent(
                text=f'A partir de ahora *{option}* recibirás el BOE automáticamente\\.',
                parse_mode='MarkdownV2')
            msg.send(token, update.content.cid, verbose=True)


help_text = (
    '@boes\\_bot recopila las entradas del [BOE](https://boe\\.es) para que puedas:\n\n'
    ' ❉ Ver resúmenes gráficos diarios del BOE\\.\n'
    ' ❉ Explorar interactivamente las secciones y departamentos\\.\n'
    ' ❉ Buscar entradas por texto\\.\n\n'
    '*¿Cómo usar el bot?*\n'
    'Puedes usar las opciones del menú:\n'
    ' ➥ Escribe @boes\\_bot ó /menu para ver las opciones\\.\n\n'
    'O ejecutar los comandos correspondientes:\n'
    ' ➥ El comando /suscribirse para recibir el BOE diariamente\\.\n'
    ' ➥ El comando /desuscribirse para cancelar la suscripción\\.\n'
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
        with open(os.path.join(basedir, 'static/header.png'), 'rb') as p:
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
    [{'text': 'Buscar en el BOE', 'switch_inline_query_current_chat': '/buscar '}],
    [{'text': 'Suscribirse al BOE', 'callback_data': SuscriptionHandler.__name__}],
    ]})


class MenuHandler:
    def handles(self, update):
        if update.type == types.Message:
            if update.content.is_command('/menu') or update.content.mentions('@boes_bot'):
                return True
        return False
    
    def __call__(self, update, token):
        with open(os.path.join(basedir, 'static/header.png'), 'rb') as p:
            start_msg = messages.PhotoContent(
                photo=p,
                parse_mode='MarkdownV2',
                caption=menu_text,
                reply_markup=menu_options)
            start_msg.send(token, update.content.cid, verbose=True)


handlers = [
    DayHandler(),
    DayInputHandler(),
    SearchHandler(),
    SuscriptionHandler(),
    MenuHandler(),
    HelpHandler(),
]

