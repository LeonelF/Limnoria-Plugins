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
from urllib.request import urlopen, HTTPError, URLError
from socket import timeout

import emoji
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks


try:
	from supybot.i18n import PluginInternationalization
	_ = PluginInternationalization('Coin')
except ImportError:
	# Placeholder that allows to run the plugin on a bot
	# without the i18n module
	_ = lambda x: x


class Coin(callbacks.Plugin):
	"""Fetch Coin market price"""
	pass
		
	def coin(self, irc, msg, args, argv):
		"""<coin to fetch the prices> [amount]

		Returns the price of the coin.
		"""
		argv = str(argv.upper()).split(" ")
		if (argv[0] == "None"):
			irc.error("Usage .coin <coin coin1 coinN> [ammount]")
			return
		ammount = 1
		if (len(argv) > 1):
			if (len(argv) > 6):
				irc.error("Possible bot abuse detected, ignoring the command...")
				return
			else:
				try:
					ammount = float(argv[-1])
					argv = argv[:-1]
				except:
					ammount = 1
		resultcoin = ",".join(argv )
		url = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms=BTC,EUR,USD'.format(resultcoin.upper())

		try:
			response = urlopen(url, timeout=5)
		except (HTTPError, URLError) as error:
			irc.error('Data of %s not retrieved because %s', name, error)
			return
		except timeout:
			irc.error('Socket timed out, please try again later') 
			return
		values = json.loads(response.read().decode('utf-8'))
		for arg in argv: 
			try:
				tmp = values['RAW'][arg]
			except:
				errout = ("No results found for {0}").format(arg)
				irc.reply(errout)
				continue
			if (arg != "BTC"):
				btc = values['RAW'][arg]['BTC']['PRICE']
				prtbct = values['DISPLAY'][arg]['BTC']['CHANGEPCT24HOUR']
				if (float(prtbct) > 0):
					iconbtc = ircutils.mircColor('\u2b06', fg='green')
				else:
					iconbtc = ircutils.mircColor('\u2b07', fg='red')
				btc_out = (" = {0:.8f} BTC {1} ({2}%)").format(float(btc) * float(ammount), emoji.emojize(iconbtc), prtbct)
			else:
				btc_out = ""
			eur = values['RAW'][arg]['EUR']['PRICE']
			usd = values['RAW'][arg]['USD']['PRICE']

			prteur = values['DISPLAY'][arg]['EUR']['CHANGEPCT24HOUR']
			prtusd = values['DISPLAY'][arg]['USD']['CHANGEPCT24HOUR']
			
			if (float(prteur) > 0):
				iconeur = ircutils.mircColor(':arrow_up:', fg='green')
			else:
				iconeur = ircutils.mircColor(':arrow_down:', fg='red')
			if (float(prtusd) > 0):
				iconusd = ircutils.mircColor(':arrow_up:', fg='green')
			else:
				iconusd = ircutils.mircColor(':arrow_down:', fg='red')
			
			output = ("{0:g} {1}{2} = {3:.2f} USD {4} ({5}%) = {6:.2f} EUR {7} ({8}%)").format(float(ammount), arg, btc_out, float(usd) * float(ammount), emoji.emojize(iconusd, use_aliases=True), prtusd, float(eur) * float(ammount), emoji.emojize(iconeur, use_aliases=True), prteur)
			irc.reply(_(output))
	def btc(self, irc, msg, args, argv):
		"""btc

		Returns the price of Bitcoin.
		"""
		
		url = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC&tsyms=EUR,USD'
		ammount = 1
		try:
			response = urlopen(url, timeout=5)
		except (HTTPError, URLError) as error:
			irc.error('Data of %s not retrieved because %s', name, error)
			return
		except timeout:
			irc.error('Socket timed out, please try again later') 
			return
		values = json.loads(response.read().decode('utf-8'))
		 
		try:
			tmp = values['RAW']['BTC']
		except:
			errout = ("No results found for BTC")
			irc.reply(errout)

		btc_out = ""
		eur = values['RAW']['BTC']['EUR']['PRICE']
		usd = values['RAW']['BTC']['USD']['PRICE']

		prteur = values['DISPLAY']['BTC']['EUR']['CHANGEPCT24HOUR']
		prtusd = values['DISPLAY']['BTC']['USD']['CHANGEPCT24HOUR']
		
		if (float(prteur) > 0):
			iconeur = ircutils.mircColor(':arrow_up:', fg='green')
		else:
			iconeur = ircutils.mircColor(':arrow_down:', fg='red')
		if (float(prtusd) > 0):
			iconusd = ircutils.mircColor(':arrow_up:', fg='green')
		else:
			iconusd = ircutils.mircColor(':arrow_down:', fg='red')	
		output = ("{0:g} BTC = {1:.2f} USD {2} ({3}%) = {4:.2f} EUR {5} ({6}%)").format(float(ammount), float(usd) * float(ammount), emoji.emojize(iconusd, use_aliases=True), prtusd, float(eur) * float(ammount), emoji.emojize(iconeur, use_aliases=True), prteur)
		irc.reply(_(output))


	coin = wrap(coin, [additional('text')])
	c = wrap(btc, [additional('text')])

Class = Coin

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
