'''Telegram bot implementation for BOE information retrieval.'''
from telegram import admin

import os
import sys
import json
import argparse
import functools
import time
import asyncio
from aiohttp import web


DEFAUT_MAX_CONNECTIONS = 2
DEFAULT_PORT = 80


async def handle_query(request):
    print(request)
    res = web.json_response({'ok': True})
    if res == None:
        print('{!r} [ERROR]'.format(request))
        raise web.HTTPNotFound()

    print('{!r} [OK]'.format(request))
    return res


def init(token):
    app = web.Application()
    app.add_routes([
        web.get('/', handle_query),
        web.post('/', handle_query)])
    return app


def main(token, address, ip, port, certificate, max_connections):
    if token is None or len(token) == 0:
        raise ValueError('A valid Telegram bot token must be specified.')
    if ip is not None and len(address) > 0:
        raise ValueError('Only address or fixed IP can be specified.')
    if ip is None and len(address) == 0:
        raise ValueError('Address or IP must be specified.')
    bind = ip if ip and len(ip) > 0 else address
    print(token, bind, port, certificate, max_connections)
    #with admin.Webhook(token) as wb:
    app = init(token)
    web.run_app(app, host=bind, port=port)


def getOptions(def_port, def_max_connections):
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
            '-i',
            '--ip',
            type=str,
            help='Destination folder for meta-data.')

    parser.add_argument(
            '-p',
            '--port',
            type=str,
            help='What port to listen.',
            default=def_port)

    parser.add_argument(
            '-c',
            '--certificate',
            type=str,
            help='Destination folder for images.')

    parser.add_argument(
            '-m',
            '--max-connections',
            type=str,
            help='What address to bind to.',
            default=def_max_connections)

    params = parser.parse_args()
    return (
        params.token,
        params.address,
        params.ip,
        params.port,
        params.certificate,
        params.max_connections)


if __name__ == '__main__':
    token, address, ip, port, certificate, max_connections = getOptions(
        DEFAULT_PORT,
        DEFAUT_MAX_CONNECTIONS)
    main(token, address, ip, port, certificate, max_connections)
