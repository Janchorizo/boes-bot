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


basedir = os.path.realpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
)

def create_menu_options(day, month, year):
    options = [
        [{
            'text': 'Volver al resumen del diario',
            'callback_data': f'DayHandler:{year}:{month}:{day}'
        }]
    ]
    return json.dumps({'inline_keyboard': options})

class SectionHandler:
    collection = 'diary_section_summary'

    def handles(self, update):
        if update.type != types.CallbackQuery:
            return False
        if update.content['data'].startswith(self.__class__.__name__):
            return True
        return False

    def __call__(self, update, token, dbname, dburi, sftphost, sftpuser, sftppass, sftp_cnopts=None):
        year, month, day, section = update.content['data'].split(':')[1:]
        year, month, day = int(year), int(month), int(day)
        date = datetime.datetime(year, month, day)
        formatted_date = '{:%Y-%m-%d}'.format(date)

        client = MongoClient(dburi)
        db = client[dbname]
        summary = db[self.collection].find_one({'date': formatted_date, 'section': section})
        
        if summary == None:
            client.close()
            return
        
        caption = (
            f'Se registraron un total de {summary["entry_count"]} en la sección "{section}" del'
            f' Boletín del día *{day} de {calendar.month_name[month].capitalize()}, {year}*\\.'
        )

        if summary['summary_graphic']['telegram_id'] != '':
            msg = messages.PhotoReplacementContent(
                message_id=update.content['message']['message_id'],
                reply_markup=create_menu_options(day, month, year),
                media={
                    'content': summary['summary_graphic']['telegram_id'],
                    'caption': caption,
                    'parse_mode': 'MarkdownV2',
                })
            msg.apply(token, update.content.cid, verbose=True)
        else:
            local_path = os.path.basename(summary['summary_graphic']['sftp_file'])
            if not os.path.exists(local_path):
                with pysftp.Connection(
                        sftphost,
                        username=sftpuser,
                        password=sftppass,
                        cnopts=sftp_cnopts) as sftp:
                    sftp.get(
                        summary['summary_graphic']['sftp_file'],
                        local_path)
            with open(local_path, 'rb') as f:
                msg = messages.PhotoReplacementContent(
                    message_id=update.content['message']['message_id'],
                    reply_markup=create_menu_options(day, month, year),
                    media={
                        'content': f,
                        'caption': caption,
                        'parse_mode': 'MarkdownV2',
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

