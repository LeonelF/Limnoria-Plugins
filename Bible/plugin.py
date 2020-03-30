###
# Copyright (c) 2017, Leonel Faria
# All rights reserved.

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
import json
import sys
import re
import emoji
import urllib.request
from urllib.request import urlopen, HTTPError, URLError
from socket import timeout

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks


try:
	from supybot.i18n import PluginInternationalization
	_ = PluginInternationalization('Bible')
except ImportError:
	# Placeholder that allows to run the plugin on a bot
	# without the i18n module
	_ = lambda x: x


class Bible(callbacks.Plugin):
	"""Fetch random bible verse from Ourmanna.com API"""
	pass

	def bible(self, irc, msg, args, argv):
		"""<location>

		Returns a random bible verse.
		"""
		transkey = 'yandex.translate.key'		
		url = 'https://beta.ourmanna.com/api/v1/get/?format=json&order=random'

		req = urllib.request.Request(
    		url, 
    		data=None, 
    		headers={
        		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    		}
		)

		try:
			response = urlopen(req, timeout=5)
		except (HTTPError, URLError) as error:
			irc.error("Data not retrieved because {}".format(str(error.reason)))
			return
		except timeout:
			irc.error('Socket timed out, please try again later') 
			return
		values = json.loads(response.read().decode('utf-8'))
		if values is None:
			irc.reply("No results found")
			return
		else:
			verse = values['verse']['details']['text']
			verse = urllib.parse.quote(verse)
			
			
			url2 = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key={0}&text={1}&lang=en-pt'.format(transkey, verse)
			
			req2 = urllib.request.Request(
    			url2, 
    			data=None, 
    			headers={
        			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    			}
			)
			try:
				response2 = urlopen(req2, timeout=5)
			except (HTTPError, URLError) as error:
				irc.error("Data not retrieved because {}".format(str(error.reason)))
				return
			except timeout:
				irc.error('Socket timed out, please try again later') 
				return
			values2 = json.loads(response2.read().decode('utf-8'))
			if values2 is None:
				irc.reply("No results found")
				return
			else:
				verso = values2['text'][0]
			reference = values['verse']['details']['reference']
			verso = ircutils.mircColor(verso, fg='pink')
			reference = ircutils.mircColor(reference, fg='yellow')
			output = ("{0} {1} - {2} {3}").format(emoji.emojize(ircutils.mircColor('\u271D',bg='red', fg='black')), verso, reference, emoji.emojize(ircutils.mircColor('\u271D', bg='red', fg='black')))
			irc.reply(_(output))
	bible = wrap(bible, [additional('text')])

Class = Bible

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
