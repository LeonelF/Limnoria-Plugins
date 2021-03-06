###
# Copyright (c) 2017, Weasel
# All rights reserved.
#
#
###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import random
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Random')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


class Random(callbacks.Plugin):
    """This plugin provides a few random number commands and some
    commands for getting random samples.  Use the "seed" command to seed
    the plugin's random number generator if you like, though it is
    unnecessary as it gets seeded upon loading of the plugin.  The
    "random" command is most likely what you're looking for, though
    there are a number of other useful commands in this plugin.  Use
    'list random' to check them out.  """
    pass
    def __init__(self, irc):
        self.__parent = super(Random, self)
        self.__parent.__init__(irc)
        self.rng = random.Random()   # create our rng
        self.rng.seed()   # automatically seeds with current time

    def random(self, irc, msg, args):
        """takes no arguments

        Returns the next random number from the random number generator.
        """
        irc.reply(str(self.rng.random()))
    random = wrap(random)
	
    def seed(self, irc, msg, args, seed):
        """<seed>

        Sets the internal RNG's seed value to <seed>.  <seed> must be a
        floating point number.
        """
        self.rng.seed(seed)
        irc.replySuccess()
    seed = wrap(seed, ['float'])

    def sample(self, irc, msg, args, n, items):
        """<number of items> <item1> [<item2> ...]

        Returns a sample of the <number of items> taken from the remaining
        arguments.  Obviously <number of items> must be less than the number
        of arguments given.
        """
        if n > len(items):
            irc.error('<number of items> must be less than the number of arguments.')
            return
        sample = self.rng.sample(items, n)
        sample.sort()
        irc.reply(utils.str.commaAndify(sample))
    sample = wrap(sample, ['int', many('anything')])

    def diceroll(self, irc, msg, args, n):
        """[<number of sides>]

        Rolls a die with <number of sides> sides.  The default number of sides
        is 6.
        """
        s = 'rolls a %s saaan' % self.rng.randrange(1, n)
        irc.reply(s, action=True)
    diceroll = wrap(diceroll, [additional(('int', 'number of sides'), 6)])
Class = Random


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
