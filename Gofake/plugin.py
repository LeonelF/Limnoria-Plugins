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
	_ = PluginInternationalization('Gofake')
except ImportError:
	# Placeholder that allows to run the plugin on a bot
	# without the i18n module
	_ = lambda x: x


class Gofake(callbacks.Plugin):
	"""Generates a Fake Search with the google bug"""
	pass

	def gofake(self, irc, msg, args, argv):
		"""<keywords+to+search> <fake+keywords+to+show>

		Returns the url to a fake search.
		"""
		argv = str(argv).split(" ")
		if (len(argv) < 2):
			irc.error("Usage .gofake <keywords+to+search> <fake+keywords+to+show>")
			return
		search = argv[0].replace(" ","+")
		fake = argv[1].replace(" ","+")
		url = 'https://www.google.com/search?q={}'.format(urllib.parse.quote(search))
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
		for line_number, line in enumerate(response):
			if "kgmid" in str(line):
				code = str(line)
				break
		if 'myVar' not in locals():
			irc.error('It was impossible to create a fake search url with the keywords provided')
			return
		init = code.find("kgmid")
		end = code.find("\\\\u0026hl")
		code2 = code[init:end]
		eval = code2.split("u003d")
		output = "https://www.google.com/search?kgmid={0}&q={1}&kponly".format(eval[1].replace("\\",""), fake)
		irc.reply(_(output))
	gofake = wrap(gofake, [additional('text')])

Class = Gofake

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
