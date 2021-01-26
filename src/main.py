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


MAX_CONNECTIONS = 10
DEFAULT_PORT = 80


async def get_body_dict(request):
    if request.body_exists and request.can_read_body:
        raw_body = b''
        async for line in request.content:
            raw_body += line
        try:
            d = json.loads(raw_body.decode())
        except Exception:
            return None
        else:
            return d
    else:
        return None

global_options_text = '''
@boes\_bot te permite seguir la actividad del gobierno de forma sencilla\\.

Todos los días se procesan las leyes publicadas en el BOE el día anterior
y se proporcionan como resúmenes sencillos\\. También puedes ver resúmenes
semanales y _perlas que aparecen en el BOE_ y que te pueden resultar interesantes\\.

Puedes votar cada paquete dirario de leyes y ver resultados pasados\\. Como
ciudadano estás en tu derecho de conocer y opinar sobre las leyes que se
crean\\.

Para más información visita [https://boesbot\\.jancho\\.es](https://boes\\.jancho\\.es)
'''

global_options = json.dumps({'inline_keyboard': [
    [{'text': 'Ayer en el BOE', 'callback_data': 'ayer'}],
    [{'text': 'Resumen semanal', 'callback_data': 'semanal'}],
    [{'text': 'Perlas en el BOE', 'callback_data': 'perlas'}],
    [{'text': 'Cuestionarios', 'callback_data': 'cuestionarios'}],
    ]})

class MentionHandler:
    msg = messages.MessageContent(text=global_options_text, parse_mode='MarkdownV2', reply_markup=global_options)

    def handles(self, update):
        if update.type != types.Message:
            return False
        if hasattr(update.content, 'mentions') and update.content.mentions('@boes_bot'):
            return True
    
    def __call__(self, update, token):
        self.msg.send(token, update.content.cid, verbose=True)


class DefaultHandler:
    def handles(self, update):
        if hasattr(update.content, 'cid'):
            return True
    
    def __call__(self, update, token):
        msg = messages.MessageContent(text=f'[{update.id}] Received a *{update.field_name}*', parse_mode='MarkdownV2')
        msg.send(token, update.content.cid, verbose=True)


handlers = [
    MentionHandler(),
    DefaultHandler()
]


async def handle_query(request):
    print(f'<- {request.host}')
    body = await get_body_dict(request)

    if body is None:
        print('{!r} [ERROR]'.format(request))
        raise web.HTTPNotFound()

    token = request.config_dict['token']
    update = content.Update(body)
    for handler in handlers:
        if handler.handles(update):
            handler(update, token)
            break
    return web.Response(text='ok')
    

async def healthy(request):
    return web.json_response({'healty': True})


def init(token):
    app = web.Application()
    app.add_routes([
        web.get('/healthy', healthy),
        web.post(f'/{token}', handle_query)])
    app['token'] = token
    return app


def main(token, address, port, pubkey, privkey, **kwargs):
    if token is None or len(token) == 0:
        raise ValueError('A valid Telegram bot token must be specified.')
    if len(address) == 0:
        raise ValueError('Address must be specified.')

    with admin.Webhook(token, url=f'https://{address}:{port}/{token}', max_connections=MAX_CONNECTIONS,
            drop_pending_updates=True) as wb:
        app = init(token)
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain(pubkey, privkey)
        web.run_app(app, port=port, ssl_context=ssl_ctx)


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
        '--pubkey',
        type=str,
        help='Public key')

    parser.add_argument(
        '--privkey',
        type=str,
        help='Private key')

    params = parser.parse_args()
    return {
        'token': params.token,
        'address': params.address,
        'port': params.port,
        'pubkey': params.pubkey,
        'privkey': params.privkey,
    }


if __name__ == '__main__':
    params = getOptions(DEFAULT_PORT)
    main(**params)

