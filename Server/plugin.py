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
import subprocess
from random import randint

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks


try:
	from supybot.i18n import PluginInternationalization
	_ = PluginInternationalization('Server')
except ImportError:
	# Placeholder that allows to run the plugin on a bot
	# without the i18n module
	_ = lambda x: x


class Server(callbacks.Plugin):
	"""Server Administration Plugin"""
	pass
		
	def srvuptime(self, irc, msg, args, argv):
		"""
		Returns the server uptime
		"""
		result = subprocess.run(['uptime', ''], stdout=subprocess.PIPE)
		irc.reply(_(result.stdout.decode('utf-8').rstrip()))
	def srvuname(self, irc, msg, args, argv):
		"""
		Returns the server uptime
		"""
		result = subprocess.run(['uname', '-a'], stdout=subprocess.PIPE)
		irc.reply(_(result.stdout.decode('utf-8').rstrip()))
	def srvphp(self, irc, msg, args, argv):
		"""
		Returns the server php version
		"""
		result = subprocess.run(['php', '-v'], stdout=subprocess.PIPE)
		irc.reply(_(result.stdout.decode('utf-8').rstrip()))
	def srvpython(self, irc, msg, args, argv):
		"""
		Returns the server php version
		"""
		result = subprocess.run(['python3', '-V'], stdout=subprocess.PIPE)
		irc.reply(_(result.stdout.decode('utf-8').rstrip()))
	srvuptime = wrap(srvuptime, ['owner', additional('text')])
	srvuname = wrap(srvuname, ['owner', additional('text')])
	srvphp = wrap(srvphp, ['owner', additional('text')])
	srvpython = wrap(srvpython, ['owner', additional('text')])

Class = Server

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
