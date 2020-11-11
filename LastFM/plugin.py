###
# Copyright (c) 2020, Leonel Faria
# All Hail Pedro de Oliveira (Where forked my version from)
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
    _ = PluginInternationalization('LastFM')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x
import supybot.utils.minisix as minisix
import os
import sqlite3
import requests
import json

class SqliteLastFMDB(object):
    def __init__(self, filename):
        self.dbs = ircutils.IrcDict()
        self.filename = filename

    def close(self):
        for db in self.dbs.values():
            db.close()

    def _getDb(self, channel):
        filename = plugins.makeChannelFilename(self.filename, channel)
        if filename in self.dbs:
            return self.dbs[filename]
        if os.path.exists(filename):
            db = sqlite3.connect(filename, check_same_thread=False)
            if minisix.PY2:
                db.text_factory = str
            self.dbs[filename] = db
            return db
        db = sqlite3.connect(filename, check_same_thread=False)
        if minisix.PY2:
            db.text_factory = str
        self.dbs[filename] = db
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE lastfm (
                          id INTEGER PRIMARY KEY,
                          nick TEXT,
                          user TEXT
                          )""")
        db.commit()
        return db

    def get_user(self, channel, nick):
        db = self._getDb(channel)
        cursor = db.cursor()
        cursor.execute("""SELECT user FROM lastfm
                          WHERE nick=?""", (nick,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def set_user(self, channel, nick, user):
        db = self._getDb(channel)
        cursor = db.cursor()
        cursor.execute("""DELETE FROM lastfm
                          WHERE nick=?""", (nick,))
        cursor.execute("""INSERT INTO lastfm VALUES (NULL, ?, ?)""",
                       (nick, user,))
        db.commit()

LastFMDB = plugins.DB('LastFM',
                     {'sqlite3': SqliteLastFMDB})

class LastFM(callbacks.Plugin):
    """Last.fm client"""

    def __init__(self, irc):
        self.__parent = super(LastFM, self)
        self.__parent.__init__(irc)
        self.db = LastFMDB()
        self.network = None
        self.prepend = "0,5last.fm"
    
    def die(self):
        self.__parent.die()
        self.db.close()

    def connect(self):
        key = self.registryValue('apiKey')

        if not key:
            irc.error("{} API key not set".format(self.prepend))
            return False
        return True

    def setuser(self, irc, msg, args, channel, user):
        """[<channel>] <last.fm user>

        Assigns the <last.fm user> to the current nick, in [channel].
        """
        self.db.set_user(channel, msg.nick.lower(), user)
        irc.reply("{} User set as {} for {}".format(
            self.prepend,
            user,
            msg.nick
            ), prefixNick=False)
    setuser = wrap(setuser, ['channel', 'anything'])

    def nowplaying(self, irc, msg, args, channel, user):
        """[<channel>] [<last.fm user>]

        Show the currently playing song, by [last.fm user], in [channel].
        """
        if self.connect() is False:
            return
        if user:
            username = user
        else:
            username = self.db.get_user(channel, msg.nick.lower())

        headers = {
            'user-agent': 'Dataquest'
        }

        key = self.registryValue('apiKey')

        payload_current_track = {
            'api_key': key,
            'method': 'user.getRecentTracks',
            'user': username,
            'limit': 1,
            'format': 'json'
        }

        r = requests.get('http://ws.audioscrobbler.com/2.0/', headers=headers, params=payload_current_track)
        if "nowplaying" in r.content.decode("utf-8"):
            values = json.loads(r.content.decode("utf-8"))
            artist = values['recenttracks']['track'][0]['artist']['#text']
            track = values['recenttracks']['track'][0]['name']

            payload_track = {
            'api_key': key,
            'method': 'track.getInfo',
            'username': username,
            'track': values['recenttracks']['track'][0]['name'],
            'artist': values['recenttracks']['track'][0]['artist']['#text'],
            'format': 'json'
            }

            r2 = requests.get('http://ws.audioscrobbler.com/2.0/', headers=headers, params=payload_track)
            values2 = json.loads(r2.content.decode("utf-8"))
            playcount = values2['track']['userplaycount']
            if len(values2['track']['toptags']['tag']) > 0:
                tags = ""
                for tag in values2['track']['toptags']['tag']:
                    tags = tags + tag['name'] + ", "
            else:
                tags = ""
            message = "{} {} is listening to: {} - {} ({} plays) {}".format(
                self.prepend,
                username,
                track,
                artist,
                playcount,
                tags[:-2]
                )
        else:
            message = "{} {} is not playing anything right now".format(
                self.prepend,
                username
                )
            
        irc.reply(message, prefixNick=False)
    nowplaying = wrap(nowplaying, ['channel', optional('anything')])
Class = LastFM


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
