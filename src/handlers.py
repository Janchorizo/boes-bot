'''Update handlers for boes_bot.'''
import os
import datetime, calendar
import locale
import json

import pymongo
import pysftp
from pymongo import MongoClient

from telegram import messages
from telegram import types
from telegram import methods


locale.setlocale(locale.LC_ALL,"es_ES.UTF-8")


basedir = os.path.dirname(os.path.abspath(__file__))


class DayHandler:
    collection = 'diary_summary'

    def handles(self, update):
        if update.type != types.CallbackQuery:
            return False
        if update.content['data'].startswith(self.__class__.__name__):
            return True
        return False

    def __call__(self, update, token, dbname, dburi, sftphost, sftpuser, sftppass):
        year, month, day = update.content['data'].split(':')[1:]
        year, month, day = int(year), int(month), int(day)
        date = datetime.datetime(year, month, day)
        formatted_date = '{:%Y-%m-%d}'.format(date)

        client = MongoClient(dburi)
        db = client[dbname]
        summary = db[self.collection].find_one({'date': formatted_date})
        
        if summary == None:
            client.close()
            return
        
        formatted_link = summary["link"]\
            .replace(".", "\\.")\
            .replace('=', '\\=')\
            .replace('-', '\\-')\
            .replace('_', '\\_')
        formatted_entry_types = '\n'.join(
            f'◇ {c} entradas son {t}'
            for t, c
            in summary["per_type_def_count"].items()
            if t != ''
        )

        caption = (
            f'Boletín del día *{day} de {calendar.month_name[month].capitalize()}, {year}*\\.'
            f'Accesible en {formatted_link}\\.\n\n'
            f'Se registraron un total de {summary["entry_count"]} entradas, de las cuales:\n'
            f'{formatted_entry_types}'
        )

        if summary['summary_graphic']['telegram_id'] != '':
            msg = messages.PhotoReplacementContent(
                message_id=update.content['message']['message_id'],
                reply_markup='{}',
                media={
                    'content': summary['summary_graphic']['telegram_id'],
                    'caption': caption,
                    'parse_mode': 'MarkdownV2',
                    'reply_markup': ''
                })
            msg.apply(token, update.content.cid, verbose=True)
        else:
            local_path = os.path.basename(summary['summary_graphic']['sftp_file'])
            if not os.path.exists(local_path):
                with pysftp.Connection(
                        sftphost,
                        username=sftpuser,
                        password=sftppass) as sftp:
                    sftp.get(
                        summary['summary_graphic']['sftp_file'],
                        local_path)
            with open(local_path, 'rb') as f:
                msg = messages.PhotoReplacementContent(
                    message_id=update.content['message']['message_id'],
                    reply_markup='{}',
                    media={
                        'content': f,
                        'caption': caption,
                        'parse_mode': 'MarkdownV2',
                        'reply_markup': ''
                    })
                status, res = msg.apply(token, update.content.cid, verbose=True)
            
            if status == 200 and res['ok'] == True:
                photo, thumbnail = res['result']['photo'][-2:]
                photo_id = photo['file_id']
                result = db[self.collection].update_one(
                    {'date': formatted_date},
                    {'$set': {'summary_graphic.telegram_id': photo_id}}
                )
                client.close()
                if result.modified_count == 1:
                    os.remove(local_path)


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

    def __call__(self, update, token, dbname, dburi, sftphost, sftpuser, sftppass):
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

    def __call__(self, update, token, dbname, dburi, sftphost, sftpuser, sftppass):
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
    
    def __call__(self, update, token, dbname, dburi, sftphost, sftpuser, sftppass):
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
    
    def __call__(self, update, token, dbname, dburi, sftphost, sftpuser, sftppass):
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


menu_options = lambda last_day: json.dumps({'inline_keyboard': [
    [{'text': f'Ver el último BOE ({last_day:%d/%m/%Y})', 'callback_data': f'{DayHandler.__name__}:{last_day:%Y:%m:%d}'}],
    [{'text': 'Ver otro día', 'callback_data': DayInputHandler.__name__}],
    [{'text': 'Buscar en el BOE', 'switch_inline_query_current_chat': '/buscar '}],
    [{'text': 'Suscribirse al BOE', 'callback_data': SuscriptionHandler.__name__}],
    ]})


class MenuHandler:
    collection = 'diary_summary'

    def handles(self, update):
        if update.type == types.Message:
            if update.content.is_command('/menu') or update.content.mentions('@boes_bot'):
                return True
        return False
    
    def __call__(self, update, token, dbname, dburi, sftphost, sftpuser, sftppass):
        client = MongoClient(dburi)
        db = client[dbname]
        cursor = db[self.collection].find({}, {'date': 1})\
            .sort([('date', pymongo.DESCENDING)])\
            .limit(1)
        
        year, month, day = next(cursor)['date'].split('-')
        year, month, day = int(year), int(month), int(day)
        last_day = datetime.datetime(year, month, day)
        client.close()

        with open(os.path.join(basedir, 'static/header.png'), 'rb') as p:
            start_msg = messages.PhotoContent(
                photo=p,
                parse_mode='MarkdownV2',
                caption=menu_text,
                reply_markup=menu_options(last_day))
            start_msg.send(token, update.content.cid, verbose=True)


handlers = [
    DayHandler(),
    DayInputHandler(),
    SearchHandler(),
    SuscriptionHandler(),
    MenuHandler(),
    HelpHandler(),
]

