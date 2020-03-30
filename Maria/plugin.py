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
	_ = PluginInternationalization('Maria')
except ImportError:
	# Placeholder that allows to run the plugin on a bot
	# without the i18n module
	_ = lambda x: x


class Maria(callbacks.Plugin):
	"""Plugin that interacts with maria API from DeadBSD.org"""
	pass
		
	def mariaf(self, irc, msg, args, argv):
		"""
		Search the messages for the given text.
		"""

		argv = str(argv).split(" ")	
		if (argv[0] == "None"):
			irc.error("Usage .mariaf <text to search> [number]")
			return
		pos = 1
		if (len(argv) > 1):	
			try:	
				pos = argv[1]	
			except:	
				pos = 1
		text = argv[0]
		
		url = 'https://maria.deadbsd.org/api/find?text={0}&position={1}'.format(text,pos)
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
				message = values['message']['text']
				datetime = values['message']['datetime']
				number = values['message']['number']
				total = values['total']
				nextfind = values['next']
			except:
				errout = ("No results found for {0}").format(argv[0])
				irc.reply(errout)
				return
		if (int(pos) < int(total)):
			output = ("{0} found '.maria {1} {2}' for the next one").format(total, text, nextfind)
			irc.reply(_(output))
		output1 = ("{0} - {1}, {2}").format(message, number, datetime)
		irc.reply(_(output1))

	def marial(self, irc, msg, args, argv):
		"""
		Returns the latest message.
		"""

		argv = str(argv).split(" ")	
		
		pos = 1
		try:
			if (len(argv) > 0):	
				pos = int(argv[0])
			else:
				pos = 1
		except:	
			pos = 1
		
		url = 'https://maria.deadbsd.org/api/latest?position={0}'.format(pos)
		try:
			response = urlopen(url, timeout=5)
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
				message = values['message']['text']
				datetime = values['message']['datetime']
				number = values['message']['number']
				total = values['total']
				nextfind = values['next']
			except:
				errout = ("No results found for {0}").format(argv[0])
				irc.reply(errout)
				return
		if (int(pos) < int(total)):
			output = ("{0} found '.marial {1}' for the next one").format(total, nextfind)
			irc.reply(_(output))
		output1 = ("{0} - {1}, {2}").format(message, number, datetime)
		irc.reply(_(output1))
	
	def maria(self, irc, msg, args, argv):
		"""
		Returns random message.
		"""
		
		url = 'https://maria.deadbsd.org/api/random'
		try:
			response = urlopen(url, timeout=5)
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
				message = values['message']['text']
				datetime = values['message']['datetime']
				number = values['message']['number']
			except:
				errout = ("No results found for {0}").format(argv[0])
				irc.reply(errout)
				return
		output = ("{0} - {1}, {2}").format(message, number, datetime)
		irc.reply(_(output))
	
	
	maria = wrap(maria, [additional('text')])
	mariaf = wrap(mariaf, [additional('text')])
	marial = wrap(marial, [additional('text')])

Class = Maria

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
