from plugin import Plugin
import discord
import logging
import urllib.request
import os
import uuid
import styrobot
import commands

class Meme(Plugin):
    async def initialize(self, bot):
        self.tag = 'meme'
        self.shortTag = 'meme'
        self.defaultParser = commands.CommandRegistry.PARAM_PARSER_ALL
        self.defaultParserType = commands.ParamParserType.ALL

    @styrobot.plugincommand('10 Guy', name='tenguy') 
    async def _tenguy_(self, server, channel, author, message):
        await self.displayMeme(channel, 'tenguy', message)

    @styrobot.plugincommand('Afraid to Ask Andy', name='afraid')
    async def _afraid_(self, server, channel, author, message):
        await self.displayMeme(channel, 'afraid', message)

    @styrobot.plugincommand('An Older Code Sir, But It Checks Out', name='older')
    async def _older_(self, server, channel, author, message):
        await self.displayMeme(channel, 'older', message)

    @styrobot.plugincommand('Ancient Aliens Guy', name='aag')
    async def _aag_(self, server, channel, author, message):
        await self.displayMeme(channel, 'aag', message)

    @styrobot.plugincommand('At Least You Tried', name='tried')
    async def _tried_(self, server, channel, author, message):
        await self.displayMeme(channel, 'tried', message)

    @styrobot.plugincommand('Baby Insanity Wolf', name='biw')
    async def _biw_(self, server, channel, author, message):
        await self.displayMeme(channel, 'biw', message)

    @styrobot.plugincommand('Bad Luck Brian', name='blb')
    async def _blb_(self, server, channel, author, message):
        await self.displayMeme(channel, 'blb', message)

    @styrobot.plugincommand('But That\'s None of My Business', name='kermit')
    async def _kermit_(self, server, channel, author, message):
        await self.displayMeme(channel, 'kermit', message)

    @styrobot.plugincommand('Butthurt Dweller', name='bd')
    async def _bd_(self, server, channel, author, message):
        await self.displayMeme(channel, 'bd', message)

    @styrobot.plugincommand('Captain Hindsight', name='ch')
    async def _ch_(self, server, channel, author, message):
        await self.displayMeme(channel, 'ch', message)

    @styrobot.plugincommand('Comic Book Guy', name='cbg')
    async def _cbg_(self, server, channel, author, message):
        await self.displayMeme(channel, 'cbg', message)

    @styrobot.plugincommand('Condescending Wonka', name='wonka')
    async def _wonka_(self, server, channel, author, message):
        await self.displayMeme(channel, 'wonka', message)

    @styrobot.plugincommand('Confession Bear', name='cb')
    async def _cb_(self, server, channel, author, message):
        await self.displayMeme(channel, 'cb', message)

    @styrobot.plugincommand('Conspiracy Keanu', name='keanu')
    async def _keanu_(self, server, channel, author, message):
        await self.displayMeme(channel, 'keanu', message)

    @styrobot.plugincommand('Dating Site Murderer', name='dsm')
    async def _dsm_(self, server, channel, author, message):
        await self.displayMeme(channel, 'dsm', message)

    @styrobot.plugincommand('Do It Live!', name='live')
    async def _live_(self, server, channel, author, message):
        await self.displayMeme(channel, 'live', message)

    @styrobot.plugincommand('Do You Want Ants?', name='ants')
    async def _ants_(self, server, channel, author, message):
        await self.displayMeme(channel, 'ants', message)

    @styrobot.plugincommand('Doge', name='doge')
    async def _doge_(self, server, channel, author, message):
        await self.displayMeme(channel, 'doge', message)

    @styrobot.plugincommand('Drake Always On Beat', name='alwaysonbeat')
    async def _alwaysonbeat_(self, server, channel, author, message):
        await self.displayMeme(channel, 'alwaysonbeat', message)

    @styrobot.plugincommand('Ermahgerd', name='ermg')
    async def _ermg_(self, server, channel, author, message):
        await self.displayMeme(channel, 'ermg', message)

    @styrobot.plugincommand('Facepalm', name='facepalm')
    async def _facepalm_(self, server, channel, author, message):
        await self.displayMeme(channel, 'facepalm', message)

    @styrobot.plugincommand('First World Problems', name='fwp')
    async def _fwp_(self, server, channel, author, message):
        await self.displayMeme(channel, 'fwp', message)

    @styrobot.plugincommand('Forever Alone', name='fa')
    async def _fa_(self, server, channel, author, message):
        await self.displayMeme(channel, 'fa', message)

    @styrobot.plugincommand('Foul Bachelor Frog', name='fbf')
    async def _fbf_(self, server, channel, author, message):
        await self.displayMeme(channel, 'fbf', message)

    @styrobot.plugincommand('Fuck Me, Right?', name='fmr')
    async def _fmr_(self, server, channel, author, message):
        await self.displayMeme(channel, 'fmr', message)

    @styrobot.plugincommand('Futurama Fry', name='fry')
    async def _fry_(self, server, channel, author, message):
        await self.displayMeme(channel, 'fry', message)

    @styrobot.plugincommand('Good Guy Greg', name='ggg')
    async def _ggg_(self, server, channel, author, message):
        await self.displayMeme(channel, 'ggg', message)

    @styrobot.plugincommand('Hipster Barista', name='hipster')
    async def _hipster_(self, server, channel, author, message):
        await self.displayMeme(channel, 'hipster', message)

    @styrobot.plugincommand('I Can Has Cheezburger?', name='icanhas')
    async def _icanhas_(self, server, channel, author, message):
        await self.displayMeme(channel, 'icanhas', message)

    @styrobot.plugincommand('I Feel Like I\'m Taking Crazy Pills', name='crazypills')
    async def _crazypills_(self, server, channel, author, message):
        await self.displayMeme(channel, 'crazypills', message)

    @styrobot.plugincommand('I Guarantee It', name='mw')
    async def _mw_(self, server, channel, author, message):
        await self.displayMeme(channel, 'mw', message)

    @styrobot.plugincommand('I Have No Idea What I\'m Doing', name='noidea')
    async def _noidea_(self, server, channel, author, message):
        await self.displayMeme(channel, 'noidea', message)

    @styrobot.plugincommand('I Immediately Regret This Decision!', name='regret')
    async def _regret_(self, server, channel, author, message):
        await self.displayMeme(channel, 'regret', message)

    @styrobot.plugincommand('I Should Buy a Boat Cat', name='boat')
    async def _boat_(self, server, channel, author, message):
        await self.displayMeme(channel, 'boat', message)

    @styrobot.plugincommand('I Should Not Have Said That', name='hagrid')
    async def _hagrid_(self, server, channel, author, message):
        await self.displayMeme(channel, 'hagrid', message)

    @styrobot.plugincommand('I Would Be So Happy', name='sohappy')
    async def _sohappy_(self, server, channel, author, message):
        await self.displayMeme(channel, 'sohappy', message)

    @styrobot.plugincommand('I am the Captain Now', name='captain')
    async def _captain_(self, server, channel, author, message):
        await self.displayMeme(channel, 'captain', message)

    @styrobot.plugincommand('Inigo Montoya', name='inigo')
    async def _inigo_(self, server, channel, author, message):
        await self.displayMeme(channel, 'inigo', message)

    @styrobot.plugincommand('Insanity Wolf', name='iw')
    async def _iw_(self, server, channel, author, message):
        await self.displayMeme(channel, 'iw', message)

    @styrobot.plugincommand('It\'s A Trap!', name='ackbar')
    async def _ackbar_(self, server, channel, author, message):
        await self.displayMeme(channel, 'ackbar', message)

    @styrobot.plugincommand('It\'s Happening', name='happening')
    async def _happening_(self, server, channel, author, message):
        await self.displayMeme(channel, 'happening', message)

    @styrobot.plugincommand('It\'s Simple, Kill the Batman', name='joker')
    async def _joker_(self, server, channel, author, message):
        await self.displayMeme(channel, 'joker', message)

    @styrobot.plugincommand('Jony Ive Redesigns Things', name='ive')
    async def _ive_(self, server, channel, author, message):
        await self.displayMeme(channel, 'ive', message)

    @styrobot.plugincommand('Laughing Lizard', name='ll')
    async def _ll_(self, server, channel, author, message):
        await self.displayMeme(channel, 'll', message)

    @styrobot.plugincommand('Matrix Morpheus', name='morpheus')
    async def _morpheus_(self, server, channel, author, message):
        await self.displayMeme(channel, 'morpheus', message)

    @styrobot.plugincommand('Milk Was a Bad Choice', name='badchoice')
    async def _badchoice_(self, server, channel, author, message):
        await self.displayMeme(channel, 'badchoice', message)

    @styrobot.plugincommand('Minor Mistake Marvin', name='mmm')
    async def _mmm_(self, server, channel, author, message):
        await self.displayMeme(channel, 'mmm', message)

    @styrobot.plugincommand('Nothing To Do Here', name='jetpack')
    async def _jetpack_(self, server, channel, author, message):
        await self.displayMeme(channel, 'jetpack', message)

    @styrobot.plugincommand('Oh, I\'m Sorry, I Thought This Was America', name='imsorry')
    async def _imsorry_(self, server, channel, author, message):
        await self.displayMeme(channel, 'imsorry', message)

    @styrobot.plugincommand('Oh, Is That What We\'re Going to Do Today?', name='red')
    async def _red_(self, server, channel, author, message):
        await self.displayMeme(channel, 'red', message)

    @styrobot.plugincommand('One Does Not Simply Walk into Mordor', name='mordor')
    async def _mordor_(self, server, channel, author, message):
        await self.displayMeme(channel, 'mordor', message)

    @styrobot.plugincommand('Oprah You Get a Car', name='oprah')
    async def _oprah_(self, server, channel, author, message):
        await self.displayMeme(channel, 'oprah', message)

    @styrobot.plugincommand('Overly Attached Girlfriend', name='oag')
    async def _oag_(self, server, channel, author, message):
        await self.displayMeme(channel, 'oag', message)

    @styrobot.plugincommand('Pepperidge Farm Remembers', name='remembers')
    async def _remembers_(self, server, channel, author, message):
        await self.displayMeme(channel, 'remembers', message)

    @styrobot.plugincommand('Philosoraptor', name='philosoraptor')
    async def _philosoraptor_(self, server, channel, author, message):
        await self.displayMeme(channel, 'philosoraptor', message)

    @styrobot.plugincommand('Probably Not a Good Idea', name='jw')
    async def _jw_(self, server, channel, author, message):
        await self.displayMeme(channel, 'jw', message)

    @styrobot.plugincommand('Push it somewhere else Patrick', name='patrick')
    async def _patrick_(self, server, channel, author, message):
        await self.displayMeme(channel, 'patrick', message)

    @styrobot.plugincommand('Sad Barack Obama', name='sad-obama')
    async def _sadobama_(self, server, channel, author, message):
        await self.displayMeme(channel, 'sad-obama', message)

    @styrobot.plugincommand('Sad Bill Clinton', name='sad-clinton')
    async def _sadclinton_(self, server, channel, author, message):
        await self.displayMeme(channel, 'sad-clinton', message)

    @styrobot.plugincommand('Sad Frog / Feels Bad Man', name='sadfrog')
    async def _sadfrog_(self, server, channel, author, message):
        await self.displayMeme(channel, 'sadfrog', message)

    @styrobot.plugincommand('Sad George Bush', name='sad-bush')
    async def _sadbush_(self, server, channel, author, message):
        await self.displayMeme(channel, 'sad-bush', message)

    @styrobot.plugincommand('Sad Joe Biden', name='sad-biden')
    async def _sadbiden_(self, server, channel, author, message):
        await self.displayMeme(channel, 'sad-biden', message)

    @styrobot.plugincommand('Sad John Boehner', name='sad-boehner')
    async def _sadboehner_(self, server, channel, author, message):
        await self.displayMeme(channel, 'sad-boehner', message)

    @styrobot.plugincommand('Sarcastic Bear', name='sarcasticbear')
    async def _sarcasticbear_(self, server, channel, author, message):
        await self.displayMeme(channel, 'sarcasticbear', message)

    @styrobot.plugincommand('Schrute Facts', name='dwight')
    async def _dwight_(self, server, channel, author, message):
        await self.displayMeme(channel, 'dwight', message)

    @styrobot.plugincommand('Scumbag Brain', name='sb')
    async def _sb_(self, server, channel, author, message):
        await self.displayMeme(channel, 'sb', message)

    @styrobot.plugincommand('Scumbag Steve', name='ss')
    async def _ss_(self, server, channel, author, message):
        await self.displayMeme(channel, 'ss', message)

    @styrobot.plugincommand('Sealed Fate', name='sf')
    async def _sf_(self, server, channel, author, message):
        await self.displayMeme(channel, 'sf', message)

    @styrobot.plugincommand('See? Nobody Cares', name='dodgson')
    async def _dodgson_(self, server, channel, author, message):
        await self.displayMeme(channel, 'dodgson', message)

    @styrobot.plugincommand('Shut Up and Take My Money!', name='money')
    async def _money_(self, server, channel, author, message):
        await self.displayMeme(channel, 'money', message)

    @styrobot.plugincommand('So Hot Right Now', name='sohot')
    async def _sohot_(self, server, channel, author, message):
        await self.displayMeme(channel, 'sohot', message)

    @styrobot.plugincommand('So I Got That Goin\' For Me, Which is Nice', name='goinforme')
    async def _goinforme_(self, server, channel, author, message):
        await self.displayMeme(channel, 'goinforme', message)

    @styrobot.plugincommand('Socially Awesome Awkward Penguin', name='awesome-awkward')
    async def _awesomeawkward_(self, server, channel, author, message):
        await self.displayMeme(channel, 'awesome-awkward', message)

    @styrobot.plugincommand('Socially Awesome Penguin', name='awesome')
    async def _awesome_(self, server, channel, author, message):
        await self.displayMeme(channel, 'awesome', message)

    @styrobot.plugincommand('Socially Awkward Awesome Penguin', name='awkward-awesome')
    async def _awkwardawesome_(self, server, channel, author, message):
        await self.displayMeme(channel, 'awkward-awesome', message)

    @styrobot.plugincommand('Socially Awkward Penguin', name='awkward')
    async def _awkward_(self, server, channel, author, message):
        await self.displayMeme(channel, 'awkward', message)

    @styrobot.plugincommand('Stop Trying to Make Fetch Happen', name='fetch')
    async def _fetch_(self, server, channel, author, message):
        await self.displayMeme(channel, 'fetch', message)

    @styrobot.plugincommand('Success Kid', name='success')
    async def _success_(self, server, channel, author, message):
        await self.displayMeme(channel, 'success', message)

    @styrobot.plugincommand('Super Cool Ski Instructor', name='ski')
    async def _ski_(self, server, channel, author, message):
        await self.displayMeme(channel, 'ski', message)

    @styrobot.plugincommand('That Would Be Great', name='officespace')
    async def _officespace_(self, server, channel, author, message):
        await self.displayMeme(channel, 'officespace', message)

    @styrobot.plugincommand('The Most Interesting Man in the World', name='interesting')
    async def _interesting_(self, server, channel, author, message):
        await self.displayMeme(channel, 'interesting', message)

    @styrobot.plugincommand('The Rent Is Too Damn High', name='toohigh')
    async def _toohigh_(self, server, channel, author, message):
        await self.displayMeme(channel, 'toohigh', message)

    @styrobot.plugincommand('This is Bull, Shark', name='bs')
    async def _bs_(self, server, channel, author, message):
        await self.displayMeme(channel, 'bs', message)

    @styrobot.plugincommand('What is this, a Center for Ants?!', name='center')
    async def _center_(self, server, channel, author, message):
        await self.displayMeme(channel, 'center', message)

    @styrobot.plugincommand('Why Not Both?', name='both')
    async def _both_(self, server, channel, author, message):
        await self.displayMeme(channel, 'both', message)

    @styrobot.plugincommand('Winter is coming', name='winter')
    async def _winter_(self, server, channel, author, message):
        await self.displayMeme(channel, 'winter', message)

    @styrobot.plugincommand('X all the Y', name='xy')
    async def _xy_(self, server, channel, author, message):
        await self.displayMeme(channel, 'xy', message)

    @styrobot.plugincommand('X, X Everywhere', name='buzz')
    async def _buzz_(self, server, channel, author, message):
        await self.displayMeme(channel, 'buzz', message)

    @styrobot.plugincommand('Xzibit Yo Dawg', name='yodawg')
    async def _yodawg_(self, server, channel, author, message):
        await self.displayMeme(channel, 'yodawg', message)

    @styrobot.plugincommand('Y U NO Guy', name='yuno')
    async def _yuno_(self, server, channel, author, message):
        await self.displayMeme(channel, 'yuno', message)

    @styrobot.plugincommand('Y\'all Got Any More of Them', name='yallgot')
    async def _yallgot_(self, server, channel, author, message):
        await self.displayMeme(channel, 'yallgot', message)

    @styrobot.plugincommand('You Should Feel Bad', name='bad')
    async def _bad_(self, server, channel, author, message):
        await self.displayMeme(channel, 'bad', message)

    @styrobot.plugincommand('You Sit on a Throne of Lies', name='elf')
    async def _elf_(self, server, channel, author, message):
        await self.displayMeme(channel, 'elf', message)

    @styrobot.plugincommand('You Were the Chosen One!', name='chosen')
    async def _chosen_(self, server, channel, author, message):
        await self.displayMeme(channel, 'chosen', message)

    def parseMeme(self, message):
        if message.find(':') is not -1:
            top, bottom = message.split(':')
            return [top, bottom]
        else:
            return [message, '']

    async def displayMeme(self, channel, type, message):
        message = self.parseMeme(message)
        if not message[0]:
            await self.bot.send_message(channel, 'That is not a valid meme string')
            self.logger.debug('[%s]: Invalid meme string: %s | %s', type, message[0], message[1])
            return

        request = urllib.request.Request(
            'https://memegen.link/{}/{}/{}.jpg'.format(type, message[0], message[1]),
            data = None,
            headers = {
                'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.19 (KHTML, like Gecko) Ubuntu/12.04 Chromium/18.0.1025.168 Chrome/18.0.1025.168 Safari/535.19'
            }
        )

        self.logger.debug('Attempting to do API call to memegen')

        f = None
        try:
            f = urllib.request.urlopen(request)
        except urllib.error.HTTPError as ex:
            await self.bot.send_message(channel, 'Something seems to have gone wrong while creating the meme, please try again. If it continues to fail, try waiting a few minutes.')
            self.logger.debug('API call to memegen has failed with error: %s', ex)
            return

        self.logger.debug('API call to memegen has succeeded')

        filename = 'images/' + str(uuid.uuid1()) + '.jpg'
        output = open(filename, 'wb')
        output.write(f.read())
        output.close()

        self.logger.debug('[%s]: %s | %s', type, message[0], message[1])
        await self.bot.send_file(channel, filename)

        try:
            os.remove(filename)
            self.logger.debug('Deleted meme %s', filename)
        except OSError:
            self.logger.debug('Meme file %s does not exist', filename)
