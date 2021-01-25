'''Higher-level functions for Telegram bot administration.'''
import os
import json
import termcolor
from . import methods


ALLOWED_PORTS = (443, 80, 88, 8443)


def get_bot_info(token:str, verbose:bool=False):
    '''Get basic bot info to test the connection.'''
    status, info = methods.getMe(token, verbose=verbose)
    return status, info


def log_out(token:str, verbose:bool=False):
    '''Use this method to log out from the cloud Bot API server before
    launching the bot locally. You must log out the bot before running
    it locally, otherwise there is no guarantee that the bot will receive
    updates. After a successful call, you can immediately log in on a local
    server, but will not be able to log in back to the cloud Bot API server
    for 10 minutes. Returns True on success. Requires no parameters.
    '''
    status, _ = methods.logOut(token, verbose=verbose)
    return status, None


def close(token:str, verbose:bool=False):
    '''Use this method to close the bot instance before moving it from
    one local server to another. You need to delete the webhook before
    calling this method to ensure that the bot isn't launched again after
    server restart. The method will return error 429 in the first 10 minutes
    after the bot is launched. Returns True on success. Requires no parameters.
    '''
    status, _ = methods.close(token, verbose=verbose)
    return status, None

def get_commands(token:str, verbose:bool=False):
    '''Retrieve current commands for the specified bot.'''
    status, commands = methods.getMyCommands(token, verbose=verbose)
    return status, commands


def set_commands(token:str, commands, verbose:bool=False):
    '''Sets the commands on the specified bot to be
    provided iterable of tuples (<command>, <description>).
    '''
    try:
        commands_dict = [{'command': c, 'description': d} for c, d in commands]
        commands_json = json.dumps(commands_dict)
    except ValueError as e:
        print(e)
    else:
        status, _ = methods.setMyCommands(
            token,
            params={'commands': commands_json},
            verbose=verbose)
        return status, None


def set_webhook(
        token:str,
        url,
        certificate=None,
        ip_address=None,
        max_connections=40,
        allowed_updates=None,
        drop_pending_updates=False,
        verbose=False):
    '''Set a webhook for the specified bot.'''
    params = {
        'url': url,
        'max_connections': max_connections,
        'drop_pending_updates': drop_pending_updates
    }

    if ip_address is not None:
        params['ip_address'] = ip_address

    if allowed_updates is not None:
        params['allowed_updates'] = allowed_updates

    if drop_pending_updates is not None:
        params['drop_pending_updates'] = drop_pending_updates

    files = None
    if certificate is not None:
        if hasattr(certificate, 'read'):
            files = {'certificate': certificate}
        else:
            params['certificate'] = certificate
        
    print(params)
    status, info = methods.setWebhook(
        token,
        params=params,
        files=files,
        verbose=verbose)
    return status, info


def get_webhook(token:str, verbose=False):
    '''Retrieve the webhook configuration.'''
    status, info = methods.getWebhookInfo(token, verbose=verbose)
    return status, info


def remove_webhook(token:str, drop_pending_updates=False, verbose=False):
    '''Remove the webhook configuration.'''
    params = {'drop_pending_updates': drop_pending_updates}
    status, info = methods.deleteWebhook(token, params=params, verbose=verbose)
    return status, info 


def get_updates(token:str, verbose=False):
    '''Returns a list of bot updates.'''
    status, updates = methods.getUpdates(token, verbose=verbose)
    return status, updates


class Webhook:
    '''Provides setup and taredown of the bot webhook as
    a context manager.
    '''
    def __init__(
            self,
            token,
            url,
            certificate=None,
            ip_address=None,
            max_connections=40,
            allowed_updates=None,
            drop_pending_updates=False):
        self.token = token
        self.url = ip_address if ip_address is not None and len(ip_address) > 0 else url
        self.certificate = certificate
        self.ip_address = ip_address
        self.max_connections = max_connections
        self.allowed_updates = allowed_updates
        self.drop_pending_updates = drop_pending_updates
        self.status = None
    
    def __enter__(self):
        dest = self.ip_address if self.ip_address and len(self.ip_address) > 0 else self.url
        msg_contents = [
            termcolor.colored('-> Setting webhook ', 'white', attrs=('bold',)),
            termcolor.colored(f'[{dest}]', 'white', attrs=('bold',)),
            termcolor.colored(f'for bot {self.token}', 'cyan'),
        ]
        print(' '.join(msg_contents))

        if self.certificate and os.path.isfile(self.certificate):
            with open(self.certificate, 'rb') as cf:
                status, _ = set_webhook(
                    self.token,
                    self.url,
                    certificate=cf,
                    ip_address=self.ip_address,
                    max_connections=self.max_connections,
                    allowed_updates=self.allowed_updates,
                    drop_pending_updates=self.drop_pending_updates,
                    verbose=True)
        else:
            status, _ = set_webhook(
                self.token,
                self.url,
                ip_address=self.ip_address,
                max_connections=self.max_connections,
                allowed_updates=self.allowed_updates,
                drop_pending_updates=self.drop_pending_updates,
                verbose=True)
        self.status = status
        
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        dest = self.ip_address if self.ip_address and len(self.ip_address) > 0 else self.url
        msg_contents = [
            termcolor.colored('-> Removing webhook ', 'white', attrs=('bold',)),
            termcolor.colored(f'[{dest}]', 'white', attrs=('bold',)),
            termcolor.colored(f'for bot {self.token}', 'cyan', attrs=('underline',)),
        ]
        print(' '.join(msg_contents))
        status, _ = remove_webhook(self.token, self.drop_pending_updates, verbose=True)
