'''Telegram bot implementation for BOE information retrieval.'''
import argparse
import asyncio
import json
import ssl
import os

from aiohttp import web

from telegram import admin
from telegram import content
from telegram import types
from telegram import messages
from handlers import handlers


MAX_CONNECTIONS = 10
DEFAULT_PORT = 80


async def get_body_dict(request):
    if request.body_exists and request.can_read_body:
        raw_body = b''
        async for line in request.content:
            raw_body += line
        try:
            d = json.loads(raw_body.decode('utf8'))
        except Exception:
            return None
        else:
            return d
    else:
        return None


async def handle_query(request):
    token = request.config_dict['token']
    dbname = request.config_dict['dbname']
    dburi = request.config_dict['dburi']

    print(f'<- {request.host}')
    body = await get_body_dict(request)

    if body is None:
        print('{!r} [ERROR]'.format(request))
        raise web.HTTPNotFound()

    update = content.Update(body)
    for handler in handlers:
        if handler.handles(update):
            print(f'Request handled by {handler.__class__.__name__}')
            handler(update, token, dbname=dbname, dburi=dburi)
            break
    return web.Response(text='ok')
    

async def healthy(request):
    return web.json_response({'healty': True})


def init(token, dburi, dbname):
    app = web.Application()
    app.add_routes([
        web.get('/healthy', healthy),
        web.post(f'/{token}', handle_query)])
    app['token'] = token
    app['dburi'] = dburi
    app['dbname'] = dbname
    return app


def main(token, address, port, pubkey, privkey, dburi, dbname, **kwargs):
    if token is None or len(token) == 0:
        raise ValueError('A valid Telegram bot token must be specified.')
    if len(address) == 0:
        raise ValueError('Address must be specified.')

    with admin.Webhook(token, url=f'https://{address}/{token}', max_connections=MAX_CONNECTIONS,
            drop_pending_updates=True) as wb:
        app = init(token, dburi, dbname)
        web.run_app(app, port=port)


def getOptions(def_port):
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        '-t',
        '--token',
        type=str,
        help='Bot private token.')

    parser.add_argument(
        '-a',
        '--address',
        type=str,
        help='Address to listen.',
        default='')

    parser.add_argument(
        '-p',
        '--port',
        type=str,
        help='What port to listen.',
        default=def_port)

    parser.add_argument(
        '--dburi',
        type=str,
        help='Public key')

    parser.add_argument(
        '--dbname',
        type=str,
        help='Private key')

    params = parser.parse_args()
    return {
        'token': params.token,
        'address': params.address,
        'port': params.port,
        'pubkey': params.pubkey,
        'privkey': params.privkey,
        'dburi': params.dbui,
        'dbname': params.dbname
    }


if __name__ == '__main__':
    params = getOptions(DEFAULT_PORT)
    main(**params)

