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

class DayHandler:
    collection = 'diary_summary'

    def handles(self, update):
        if update.type != types.CallbackQuery:
            return False
        if update.content['data'].startswith(self.__class__.__name__):
            return True
        return False

    def __call__(self, update, token, dbname, dburi, sftphost, sftpuser, sftppass, sftp_cnopts=None):
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
                        password=sftppass,
                        cnopts=sftp_cnopts) as sftp:
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
