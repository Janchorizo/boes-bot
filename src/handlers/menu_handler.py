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
from handlers.day_input_handler import DayInputHandler
from handlers.day_handler import DayHandler
from handlers.suscription_handler import SuscriptionHandler

basedir = os.path.realpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
)
locale.setlocale(locale.LC_ALL,"es_ES.UTF-8")

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
    
    def __call__(self, update, token, dbname, dburi, sftphost, sftpuser, sftppass, sftp_cnopts=None):
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
