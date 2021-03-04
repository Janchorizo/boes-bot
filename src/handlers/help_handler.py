'''Update handlers for boes_bot.'''
from telegram import messages
from telegram import types


help_text = (
    '@boes\\_bot recopila las entradas del [BOE](https://boe\\.es) para que puedas:\n\n'
    ' ❉ Ver resúmenes gráficos diarios del BOE\\.\n'
    ' ❉ Explorar interactivamente las secciones y departamentos\\.\n'
    ' ❉ Buscar entradas por texto\\.\n\n'
    '*¿Cómo usar el bot?*\n'
    'Puedes usar las opciones del menú:\n'
    ' ➥ Escribe @boes\\_bot ó /menu para ver las opciones\\.\n\n'
    'O ejecutar los comandos correspondientes:\n'
    ' ➥ El comando /suscribirse para recibir el BOE diariamente\\.\n'
    ' ➥ El comando /desuscribirse para cancelar la suscripción\\.\n'
    ' ➥ Usa el comando /buscar buscar en el BOE\\.\n\n'
    'Si el chat se te hace pequeño, prueba la [applicación web](boesbot\\.jancho\\.es)\\.\n\n'
    'Si quieres apoyar el proyecto puedes '
    '[pagarme un café en BuyMeACoffee](https://www\\.buymeacoffee\\.com/janchorizo)\\.\n\n'
    'Para ver otra vez este mensaje usa el comando /help\\.'
)


class HelpHandler:
    def handles(self, update):
        if update.type == types.Message:
            if update.content.is_command('/help') or update.content.is_command('/start'):
                return True
        return False
    
    def __call__(self, update, token, dbname, dburi, sftphost, sftpuser, sftppass, sftp_cnopts=None):
        with open(os.path.join(basedir, 'static/header.png'), 'rb') as p:
            start_msg = messages.PhotoContent(
                photo=p,
                parse_mode='MarkdownV2',
                caption=help_text)
            start_msg.send(token, update.content.cid, verbose=True)
