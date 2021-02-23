'''Telegram bot implementation for BOE information retrieval using long-term polling.'''
import argparse
import requests
import signal
import time
import json
import os

from telegram import admin
from telegram import content
from telegram import types
from telegram import messages
from handlers import handlers


def handle_update(update, token, dburi, dbname, sftphost, sftpuser, sftppass):
    print(f'<- Update [{update.id}]')

    for handler in handlers:
        if handler.handles(update):
            try:
                handler(update,
                        token,
                        dbname=dbname,
                        dburi=dburi,
                        sftphost=sftphost,
                        sftpuser=sftpuser,
                        sftppass=sftppass)
            except Exception as e:
                print(f'ERROR: {e}')
            break
    

def main(token, dburi, dbname, sftphost, sftpuser, sftppass, **kwargs):
    if token is None or len(token) == 0:
        raise ValueError('A valid Telegram bot token must be specified.')

    def handle_break(*args):
        print('Stopping the bot ...')
        global stopped
        handle_break.called = True
    handle_break.called = False
    signal.signal(signal.SIGINT, handle_break)

    print('Running bot ... \npress [CTRL+C] to stop')
    offset = None
    while not handle_break.called:
        status, updates = content.get_updates(token, offset)
        for update in updates:
            handle_update(update, token, dburi, dbname, sftphost, sftpuser, sftppass)
            offset = update.id + 1
        time.sleep(.1)
        

def getOptions():
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        '-t',
        '--token',
        type=str,
        help='Bot private token.')

    parser.add_argument(
        '--dburi',
        type=str,
        help='Public key')

    parser.add_argument(
        '--dbname',
        type=str,
        help='Private key')

    parser.add_argument(
        '--sftpuser',
        type=str,
        help='Public key')

    parser.add_argument(
        '--sftppass',
        type=str,
        help='Private key')

    parser.add_argument(
        '--sftphost',
        type=str,
        help='Private key')

    params = parser.parse_args()
    return {
        'token': params.token,
        'dburi': params.dburi,
        'dbname': params.dbname,
        'sftphost': params.sftphost,
        'sftpuser': params.sftpuser,
        'sftppass': params.sftppass,
    }


if __name__ == '__main__':
    params = getOptions()
    main(**params)
