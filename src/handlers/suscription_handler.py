'''Update handlers for boes_bot.'''
from telegram import messages
from telegram import types


class SuscriptionHandler:
    def handles(self, update):
        if (update.type == types.CallbackQuery and
                update.content['data'].startswith(self.__class__.__name__)):
            return True
        if (update.type == types.Message and 
                update.content.is_command('/suscribirse')):
            return True
        if (update.type == types.Message and 
                update.content.is_command('/desuscribirse')):
            return True
        return False
    
    def __call__(self, update, token, dbname, dburi, sftphost, sftpuser, sftppass, sftp_cnopts=None):
        if (update.type == types.CallbackQuery):
            msg = messages.CaptionReplacementContent(
                message_id=update.content['message']['message_id'],
                caption='A partir de ahora *sí* recibirás el BOE automáticamente\\.',
                parse_mode='MarkdownV2',
                reply_markup='')
            msg.apply(token, update.content.cid, verbose=True)
        else:
            option = 'sí' if update.content.is_command('/suscribirse') else 'no'
            msg = messages.MessageContent(
                text=f'A partir de ahora *{option}* recibirás el BOE automáticamente\\.',
                parse_mode='MarkdownV2')
            msg.send(token, update.content.cid, verbose=True)
