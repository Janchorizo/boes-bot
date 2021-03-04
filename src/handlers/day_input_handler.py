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
from handlers.day_handler import DayHandler

def get_arranged_buttons(year, month, bounds, fmt, fallback):
    c = calendar.TextCalendar()
    f_width = 3
    weeks = c.formatmonth(year, month, w=f_width).split('\n')[2:-1] # remove headers
    arranged_days = [
        [week[i*(f_width+1):i*(f_width+1)+(f_width+1)].strip() for i in range(7)]
        for week
        in weeks
    ]
    filtered_days = [
        [
            day if int(day) >= bounds[0] and int(day) <= bounds[1] else ''
            for day
            in week
        ]
        for week
        in arranged_days
    ]
    arranged_buttons = [
        [
            fallback if day == '' else {'text': day, 'callback_data': fmt.format(year, month, day)}
            for day
            in week
        ]
        for week
        in filtered_days
    ]
    return arranged_buttons


class DayInputHandler:
    collection = 'diary_summary'

    def handles(self, update):
        if update.type != types.CallbackQuery:
            return False
        if update.content['data'].startswith(self.__class__.__name__):
            return True
        return False

    def __call__(self, update, token, dbname, dburi, sftphost, sftpuser, sftppass, sftp_cnopts=None):
        fields = update.content['data'].split(':')
        field_count = len(fields) - 1
        year = None if field_count == 0 else int(fields[1])
        month = None if field_count < 2 else int(fields[2])

        client = MongoClient(dburi)
        db = client[dbname]
        cursor = db[self.collection].aggregate([
            {'$group': {'_id': '', 'max': {'$max': '$date'}, 'min': {'$min': '$date'}}}
        ])
        
        date_range = next(cursor)
        client.close()

        first_date = datetime.datetime(*map(int, date_range['min'].split('-')))
        last_date = datetime.datetime(*map(int, date_range['max'].split('-')))

        if field_count == 0: # select a year
            years = [*range(first_date.year, last_date.year+1)]
            caption = 'Selecciona el año que quieres consultar\\.'
            options = json.dumps({'inline_keyboard': [
                [{'text': y, 'callback_data': f'{DayInputHandler.__name__}:{y}'}
                    for y in years]
            ]})

        if field_count == 1: # select the month
            bounds = [1, 13]
            if year == first_date.year:
                bounds[0] = first_date.month
            if year == last_date.year:
                bounds[1] = last_date.month + 1
            
            months = tuple(range(*bounds))
            row_count = max(1, len(months)//3)
            arranged_months = []
            for i in range(row_count):
                left = 3 if i < row_count+1 else row_count%3
                arranged_months.append(months[i*3:i*3+left])

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
            bounds = [1, calendar.mdays[month]]
            if year == first_date.year and month == first_date.month:
                bounds[0] = first_date.day
            if year == last_date.year and month == last_date.month:
                bounds[1] = last_date.day

            fmt = DayHandler.__name__+':{}:{}:{}'
            fallback = {'text': ' ', 'callback_data': f'{DayInputHandler.__name__}:{year}:{month}'}
            
            caption = (f'Selecciona el día de *{calendar.month_name[month].capitalize()}*, *{year}*'
                        ' que quieres consultar\\.\n'
                        '_También puedes volver atrás para cambiar de mes_\\.')
            
            buttons = get_arranged_buttons(year, month, bounds, fmt, fallback)
            buttons.append([{'text': 'Atrás', 'callback_data': f'{DayInputHandler.__name__}:{year}'}])
            options = json.dumps({'inline_keyboard': buttons})
            
        
        msg = messages.CaptionReplacementContent(
                message_id=update.content['message']['message_id'],
                caption=caption,
                parse_mode='MarkdownV2',
                reply_markup=options)
        msg.apply(token, update.content.cid, verbose=True)
