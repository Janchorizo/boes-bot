'''Base classes for modelling methods and types.

This module is not intended to be used directly but through
the provided higher-level function.
'''
import json
import argparse
from collections import namedtuple
import functools
import requests
import termcolor


GET = 'GET'
POST = 'POST'


def get_api_endpoint(method:str, token:str) -> str:
    '''Returns an endpoint url if a valid method and token are provided.'''
    return f'https://api.telegram.org/bot{token}/{method}'

                                                                                                                 
def log_request(action:str, endpoint:str, params=None):
    msg_contents = [
        termcolor.colored('->', 'white', attrs=('bold',)),
        termcolor.colored(f'[{action}]', 'white', attrs=('bold',)),
        termcolor.colored(endpoint, 'cyan', attrs=('underline',)),
    ]
    print(' '.join(msg_contents))
    if params is not None:
        log_params(action, params)


def log_params(action:str, params: dict):
    msg_contents = [
        termcolor.colored(f'-- [{action}]', 'white', attrs=('bold',)),
        termcolor.colored(f'request params:', 'white'),
        '\n' + termcolor.colored(json.dumps(params, indent=1), 'cyan'),
    ]
    print(' '.join(msg_contents))


def build_doc(method_desc):
    '''Returns a formated class description.'''
    base_url = 'https://core.telegram.org/bots/api#'
    doc = '{}\nRequired parameters: \n\t{}\nOptional Parameters: \n\t{}\n{}'
    formatted = doc.format(
        method_desc.doc,
        '\n\t'.join(method_desc.required),
        '\n\t'.join(method_desc.optional),
        base_url + method_desc.method)
    return formatted


def log_response(action:str, r:requests.Response):
    status, content = r.status_code, r.content
    response_json = json.loads(content.decode())
    msg_contents = [
        termcolor.colored(f'<- [{status}]', 'white', attrs=('bold',)),
        termcolor.colored(f'{action} response content:', 'white'),
        '\n' + termcolor.colored(json.dumps(response_json, indent=1), 'cyan'),
    ]
    print(' '.join(msg_contents))


class Method:
    '''Base callable factory method for Telegram bot HTTP API.'''
    verb = GET
    method = 'undefined'
    required = tuple()
    default = tuple()
    optional = tuple()

    def __call__(self, token, *, params=None, files=None, verbose=False):
        endpoint = get_api_endpoint(self.method, token)
        if verbose:
            log_request(self.method, endpoint)

        if self.verb == GET:
            request = requests.get
        elif self.verb == POST:
            request = requests.post

        request = functools.partial(request, endpoint)
        if params is not None:
            request = functools.partial(request, data=params)
        if files is not None:
            request = functools.partial(request, files=files)
        r = request()

        if verbose:
            log_response(self.method, r)
        return r.status_code, r.content

    def __repr__(self):
        msg = '{}(token, params={{ {}{} }}, verbose=False)'

        name = self.__class__.__name__
        required_args = ', '.join(f'{arg}={val!r}' 
                         for arg, val
                         in zip(self.required, self.default))
        optional_args = ''
        if len(self.optional) > 0:
            optional_args = '[,{}]'.format(', '.join(self.optional))
        return msg.format(name, required_args, optional_args)

    def get_def_parameters(self):
        '''Returns a dict object with the default values set for
           the required args.'''
        return dict(zip(self.required, self.default))


MethodDesc = namedtuple('MethodDesc', 'verb method required default optional doc')


def method_factory(desc:MethodDesc) -> Method:
    '''Returns a subclass of Method to be used a an HTTP endpoint.'''
    if desc.verb not in (GET, POST):
        raise ValueError(f'{dic.verb} is not a valid ({GET} {POST}) HTTP verb.')

    dic = {
        'verb': desc.verb,
        'method': desc.method,
        'required': desc.required,
        'default': desc.default,
        'optional': desc.optional,
    }
    cls = type(desc.method, (Method,), dic)
    cls.__doc__ = build_doc(desc)
    return cls
