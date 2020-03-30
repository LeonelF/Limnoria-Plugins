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
from urllib.request import urlopen, HTTPError, URLError
from socket import timeout
from random import randint

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks


try:
	from supybot.i18n import PluginInternationalization
	_ = PluginInternationalization('Repl')
except ImportError:
	# Placeholder that allows to run the plugin on a bot
	# without the i18n module
	_ = lambda x: x


class Repl(callbacks.Plugin):
	"""Lulz Script For Maria DB"""
	pass
		
	def repl(self, irc, msg, args, argv):
		"""
		Returns the lulz message.
		"""
		argv = str(argv).split(" ")
		
		if (len(argv) != 2):
			irc.error("Usage .repl <male stuff to replace to> <femal stuff to replace to>")
			return
		male = argv[0]
		female = argv[1]

		pos = randint(0, 31118)
		
		url = 'https://maria.deadbsd.org/api/find?text=homem&position={0}'.format(pos)
		try:
			response = urlopen(url, timeout=60)
		except (HTTPError, URLError) as error:
			errout = ("Data not retrieved because {0}").format(error)
			irc.error(errout)
			return
		except timeout:
			irc.error('Socket timed out, please try again later') 
			return
		values = json.loads(response.read().decode('utf-8'))
		try:
			error = values['error']
			if (error == "Not found"):
				irc.reply("Not found")
				return 
		except:
			try:
				tmp = values['message']['text']
				datetime = values['message']['datetime']
				number = values['message']['number']
			except:
				errout = ("No results found for {0}").format(argv[0])
				irc.reply(errout)
		tmp = re.sub("homem",male,tmp, flags=re.I)
		tmp = re.sub("homen",male,tmp, flags=re.I)
		tmp = re.sub("senhoras",female,tmp, flags=re.I)
		tmp = re.sub("senhora",female,tmp, flags=re.I)
		tmp = re.sub("mulheres",female,tmp, flags=re.I)
		tmp = re.sub("senhor ",male,tmp, flags=re.I)
		tmp = re.sub("jovem rapaz",male,tmp, flags=re.I)
		tmp = re.sub("rapaz",male,tmp, flags=re.I)
		tmp = re.sub("cavalheiro",male,tmp, flags=re.I)
		tmp = re.sub("jovem",male,tmp, flags=re.I)
		tmp = re.sub("quarentao",male,tmp, flags=re.I)
		tmp = re.sub("cinquentona",female,tmp, flags=re.I)
		tmp = re.sub("antonio",male,tmp, flags=re.I)
		tmp = re.sub("paulo",male,tmp, flags=re.I)
		tmp = re.sub("sou h",male,tmp, flags=re.I)
		tmp = re.sub("rapariga",female,tmp, flags=re.I)
		tmp = re.sub("mulher",female,tmp, flags=re.I)
		tmp = re.sub("menina",female,tmp, flags=re.I)
		output = ("{0} - {1}, {2}").format(tmp, number, datetime)
		irc.reply(_(output))
	repl = wrap(repl, [additional('text')])

Class = Repl

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
