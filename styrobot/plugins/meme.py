from plugin import Plugin
import discord
import logging
import urllib.request
import os
import uuid

class Meme(Plugin):

    async def initialize(self, bot):
        self.tag = 'meme'
        self.shortTag = 'meme'
        self.memes = {
            'tenguy':'10 Guy',
            'afraid':'Afraid to Ask Andy',
            'older':'An Older Code Sir, But It Checks Out',
            'aag':'Ancient Aliens Guy',
            'tried':'At Least You Tried',
            'biw':'Baby Insanity Wolf',
            'blb':'Bad Luck Brian',
            'kermit':'But That\'s None of My Business',
            'bd':'Butthurt Dweller',
            'ch':'Captain Hindsight',
            'cbg':'Comic Book Guy',
            'wonka':'Condescending Wonka',
            'cb':'Confession Bear',
            'keanu':'Conspiracy Keanu',
            'dsm':'Dating Site Murderer',
            'live':'Do It Live!',
            'ants':'Do You Want Ants?',
            'doge':'Doge',
            'alwaysonbeat':'Drake Always On Beat',
            'ermg':'Ermahgerd',
            'facepalm':'Facepalm',
            'fwp':'First World Problems',
            'fa':'Forever Alone',
            'fbf':'Foul Bachelor Frog',
            'fmr':'Fuck Me, Right?',
            'fry':'Futurama Fry',
            'ggg':'Good Guy Greg',
            'hipster':'Hipster Barista',
            'icanhas':'I Can Has Cheezburger?',
            'crazypills':'I Feel Like I\'m Taking Crazy Pills',
            'mw':'I Guarantee It',
            'noidea':'I Have No Idea What I\'m Doing',
            'regret':'I Immediately Regret This Decision!',
            'boat':'I Should Buy a Boat Cat',
            'hagrid':'I Should Not Have Said That',
            'sohappy':'I Would Be So Happy',
            'captain':'I am the Captain Now',
            'inigo':'Inigo Montoya',
            'iw':'Insanity Wolf',
            'ackbar':'It\'s A Trap!',
            'happening':'It\'s Happening',
            'joker':'It\'s Simple, Kill the Batman',
            'ive':'Jony Ive Redesigns Things',
            'll':'Laughing Lizard',
            'morpheus':'Matrix Morpheus',
            'badchoice':'Milk Was a Bad Choice',
            'mmm':'Minor Mistake Marvin',
            'jetpack':'Nothing To Do Here',
            'imsorry':'Oh, I\'m Sorry, I Thought This Was America',
            'red':'Oh, Is That What We\'re Going to Do Today?',
            'mordor':'One Does Not Simply Walk into Mordor',
            'oprah':'Oprah You Get a Car',
            'oag':'Overly Attached Girlfriend',
            'remembers':'Pepperidge Farm Remembers',
            'philosoraptor':'Philosoraptor',
            'jw':'Probably Not a Good Idea',
            'patrick':'Push it somewhere else Patrick',
            'sad-obama':'Sad Barack Obama',
            'sad-clinton':'Sad Bill Clinton',
            'sadfrog':'Sad Frog / Feels Bad Man',
            'sad-bush':'Sad George Bush',
            'sad-biden':'Sad Joe Biden',
            'sad-boehner':'Sad John Boehner',
            'sarcasticbear':'Sarcastic Bear',
            'dwight':'Schrute Facts',
            'sb':'Scumbag Brain',
            'ss':'Scumbag Steve',
            'sf':'Sealed Fate',
            'dodgson':'See? Nobody Cares',
            'money':'Shut Up and Take My Money!',
            'sohot':'So Hot Right Now',
            'goinforme':'So I Got That Goin\' For Me, Which is Nice',
            'awesome-awkward':'Socially Awesome Awkward Penguin',
            'awesome':'Socially Awesome Penguin',
            'awkward-awesome':'Socially Awkward Awesome Penguin',
            'awkward':'Socially Awkward Penguin',
            'fetch':'Stop Trying to Make Fetch Happen',
            'success':'Success Kid',
            'ski':'Super Cool Ski Instructor',
            'officespace':'That Would Be Great',
            'interesting':'The Most Interesting Man in the World',
            'toohigh':'The Rent Is Too Damn High',
            'bs':'This is Bull, Shark',
            'center':'What is this, a Center for Ants?!',
            'both':'Why Not Both?',
            'winter':'Winter is coming',
            'xy':'X all the Y',
            'buzz':'X, X Everywhere',
            'yodawg':'Xzibit Yo Dawg',
            'yuno':'Y U NO Guy',
            'yallgot':'Y\'all Got Any More of Them',
            'bad':'You Should Feel Bad',
            'elf':'You Sit on a Throne of Lies',
            'chosen':'You Were the Chosen One!'
        }

        for key, value in self.memes.items():
            self.commands.append('<{}><*>(message)<{}>'.format(key, value))

    async def _tenguy_(self, server, channel, author, message):
        await self.displayMeme(channel, 'tenguy', message)

    async def _afraid_(self, server, channel, author, message):
        await self.displayMeme(channel, 'afraid', message)

    async def _older_(self, server, channel, author, message):
        await self.displayMeme(channel, 'older', message)

    async def _aag_(self, server, channel, author, message):
        await self.displayMeme(channel, 'aag', message)

    async def _tried_(self, server, channel, author, message):
        await self.displayMeme(channel, 'tried', message)

    async def _biw_(self, server, channel, author, message):
        await self.displayMeme(channel, 'biw', message)

    async def _blb_(self, server, channel, author, message):
        await self.displayMeme(channel, 'blb', message)

    async def _kermit_(self, server, channel, author, message):
        await self.displayMeme(channel, 'kermit', message)

    async def _bd_(self, server, channel, author, message):
        await self.displayMeme(channel, 'bd', message)

    async def _ch_(self, server, channel, author, message):
        await self.displayMeme(channel, 'ch', message)

    async def _cbg_(self, server, channel, author, message):
        await self.displayMeme(channel, 'cbg', message)

    async def _wonka_(self, server, channel, author, message):
        await self.displayMeme(channel, 'wonka', message)

    async def _cb_(self, server, channel, author, message):
        await self.displayMeme(channel, 'cb', message)

    async def _keanu_(self, server, channel, author, message):
        await self.displayMeme(channel, 'keanu', message)

    async def _dsm_(self, server, channel, author, message):
        await self.displayMeme(channel, 'dsm', message)

    async def _live_(self, server, channel, author, message):
        await self.displayMeme(channel, 'live', message)

    async def _ants_(self, server, channel, author, message):
        await self.displayMeme(channel, 'ants', message)

    async def _doge_(self, server, channel, author, message):
        await self.displayMeme(channel, 'doge', message)

    async def _alwaysonbeat_(self, server, channel, author, message):
        await self.displayMeme(channel, 'alwaysonbeat', message)

    async def _ermg_(self, server, channel, author, message):
        await self.displayMeme(channel, 'ermg', message)

    async def _facepalm_(self, server, channel, author, message):
        await self.displayMeme(channel, 'facepalm', message)

    async def _fwp_(self, server, channel, author, message):
        await self.displayMeme(channel, 'fwp', message)

    async def _fa_(self, server, channel, author, message):
        await self.displayMeme(channel, 'fa', message)

    async def _fbf_(self, server, channel, author, message):
        await self.displayMeme(channel, 'fbf', message)

    async def _fmr_(self, server, channel, author, message):
        await self.displayMeme(channel, 'fmr', message)

    async def _fry_(self, server, channel, author, message):
        await self.displayMeme(channel, 'fry', message)

    async def _ggg_(self, server, channel, author, message):
        await self.displayMeme(channel, 'ggg', message)

    async def _hipster_(self, server, channel, author, message):
        await self.displayMeme(channel, 'hipster', message)

    async def _icanhas_(self, server, channel, author, message):
        await self.displayMeme(channel, 'icanhas', message)

    async def _crazypills_(self, server, channel, author, message):
        await self.displayMeme(channel, 'crazypills', message)

    async def _mw_(self, server, channel, author, message):
        await self.displayMeme(channel, 'mw', message)

    async def _noidea_(self, server, channel, author, message):
        await self.displayMeme(channel, 'noidea', message)

    async def _regret_(self, server, channel, author, message):
        await self.displayMeme(channel, 'regret', message)

    async def _boat_(self, server, channel, author, message):
        await self.displayMeme(channel, 'boat', message)

    async def _hagrid_(self, server, channel, author, message):
        await self.displayMeme(channel, 'hagrid', message)

    async def _sohappy_(self, server, channel, author, message):
        await self.displayMeme(channel, 'sohappy', message)

    async def _captain_(self, server, channel, author, message):
        await self.displayMeme(channel, 'captain', message)

    async def _inigo_(self, server, channel, author, message):
        await self.displayMeme(channel, 'inigo', message)

    async def _iw_(self, server, channel, author, message):
        await self.displayMeme(channel, 'iw', message)

    async def _ackbar_(self, server, channel, author, message):
        await self.displayMeme(channel, 'ackbar', message)

    async def _happening_(self, server, channel, author, message):
        await self.displayMeme(channel, 'happening', message)

    async def _joker_(self, server, channel, author, message):
        await self.displayMeme(channel, 'joker', message)

    async def _ive_(self, server, channel, author, message):
        await self.displayMeme(channel, 'ive', message)

    async def _ll_(self, server, channel, author, message):
        await self.displayMeme(channel, 'll', message)

    async def _morpheus_(self, server, channel, author, message):
        await self.displayMeme(channel, 'morpheus', message)

    async def _badchoice_(self, server, channel, author, message):
        await self.displayMeme(channel, 'badchoice', message)

    async def _mmm_(self, server, channel, author, message):
        await self.displayMeme(channel, 'mmm', message)

    async def _jetpack_(self, server, channel, author, message):
        await self.displayMeme(channel, 'jetpack', message)

    async def _imsorry_(self, server, channel, author, message):
        await self.displayMeme(channel, 'imsorry', message)

    async def _red_(self, server, channel, author, message):
        await self.displayMeme(channel, 'red', message)

    async def _mordor_(self, server, channel, author, message):
        await self.displayMeme(channel, 'mordor', message)

    async def _oprah_(self, server, channel, author, message):
        await self.displayMeme(channel, 'oprah', message)

    async def _oag_(self, server, channel, author, message):
        await self.displayMeme(channel, 'oag', message)

    async def _remembers_(self, server, channel, author, message):
        await self.displayMeme(channel, 'remembers', message)

    async def _philosoraptor_(self, server, channel, author, message):
        await self.displayMeme(channel, 'philosoraptor', message)

    async def _jw_(self, server, channel, author, message):
        await self.displayMeme(channel, 'jw', message)

    async def _patrick_(self, server, channel, author, message):
        await self.displayMeme(channel, 'patrick', message)

    async def _sadobama_(self, server, channel, author, message):
        await self.displayMeme(channel, 'sad-obama', message)

    async def _sadclinton_(self, server, channel, author, message):
        await self.displayMeme(channel, 'sad-clinton', message)

    async def _sadfrog_(self, server, channel, author, message):
        await self.displayMeme(channel, 'sadfrog', message)

    async def _sadbush_(self, server, channel, author, message):
        await self.displayMeme(channel, 'sad-bush', message)

    async def _sadbiden_(self, server, channel, author, message):
        await self.displayMeme(channel, 'sad-biden', message)

    async def _sadboehner_(self, server, channel, author, message):
        await self.displayMeme(channel, 'sad-boehner', message)

    async def _sarcasticbear_(self, server, channel, author, message):
        await self.displayMeme(channel, 'sarcasticbear', message)

    async def _dwight_(self, server, channel, author, message):
        await self.displayMeme(channel, 'dwight', message)

    async def _sb_(self, server, channel, author, message):
        await self.displayMeme(channel, 'sb', message)

    async def _ss_(self, server, channel, author, message):
        await self.displayMeme(channel, 'ss', message)

    async def _sf_(self, server, channel, author, message):
        await self.displayMeme(channel, 'sf', message)

    async def _dodgson_(self, server, channel, author, message):
        await self.displayMeme(channel, 'dodgson', message)

    async def _money_(self, server, channel, author, message):
        await self.displayMeme(channel, 'money', message)

    async def _sohot_(self, server, channel, author, message):
        await self.displayMeme(channel, 'sohot', message)

    async def _goinforme_(self, server, channel, author, message):
        await self.displayMeme(channel, 'goinforme', message)

    async def _awesomeawkward_(self, server, channel, author, message):
        await self.displayMeme(channel, 'awesome-awkward', message)

    async def _awesome_(self, server, channel, author, message):
        await self.displayMeme(channel, 'awesome', message)

    async def _awkwardawesome_(self, server, channel, author, message):
        await self.displayMeme(channel, 'awkward-awesome', message)

    async def _awkward_(self, server, channel, author, message):
        await self.displayMeme(channel, 'awkward', message)

    async def _fetch_(self, server, channel, author, message):
        await self.displayMeme(channel, 'fetch', message)

    async def _success_(self, server, channel, author, message):
        await self.displayMeme(channel, 'success', message)

    async def _ski_(self, server, channel, author, message):
        await self.displayMeme(channel, 'ski', message)

    async def _officespace_(self, server, channel, author, message):
        await self.displayMeme(channel, 'officespace', message)

    async def _interesting_(self, server, channel, author, message):
        await self.displayMeme(channel, 'interesting', message)

    async def _toohigh_(self, server, channel, author, message):
        await self.displayMeme(channel, 'toohigh', message)

    async def _bs_(self, server, channel, author, message):
        await self.displayMeme(channel, 'bs', message)

    async def _center_(self, server, channel, author, message):
        await self.displayMeme(channel, 'center', message)

    async def _both_(self, server, channel, author, message):
        await self.displayMeme(channel, 'both', message)

    async def _winter_(self, server, channel, author, message):
        await self.displayMeme(channel, 'winter', message)

    async def _xy_(self, server, channel, author, message):
        await self.displayMeme(channel, 'xy', message)

    async def _buzz_(self, server, channel, author, message):
        await self.displayMeme(channel, 'buzz', message)

    async def _yodawg_(self, server, channel, author, message):
        await self.displayMeme(channel, 'yodawg', message)

    async def _yuno_(self, server, channel, author, message):
        await self.displayMeme(channel, 'yuno', message)

    async def _yallgot_(self, server, channel, author, message):
        await self.displayMeme(channel, 'yallgot', message)

    async def _bad_(self, server, channel, author, message):
        await self.displayMeme(channel, 'bad', message)

    async def _elf_(self, server, channel, author, message):
        await self.displayMeme(channel, 'elf', message)

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

        f = urllib.request.urlopen(request)
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
