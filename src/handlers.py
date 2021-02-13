'''Update handlers for boes_bot.'''
import json

from telegram import messages
from telegram import types
from telegram import methods

class YesterdayHandler:
    def handles(self, update):
        if update.type != types.CallbackQuery:
            return False
        if update.content['data'] == self.__class__.__name__:
            return True
        return False
    
    def __call__(self, update, token):
        msg = messages.TextReplacementContent(
            message_id=update.content['message']['message_id'],
            text='Lo que pasó ayer en el *BOE* \\. \\. \\.',
            parse_mode='MarkdownV2')
        
        methods.answerCallbackQuery(
            token,
            params={'callback_query_id': update.content['id']},
            verbose=True)
        msg.apply(token, update.content.cid, verbose=True)


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
    [{'text': 'Ayer en el BOE', 'callback_data': YesterdayHandler.__name__}],
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
        return False
    
    def __call__(self, update, token):
        self.msg.send(token, update.content.cid, verbose=True)


class DefaultHandler:
    def handles(self, update):
        if hasattr(update.content, 'cid'):
            return True
    
    def __call__(self, update, token):
        with open('static/header.png', 'rb') as p:
            start_msg = messages.PhotoContent(
                photo=p,
                parse_mode='MarkdownV2',
                caption=
'''@boes\\_bot recopila las entradas del [BOE](https://boe\\.es) para que puedas:

 ❉ Ver resúmenes gráficos diarios del BOE\\.
 ❉ Explorar interactivamente las secciones y departamentos\\.
 ❉ Buscar entradas por texto\\.

*¿Cómo usar el bot?*
Puedes usar las opciones del menú:
➥ Escribe @boes\\_bot ó /menu para ver las opciones\\.

O ejecutar los comandos correspondientes:
➥ El comando /ultimo muestra el último BOE\\.
➥ El comando /otro\\_día permite elegir el BOE de otro día\\.
➥ Usa el comando /buscar buscar en el BOE\\.

Si el chat se te hace pequeño, prueba la [applicación web](boesbot\\.jancho\\.es)\\.

Si quieres apoyar el proyecto puedes [pagarme un café en BuyMeACoffee](https://www\\.buymeacoffee\\.com/janchorizo)\\.

Para ver otra vez este mensaje usa el comando /help\\.
''')
            start_msg.send(token, update.content.cid, verbose=True)


handlers = [
    DefaultHandler()
]

