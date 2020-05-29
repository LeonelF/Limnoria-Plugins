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
import emoji
from datetime import datetime
from urllib.request import urlopen, HTTPError, URLError
from urllib.parse import urlencode
from socket import timeout

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks


try:
	from supybot.i18n import PluginInternationalization
	_ = PluginInternationalization('Weather')
except ImportError:
	# Placeholder that allows to run the plugin on a bot
	# without the i18n module
	_ = lambda x: x


class Weather(callbacks.Plugin):
	"""Fetch the weather conditions for the given location with OpenWeatherMap API"""
	threaded = True
	pass

	def weather(self, irc, msg, args, argv):
		"""<location>

		Returns the weather conditions for the given location, and forecast if requested.
		"""
		argv2 = str(argv).split(" ")
		if (argv2[0] == "None"):
			irc.error("Usage .weather <location>")
			return
		city = argv
		
		url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=f8801321df9b3be884c3b641c1878f99'.format(urllib.parse.quote(city))
		
		try:
			response = urlopen(url, timeout=5)
		except (HTTPError, URLError) as error:
			irc.error("Data not retrieved because: {}".format(str(error.reason)))
			return
		except timeout:
			irc.error('Socket timed out, please try again later') 
			return
		values = json.loads(response.read().decode('utf-8'))
		if values is None:
			irc.reply("No results found")
			return
		elif (values['cod'] == '404'):
			irc.reply("No results found")
			return
		else:
			location = values['name']
			country = values['sys']['country']
			temp = values['main']['temp']
			temp_max = values['main']['temp_max']
			temp_min = values['main']['temp_min']
			conditions = values['weather'][0]
			conditions1 = conditions['main']
			conditions2 = conditions['description']
			iconid = conditions['icon']
			humidity = values['main']['humidity']
			wind = values['wind']['speed']
			if iconid == '01d':
				icon = ':sun:'
			elif iconid == '01n':
				icon  = ':crescent_moon:'
			elif (iconid == '02d') or (iconid == '02n'):
				icon  = ':partly_sunny:'
			elif (iconid == '03d') or (iconid == '03n'):
				icon  = ':cloud:'
			elif (iconid == '04d') or (iconid == '04n'):
				icon  = ':cloud:'
			elif (iconid == '09d') or (iconid == '09n') or (iconid == '10d') or (iconid == '10n'):
				icon  = ':umbrella:'
			elif (iconid == '11d') or (iconid == '11n'):
				icon  = ':zap:'
			elif (iconid == '13d') or (iconid == '13n'):
				icon  = ':snowflake:'
			elif (iconid == '50d') or (iconid == '50n'):
				icon  = ':foggy:'
			else:
				icon = iconid
			output = ("{0}, {1} Temperature: {2}ºC (max: {3}ºC min: {4}ºC) Conditions: {5} {6} - {7} Humidity: {8}%  Wind: {9}km/h").format(location, country, temp, temp_max, temp_min, emoji.emojize(icon, use_aliases=True), conditions1, conditions2, humidity, wind,)
			irc.reply(_(output))
	def forecast(self, irc, msg, args, argv):
		"""<location> [results (1-5)]

		Returns the weather forecast for the given location.
		"""
		argv2 = str(argv).split(" ")
		if (argv2[0] == "None"):
			irc.error("Usage .forecast <location> [results (1-5)]")
			return
		city = argv2[0]
		if (len(argv2) > 1):
			if (argv2[-1].isdigit()):
				results = int(argv2[-1])
			else:
				results = 1
		else:
			results = 1
		url = 'https://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid=f8801321df9b3be884c3b641c1878f99'.format(city)
		try:
			response = urlopen(url, timeout=5)
		except (HTTPError, URLError) as error:
			irc.error("Data not retrieved because: {}".format(str(error.reason)))
			return
		except timeout:
			irc.error('Socket timed out, please try again later') 
			return
		values = json.loads(response.read().decode('utf-8'))
		if values is None:
			irc.reply("No results found")
			return
		else:
			location = values['city']['name']
			country = values['city']['country']
			forecasts = values['list']
			if results > 0:
				if results > 5:
					results = 5
			curDay = ''
			count = 0
			for x in range(0, 39):
				if (x >= 39):
					break
				if (count >= results):
					break
				y = x
				if (y > 0):
					y += 4
				intday = int(forecasts[x]['dt'])
				day = datetime.utcfromtimestamp(intday).strftime('%d')
				if (day == curDay):
					continue
				curDay = day
				
				date = forecasts[y]['dt_txt']
				temp = forecasts[y]['main']['temp']
				conditions = forecasts[y]['weather'][0]
				conditions1 = conditions['main']
				conditions2 = conditions['description']
				iconid = conditions['icon']
				humidity = forecasts[y]['main']['humidity']
				wind = forecasts[y]['wind']['speed']
				if iconid == '01d':
					icon = ':sun:'
				elif iconid == '01n':
					icon  = ':crescent_moon:'
				elif (iconid == '02d') or (iconid == '02n'):
					icon  = ':partly_sunny:'
				elif (iconid == '03d') or (iconid == '03n'):
					icon  = ':cloud:'
				elif (iconid == '04d') or (iconid == '04n'):
					icon  = ':cloud:'
				elif (iconid == '09d') or (iconid == '09n') or (iconid == '10d') or (iconid == '10n'):
					icon  = ':umbrella:'
				elif (iconid == '11d') or (iconid == '11n'):
					icon  = ':zap:'
				elif (iconid == '13d') or (iconid == '13n'):
					icon  = ':snowflake:'
				elif (iconid == '50d') or (iconid == '50n'):
					icon  = ':foggy:'
				else:
					icon = iconid
				output = ("{0}, {1} {2} Temperature: {3}ºC Conditions: {4} {5} - {6} Humidity: {7}%  Wind: {8}km/h").format(location, country, date, temp, emoji.emojize(icon, use_aliases=True), conditions1, conditions2, humidity, wind,)
				irc.reply(_(output))
				count += 1
	weather = wrap(weather, [additional('text')])
	forecast = wrap(forecast, [additional('text')])
Class = Weather

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
