'''Update handlers for boes_bot.'''
from telegram import messages
from telegram import types


class SearchHandler:
    def handles(self, update):
        if update.type != types.Message:
            return False
        if update.content.is_command('/buscar'):
            return True
        return False

    def __call__(self, update, token, dbname, dburi, sftphost, sftpuser, sftppass, sftp_cnopts=None):
        search_string = update.content["text"].split('/buscar')[1].strip()
        msg = messages.MessageContent(
            text=f'_Buscando_ {search_string} \\. \\. \\.',
            parse_mode='MarkdownV2')
        msg.send(token, update.content.cid, verbose=True)
