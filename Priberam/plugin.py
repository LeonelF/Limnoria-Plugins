###
# Copyright (c) 2019, Pedro de Oliveira
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

from supybot import utils, plugins, ircutils, callbacks
from supybot.commands import *
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Priberam')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x
import urllib.parse
import re
import requests
from bs4 import BeautifulSoup


class Priberam(callbacks.Plugin):
    """Priberam dictionary client"""

    def __clean_str(self, text, clean_number=False):
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'(\[.*?]) (\1)', r'\1', text)
        text = re.sub(r'^\s+', '', text)
        if clean_number:
            text = re.sub(r'^\d+\. +', '', text)
        return text

    def find(self, irc, msg, args, word, position):
        """<word> [position]

        Returns the dictionary definition of a word.
        """
        response = requests.get(
            "https://dicionario.priberam.org/{}".format(urllib.parse.quote(word)),
            headers={'User-agent': 'Mozilla/5.0'}
            )
        soup = BeautifulSoup(response.content.decode('utf-8'))

        error = soup.find('div', {'class': 'alert alert-info'})
        if error:
            irc.reply(self.__clean_str(error.text), prefixNick=False)
            return

        definitions = soup.find('div', {'id': 'resultados'}).find_all('p')

        total = 0
        for idx in range(len(definitions)):
            if idx > 1 and self.__clean_str(definitions[idx].text)[:1].isdigit() is False:
                break
            total += 1
        if total == 0:
            irc.reply("Num encontrei nada no dicionário!", prefixNick=False)
            return
        if position > total:
            return

        definition = self.__clean_str(definitions[position - 1].text, True)
        
        irc.reply("[{}/{}] {}".format(position, total, definition), prefixNick=False)
    find = wrap(find, ['anything', optional('int', default=1)])


Class = Priberam


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79: