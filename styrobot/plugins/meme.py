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
        """
        Generate a 10 Guy meme.
        `!meme tenguy <message>`
        **Example with top & bottom text:** `!meme tenguy top text:bottom text`
        **Example with top text:** `!meme tenguy text displayed on top`
        """

        await self.displayMeme(channel, 'tenguy', message)

    @styrobot.plugincommand('Afraid to Ask Andy', name='afraid')
    async def _afraid_(self, server, channel, author, message):
        """
        Generate an Afraid to Ask Andy meme.
        `!meme afraid <message>`
        **Example with top & bottom text:** `!meme afraid top text:bottom text`
        **Example with top text:** `!meme afraid text displayed on top`
        """

        await self.displayMeme(channel, 'afraid', message)

    @styrobot.plugincommand('An Older Code Sir, But It Checks Out', name='older')
    async def _older_(self, server, channel, author, message):
        """
        Generate An Older Code Sir, But It Checks Out meme.
        `!meme older <message>`
        **Example with top & bottom text:** `!meme older top text:bottom text`
        **Example with top text:** `!meme older text displayed on top`
        """

        await self.displayMeme(channel, 'older', message)

    @styrobot.plugincommand('Ancient Aliens Guy', name='aag')
    async def _aag_(self, server, channel, author, message):
        """
        Generate an Ancient Aliens Guy meme.
        `!meme aag <message>`
        **Example with top & bottom text:** `!meme aag top text:bottom text`
        **Example with top text:** `!meme aag text displayed on top`
        """

        await self.displayMeme(channel, 'aag', message)

    @styrobot.plugincommand('At Least You Tried', name='tried')
    async def _tried_(self, server, channel, author, message):
        """
        Generate an At Least You Tried meme.
        `!meme tried <message>`
        **Example with top & bottom text:** `!meme tried top text:bottom text`
        **Example with top text:** `!meme tried text displayed on top`
        """

        await self.displayMeme(channel, 'tried', message)

    @styrobot.plugincommand('Baby Insanity Wolf', name='biw')
    async def _biw_(self, server, channel, author, message):
        """
        Generate a Baby Insanity Wolf meme.
        `!meme biw <message>`
        **Example with top & bottom text:** `!meme biw top text:bottom text`
        **Example with top text:** `!meme biw text displayed on top`
        """

        await self.displayMeme(channel, 'biw', message)

    @styrobot.plugincommand('Bad Luck Brian', name='blb')
    async def _blb_(self, server, channel, author, message):
        """
        Generate a Bad Luck Brian meme.
        `!meme blb <message>`
        **Example with top & bottom text:** `!meme blb top text:bottom text`
        **Example with top text:** `!meme blb text displayed on top`
        """

        await self.displayMeme(channel, 'blb', message)

    @styrobot.plugincommand('But That\'s None of My Business', name='kermit')
    async def _kermit_(self, server, channel, author, message):
        """
        Generate a But That's None of My Business meme.
        `!meme kermit <message>`
        **Example with top & bottom text:** `!meme kermit top text:bottom text`
        **Example with top text:** `!meme kermit text displayed on top`
        """

        await self.displayMeme(channel, 'kermit', message)

    @styrobot.plugincommand('Butthurt Dweller', name='bd')
    async def _bd_(self, server, channel, author, message):
        """
        Generate a Butthurt Dweller meme.
        `!meme bd <message>`
        **Example with top & bottom text:** `!meme bd top text:bottom text`
        **Example with top text:** `!meme bd text displayed on top`
        """

        await self.displayMeme(channel, 'bd', message)

    @styrobot.plugincommand('Captain Hindsight', name='ch')
    async def _ch_(self, server, channel, author, message):
        """
        Generate a Captain Hindsight meme.
        `!meme ch <message>`
        **Example with top & bottom text:** `!meme ch top text:bottom text`
        **Example with top text:** `!meme ch text displayed on top`
        """

        await self.displayMeme(channel, 'ch', message)

    @styrobot.plugincommand('Comic Book Guy', name='cbg')
    async def _cbg_(self, server, channel, author, message):
        """
        Generate a Comic Book Guy meme.
        `!meme cbg <message>`
        **Example with top & bottom text:** `!meme cbg top text:bottom text`
        **Example with top text:** `!meme cbg text displayed on top`
        """

        await self.displayMeme(channel, 'cbg', message)

    @styrobot.plugincommand('Condescending Wonka', name='wonka')
    async def _wonka_(self, server, channel, author, message):
        """
        Generate a Condescending Wonka meme.
        `!meme wonka <message>`
        **Example with top & bottom text:** `!meme wonka top text:bottom text`
        **Example with top text:** `!meme wonka text displayed on top`
        """

        await self.displayMeme(channel, 'wonka', message)

    @styrobot.plugincommand('Confession Bear', name='cb')
    async def _cb_(self, server, channel, author, message):
        """
        Generate a Confession Bear meme.
        `!meme cb <message>`
        **Example with top & bottom text:** `!meme cb top text:bottom text`
        **Example with top text:** `!meme cb text displayed on top`
        """

        await self.displayMeme(channel, 'cb', message)

    @styrobot.plugincommand('Conspiracy Keanu', name='keanu')
    async def _keanu_(self, server, channel, author, message):
        """
        Generate a Conspiracy Keanu meme.
        `!meme keanu <message>`
        **Example with top & bottom text:** `!meme keanu top text:bottom text`
        **Example with top text:** `!meme keanu text displayed on top`
        """

        await self.displayMeme(channel, 'keanu', message)

    @styrobot.plugincommand('Dating Site Murderer', name='dsm')
    async def _dsm_(self, server, channel, author, message):
        """
        Generate a Dating Site Murderer meme.
        `!meme dsm <message>`
        **Example with top & bottom text:** `!meme dsm top text:bottom text`
        **Example with top text:** `!meme dsm text displayed on top`
        """

        await self.displayMeme(channel, 'dsm', message)

    @styrobot.plugincommand('Do It Live!', name='live')
    async def _live_(self, server, channel, author, message):
        """
        Generate a Do It Live! meme.
        `!meme live <message>`
        **Example with top & bottom text:** `!meme live top text:bottom text`
        **Example with top text:** `!meme live text displayed on top`
        """

        await self.displayMeme(channel, 'live', message)

    @styrobot.plugincommand('Do You Want Ants?', name='ants')
    async def _ants_(self, server, channel, author, message):
        """
        Generate a Do You Want Ants? meme.
        `!meme ants <message>`
        **Example with top & bottom text:** `!meme ants top text:bottom text`
        **Example with top text:** `!meme ants text displayed on top`
        """

        await self.displayMeme(channel, 'ants', message)

    @styrobot.plugincommand('Doge', name='doge')
    async def _doge_(self, server, channel, author, message):
        """
        Generate a Doge meme.
        `!meme doge <message>`
        **Example with top & bottom text:** `!meme doge top text:bottom text`
        **Example with top text:** `!meme doge text displayed on top`
        """

        await self.displayMeme(channel, 'doge', message)

    @styrobot.plugincommand('Drake Always On Beat', name='alwaysonbeat')
    async def _alwaysonbeat_(self, server, channel, author, message):
        """
        Generate a Drake Always On Beat meme.
        `!meme alwaysonbeat <message>`
        **Example with top & bottom text:** `!meme alwaysonbeat top text:bottom text`
        **Example with top text:** `!meme alwaysonbeat text displayed on top`
        """

        await self.displayMeme(channel, 'alwaysonbeat', message)

    @styrobot.plugincommand('Ermahgerd', name='ermg')
    async def _ermg_(self, server, channel, author, message):
        """
        Generate an Ermahgerd meme.
        `!meme ermg <message>`
        **Example with top & bottom text:** `!meme ermg top text:bottom text`
        **Example with top text:** `!meme ermg text displayed on top`
        """

        await self.displayMeme(channel, 'ermg', message)

    @styrobot.plugincommand('Facepalm', name='facepalm')
    async def _facepalm_(self, server, channel, author, message):
        """
        Generate a Facepalm meme.
        `!meme facepalm <message>`
        **Example with top & bottom text:** `!meme facepalm top text:bottom text`
        **Example with top text:** `!meme facepalm text displayed on top`
        """

        await self.displayMeme(channel, 'facepalm', message)

    @styrobot.plugincommand('First World Problems', name='fwp')
    async def _fwp_(self, server, channel, author, message):
        """
        Generate a First World Problems meme.
        `!meme fwp <message>`
        **Example with top & bottom text:** `!meme fwp top text:bottom text`
        **Example with top text:** `!meme fwp text displayed on top`
        """

        await self.displayMeme(channel, 'fwp', message)

    @styrobot.plugincommand('Forever Alone', name='fa')
    async def _fa_(self, server, channel, author, message):
        """
        Generate a Forever Alone meme.
        `!meme fa <message>`
        **Example with top & bottom text:** `!meme fa top text:bottom text`
        **Example with top text:** `!meme fa text displayed on top`
        """

        await self.displayMeme(channel, 'fa', message)

    @styrobot.plugincommand('Foul Bachelor Frog', name='fbf')
    async def _fbf_(self, server, channel, author, message):
        """
        Generate a Foul Bachelor Frog meme.
        `!meme fbf <message>`
        **Example with top & bottom text:** `!meme fbf top text:bottom text`
        **Example with top text:** `!meme fbf text displayed on top`
        """

        await self.displayMeme(channel, 'fbf', message)

    @styrobot.plugincommand('Fuck Me, Right?', name='fmr')
    async def _fmr_(self, server, channel, author, message):
        """
        Generate a Fuck Me, Right? meme.
        `!meme fmr <message>`
        **Example with top & bottom text:** `!meme fmr top text:bottom text`
        **Example with top text:** `!meme fmr text displayed on top`
        """

        await self.displayMeme(channel, 'fmr', message)

    @styrobot.plugincommand('Futurama Fry', name='fry')
    async def _fry_(self, server, channel, author, message):
        """
        Generate a Futurama Fry meme.
        `!meme fry <message>`
        **Example with top & bottom text:** `!meme fry top text:bottom text`
        **Example with top text:** `!meme fry text displayed on top`
        """

        await self.displayMeme(channel, 'fry', message)

    @styrobot.plugincommand('Good Guy Greg', name='ggg')
    async def _ggg_(self, server, channel, author, message):
        """
        Generate a Good Guy Greg meme.
        `!meme ggg <message>`
        **Example with top & bottom text:** `!meme ggg top text:bottom text`
        **Example with top text:** `!meme ggg text displayed on top`
        """

        await self.displayMeme(channel, 'ggg', message)

    @styrobot.plugincommand('Hipster Barista', name='hipster')
    async def _hipster_(self, server, channel, author, message):
        """
        Generate a Hipster Barista meme.
        `!meme hipster <message>`
        **Example with top & bottom text:** `!meme hipster top text:bottom text`
        **Example with top text:** `!meme hipster text displayed on top`
        """

        await self.displayMeme(channel, 'hipster', message)

    @styrobot.plugincommand('I Can Has Cheezburger?', name='icanhas')
    async def _icanhas_(self, server, channel, author, message):
        """
        Generate an I Can Has Cheezburger? meme.
        `!meme icanhas <message>`
        **Example with top & bottom text:** `!meme icanhas top text:bottom text`
        **Example with top text:** `!meme icanhas text displayed on top`
        """

        await self.displayMeme(channel, 'icanhas', message)

    @styrobot.plugincommand('I Feel Like I\'m Taking Crazy Pills', name='crazypills')
    async def _crazypills_(self, server, channel, author, message):
        """
        Generate an I Feel Like I'm Taking Crazy Pills meme.
        `!meme crazypills <message>`
        **Example with top & bottom text:** `!meme crazypills top text:bottom text`
        **Example with top text:** `!meme crazypills text displayed on top`
        """

        await self.displayMeme(channel, 'crazypills', message)

    @styrobot.plugincommand('I Guarantee It', name='mw')
    async def _mw_(self, server, channel, author, message):
        """
        Generate an I Guarantee It meme.
        `!meme mw <message>`
        **Example with top & bottom text:** `!meme mw top text:bottom text`
        **Example with top text:** `!meme mw text displayed on top`
        """

        await self.displayMeme(channel, 'mw', message)

    @styrobot.plugincommand('I Have No Idea What I\'m Doing', name='noidea')
    async def _noidea_(self, server, channel, author, message):
        """
        Generate an I Have No Idea What I'm Doing meme.
        `!meme noidea <message>`
        **Example with top & bottom text:** `!meme noidea top text:bottom text`
        **Example with top text:** `!meme noidea text displayed on top`
        """

        await self.displayMeme(channel, 'noidea', message)

    @styrobot.plugincommand('I Immediately Regret This Decision!', name='regret')
    async def _regret_(self, server, channel, author, message):
        """
        Generate an I Immediately Regret This Decision! meme.
        `!meme regret <message>`
        **Example with top & bottom text:** `!meme regret top text:bottom text`
        **Example with top text:** `!meme regret text displayed on top`
        """

        await self.displayMeme(channel, 'regret', message)

    @styrobot.plugincommand('I Should Buy a Boat Cat', name='boat')
    async def _boat_(self, server, channel, author, message):
        """
        Generate an I Should Buy a Boat Cat meme.
        `!meme boat <message>`
        **Example with top & bottom text:** `!meme boat top text:bottom text`
        **Example with top text:** `!meme boat text displayed on top`
        """

        await self.displayMeme(channel, 'boat', message)

    @styrobot.plugincommand('I Should Not Have Said That', name='hagrid')
    async def _hagrid_(self, server, channel, author, message):
        """
        Generate an I Should Not Have Said That meme.
        `!meme hagrid <message>`
        **Example with top & bottom text:** `!meme hagrid top text:bottom text`
        **Example with top text:** `!meme hagrid text displayed on top`
        """

        await self.displayMeme(channel, 'hagrid', message)

    @styrobot.plugincommand('I Would Be So Happy', name='sohappy')
    async def _sohappy_(self, server, channel, author, message):
        """
        Generate an I Would Be So Happy meme.
        `!meme sohappy <message>`
        **Example with top & bottom text:** `!meme sohappy top text:bottom text`
        **Example with top text:** `!meme sohappy text displayed on top`
        """

        await self.displayMeme(channel, 'sohappy', message)

    @styrobot.plugincommand('I am the Captain Now', name='captain')
    async def _captain_(self, server, channel, author, message):
        """
        Generate an I Would Be So Happy meme.
        `!meme captain <message>`
        **Example with top & bottom text:** `!meme captain top text:bottom text`
        **Example with top text:** `!meme captain text displayed on top`
        """

        await self.displayMeme(channel, 'captain', message)

    @styrobot.plugincommand('Inigo Montoya', name='inigo')
    async def _inigo_(self, server, channel, author, message):
        """
        Generate an Inigo Montoya meme.
        `!meme inigo <message>`
        **Example with top & bottom text:** `!meme inigo top text:bottom text`
        **Example with top text:** `!meme inigo text displayed on top`
        """

        await self.displayMeme(channel, 'inigo', message)

    @styrobot.plugincommand('Insanity Wolf', name='iw')
    async def _iw_(self, server, channel, author, message):
        """
        Generate an Insanity Wolf meme.
        `!meme iw <message>`
        **Example with top & bottom text:** `!meme iw top text:bottom text`
        **Example with top text:** `!meme iw text displayed on top`
        """

        await self.displayMeme(channel, 'iw', message)

    @styrobot.plugincommand('It\'s A Trap!', name='ackbar')
    async def _ackbar_(self, server, channel, author, message):
        """
        Generate an It's A Trap! meme.
        `!meme ackbar <message>`
        **Example with top & bottom text:** `!meme ackbar top text:bottom text`
        **Example with top text:** `!meme ackbar text displayed on top`
        """

        await self.displayMeme(channel, 'ackbar', message)

    @styrobot.plugincommand('It\'s Happening', name='happening')
    async def _happening_(self, server, channel, author, message):
        """
        Generate an It's Happening meme.
        `!meme happening <message>`
        **Example with top & bottom text:** `!meme happening top text:bottom text`
        **Example with top text:** `!meme happening text displayed on top`
        """

        await self.displayMeme(channel, 'happening', message)

    @styrobot.plugincommand('It\'s Simple, Kill the Batman', name='joker')
    async def _joker_(self, server, channel, author, message):
        """
        Generate an It's Simple, Kill the Batman meme.
        `!meme joker <message>`
        **Example with top & bottom text:** `!meme joker top text:bottom text`
        **Example with top text:** `!meme joker text displayed on top`
        """

        await self.displayMeme(channel, 'joker', message)

    @styrobot.plugincommand('Jony Ive Redesigns Things', name='ive')
    async def _ive_(self, server, channel, author, message):
        """
        Generate a Jony Ive Redesigns Things meme.
        `!meme ive <message>`
        **Example with top & bottom text:** `!meme ive top text:bottom text`
        **Example with top text:** `!meme ive text displayed on top`
        """

        await self.displayMeme(channel, 'ive', message)

    @styrobot.plugincommand('Laughing Lizard', name='ll')
    async def _ll_(self, server, channel, author, message):
        """
        Generate a Laughing Lizard meme.
        `!meme ll <message>`
        **Example with top & bottom text:** `!meme ll top text:bottom text`
        **Example with top text:** `!meme ll text displayed on top`
        """

        await self.displayMeme(channel, 'll', message)

    @styrobot.plugincommand('Matrix Morpheus', name='morpheus')
    async def _morpheus_(self, server, channel, author, message):
        """
        Generate a Matrix Morpheus meme.
        `!meme morpheus <message>`
        **Example with top & bottom text:** `!meme morpheus top text:bottom text`
        **Example with top text:** `!meme morpheus text displayed on top`
        """

        await self.displayMeme(channel, 'morpheus', message)

    @styrobot.plugincommand('Milk Was a Bad Choice', name='badchoice')
    async def _badchoice_(self, server, channel, author, message):
        """
        Generate a Milk Was a Bad Choice meme.
        `!meme badchoice <message>`
        **Example with top & bottom text:** `!meme badchoice top text:bottom text`
        **Example with top text:** `!meme badchoice text displayed on top`
        """

        await self.displayMeme(channel, 'badchoice', message)

    @styrobot.plugincommand('Minor Mistake Marvin', name='mmm')
    async def _mmm_(self, server, channel, author, message):
        """
        Generate a Minor Mistake Marvin meme.
        `!meme mmm <message>`
        **Example with top & bottom text:** `!meme mmm top text:bottom text`
        **Example with top text:** `!meme mmm text displayed on top`
        """

        await self.displayMeme(channel, 'mmm', message)

    @styrobot.plugincommand('Nothing To Do Here', name='jetpack')
    async def _jetpack_(self, server, channel, author, message):
        """
        Generate a Nothing To Do Here meme.
        `!meme jetpack <message>`
        **Example with top & bottom text:** `!meme jetpack top text:bottom text`
        **Example with top text:** `!meme jetpack text displayed on top`
        """

        await self.displayMeme(channel, 'jetpack', message)

    @styrobot.plugincommand('Oh, I\'m Sorry, I Thought This Was America', name='imsorry')
    async def _imsorry_(self, server, channel, author, message):
        """
        Generate an Oh, I'm Sorry, I Thought This Was America meme.
        `!meme imsorry <message>`
        **Example with top & bottom text:** `!meme imsorry top text:bottom text`
        **Example with top text:** `!meme imsorry text displayed on top`
        """

        await self.displayMeme(channel, 'imsorry', message)

    @styrobot.plugincommand('Oh, Is That What We\'re Going to Do Today?', name='red')
    async def _red_(self, server, channel, author, message):
        """
        Generate an Oh, Is That What We're Going to Do Today? meme.
        `!meme red <message>`
        **Example with top & bottom text:** `!meme red top text:bottom text`
        **Example with top text:** `!meme red text displayed on top`
        """

        await self.displayMeme(channel, 'red', message)

    @styrobot.plugincommand('One Does Not Simply Walk into Mordor', name='mordor')
    async def _mordor_(self, server, channel, author, message):
        """
        Generate an One Does Not Simply Walk into Mordor meme.
        `!meme mordor <message>`
        **Example with top & bottom text:** `!meme mordor one does not simply:walk into mordor`
        **Example with top text:** `!meme mordor one does not simply walk into mordor`
        """

        await self.displayMeme(channel, 'mordor', message)

    @styrobot.plugincommand('Oprah You Get a Car', name='oprah')
    async def _oprah_(self, server, channel, author, message):
        """
        Generate an Oprah You Get a Car meme.
        `!meme oprah <message>`
        **Example with top & bottom text:** `!meme oprah top text:bottom text`
        **Example with top text:** `!meme oprah text displayed on top`
        """

        await self.displayMeme(channel, 'oprah', message)

    @styrobot.plugincommand('Overly Attached Girlfriend', name='oag')
    async def _oag_(self, server, channel, author, message):
        """
        Generate an Overly Attached Girlfriend meme.
        `!meme oag <message>`
        **Example with top & bottom text:** `!meme oag top text:bottom text`
        **Example with top text:** `!meme oag text displayed on top`
        """

        await self.displayMeme(channel, 'oag', message)

    @styrobot.plugincommand('Pepperidge Farm Remembers', name='remembers')
    async def _remembers_(self, server, channel, author, message):
        """
        Generate a Pepperidge Farm Remembers meme.
        `!meme remembers <message>`
        **Example with top & bottom text:** `!meme remembers top text:bottom text`
        **Example with top text:** `!meme remembers text displayed on top`
        """

        await self.displayMeme(channel, 'remembers', message)

    @styrobot.plugincommand('Philosoraptor', name='philosoraptor')
    async def _philosoraptor_(self, server, channel, author, message):
        """
        Generate a Philosoraptor meme.
        `!meme philosoraptor <message>`
        **Example with top & bottom text:** `!meme philosoraptor top text:bottom text`
        **Example with top text:** `!meme philosoraptor text displayed on top`
        """

        await self.displayMeme(channel, 'philosoraptor', message)

    @styrobot.plugincommand('Probably Not a Good Idea', name='jw')
    async def _jw_(self, server, channel, author, message):
        """
        Generate a Probably Not a Good Idea meme.
        `!meme jw <message>`
        **Example with top & bottom text:** `!meme jw top text:bottom text`
        **Example with top text:** `!meme jw text displayed on top`
        """

        await self.displayMeme(channel, 'jw', message)

    @styrobot.plugincommand('Push it somewhere else Patrick', name='patrick')
    async def _patrick_(self, server, channel, author, message):
        """
        Generate a Push it somewhere else Patrick meme.
        `!meme patrick <message>`
        **Example with top & bottom text:** `!meme patrick top text:bottom text`
        **Example with top text:** `!meme patrick text displayed on top`
        """

        await self.displayMeme(channel, 'patrick', message)

    @styrobot.plugincommand('Sad Barack Obama', name='sad-obama')
    async def _sadobama_(self, server, channel, author, message):
        """
        Generate a Sad Barack Obama meme.
        `!meme sadobama <message>`
        **Example with top & bottom text:** `!meme sadobama top text:bottom text`
        **Example with top text:** `!meme sadobama text displayed on top`
        """

        await self.displayMeme(channel, 'sad-obama', message)

    @styrobot.plugincommand('Sad Bill Clinton', name='sad-clinton')
    async def _sadclinton_(self, server, channel, author, message):
        """
        Generate a Sad Bill Clinton meme.
        `!meme sadclinton <message>`
        **Example with top & bottom text:** `!meme sadclinton top text:bottom text`
        **Example with top text:** `!meme sadclinton text displayed on top`
        """

        await self.displayMeme(channel, 'sad-clinton', message)

    @styrobot.plugincommand('Sad Frog / Feels Bad Man', name='sadfrog')
    async def _sadfrog_(self, server, channel, author, message):
        """
        Generate a Sad Frog / Feels Bad Man meme.
        `!meme sadfrog <message>`
        **Example with top & bottom text:** `!meme sadfrog top text:bottom text`
        **Example with top text:** `!meme sadfrog text displayed on top`
        """

        await self.displayMeme(channel, 'sadfrog', message)

    @styrobot.plugincommand('Sad George Bush', name='sad-bush')
    async def _sadbush_(self, server, channel, author, message):
        """
        Generate a Sad George Bush meme.
        `!meme sadbush <message>`
        **Example with top & bottom text:** `!meme sadbush top text:bottom text`
        **Example with top text:** `!meme sadbush text displayed on top`
        """

        await self.displayMeme(channel, 'sad-bush', message)

    @styrobot.plugincommand('Sad Joe Biden', name='sad-biden')
    async def _sadbiden_(self, server, channel, author, message):
        """
        Generate a Sad Joe Biden meme.
        `!meme sadbiden <message>`
        **Example with top & bottom text:** `!meme sadbiden top text:bottom text`
        **Example with top text:** `!meme sadbiden text displayed on top`
        """

        await self.displayMeme(channel, 'sad-biden', message)

    @styrobot.plugincommand('Sad John Boehner', name='sad-boehner')
    async def _sadboehner_(self, server, channel, author, message):
        """
        Generate a Sad John Boehner meme.
        `!meme sadboehner <message>`
        **Example with top & bottom text:** `!meme sadboehner top text:bottom text`
        **Example with top text:** `!meme sadboehner text displayed on top`
        """

        await self.displayMeme(channel, 'sad-boehner', message)

    @styrobot.plugincommand('Sarcastic Bear', name='sarcasticbear')
    async def _sarcasticbear_(self, server, channel, author, message):
        """
        Generate a Sarcastic Bear meme.
        `!meme sarcasticbear <message>`
        **Example with top & bottom text:** `!meme sarcasticbear top text:bottom text`
        **Example with top text:** `!meme sarcasticbear text displayed on top`
        """

        await self.displayMeme(channel, 'sarcasticbear', message)

    @styrobot.plugincommand('Schrute Facts', name='dwight')
    async def _dwight_(self, server, channel, author, message):
        """
        Generate a Schrute Facts meme.
        `!meme dwight <message>`
        **Example with top & bottom text:** `!meme dwight top text:bottom text`
        **Example with top text:** `!meme dwight text displayed on top`
        """

        await self.displayMeme(channel, 'dwight', message)

    @styrobot.plugincommand('Scumbag Brain', name='sb')
    async def _sb_(self, server, channel, author, message):
        """
        Generate a Scumbag Brain meme.
        `!meme sb <message>`
        **Example with top & bottom text:** `!meme sb top text:bottom text`
        **Example with top text:** `!meme sb text displayed on top`
        """

        await self.displayMeme(channel, 'sb', message)

    @styrobot.plugincommand('Scumbag Steve', name='ss')
    async def _ss_(self, server, channel, author, message):
        """
        Generate a Scumbag Steve meme.
        `!meme ss <message>`
        **Example with top & bottom text:** `!meme ss top text:bottom text`
        **Example with top text:** `!meme ss text displayed on top`
        """

        await self.displayMeme(channel, 'ss', message)

    @styrobot.plugincommand('Sealed Fate', name='sf')
    async def _sf_(self, server, channel, author, message):
        """
        Generate a Sealed Fate meme.
        `!meme sf <message>`
        **Example with top & bottom text:** `!meme sf top text:bottom text`
        **Example with top text:** `!meme sf text displayed on top`
        """

        await self.displayMeme(channel, 'sf', message)

    @styrobot.plugincommand('See? Nobody Cares', name='dodgson')
    async def _dodgson_(self, server, channel, author, message):
        """
        Generate a See? Nobody Cares meme.
        `!meme dodgson <message>`
        **Example with top & bottom text:** `!meme dodgson top text:bottom text`
        **Example with top text:** `!meme dodgson text displayed on top`
        """

        await self.displayMeme(channel, 'dodgson', message)

    @styrobot.plugincommand('Shut Up and Take My Money!', name='money')
    async def _money_(self, server, channel, author, message):
        """
        Generate a Shut Up and Take My Money! meme.
        `!meme money <message>`
        **Example with top & bottom text:** `!meme money top text:bottom text`
        **Example with top text:** `!meme money text displayed on top`
        """

        await self.displayMeme(channel, 'money', message)

    @styrobot.plugincommand('So Hot Right Now', name='sohot')
    async def _sohot_(self, server, channel, author, message):
        """
        Generate a So Hot Right Now meme.
        `!meme sohot <message>`
        **Example with top & bottom text:** `!meme sohot top text:bottom text`
        **Example with top text:** `!meme sohot text displayed on top`
        """

        await self.displayMeme(channel, 'sohot', message)

    @styrobot.plugincommand('So I Got That Goin\' For Me, Which is Nice', name='goinforme')
    async def _goinforme_(self, server, channel, author, message):
        """
        Generate a So I Got That Goin' For Me, Which is Nice meme.
        `!meme goinforme <message>`
        **Example with top & bottom text:** `!meme goinforme top text:bottom text`
        **Example with top text:** `!meme goinforme text displayed on top`
        """

        await self.displayMeme(channel, 'goinforme', message)

    @styrobot.plugincommand('Socially Awesome Awkward Penguin', name='awesome-awkward')
    async def _awesomeawkward_(self, server, channel, author, message):
        """
        Generate a Socially Awesome Awkward Penguin meme.
        `!meme awesomeawkward <message>`
        **Example with top & bottom text:** `!meme awesomeawkward top text:bottom text`
        **Example with top text:** `!meme awesomeawkward text displayed on top`
        """

        await self.displayMeme(channel, 'awesome-awkward', message)

    @styrobot.plugincommand('Socially Awesome Penguin', name='awesome')
    async def _awesome_(self, server, channel, author, message):
        """
        Generate a Socially Awesome Penguin meme.
        `!meme awesome <message>`
        **Example with top & bottom text:** `!meme awesome top text:bottom text`
        **Example with top text:** `!meme awesome text displayed on top`
        """

        await self.displayMeme(channel, 'awesome', message)

    @styrobot.plugincommand('Socially Awkward Awesome Penguin', name='awkward-awesome')
    async def _awkwardawesome_(self, server, channel, author, message):
        """
        Generate a Socially Awkward Awesome Penguin meme.
        `!meme awkwardawesome <message>`
        **Example with top & bottom text:** `!meme awkwardawesome top text:bottom text`
        **Example with top text:** `!meme awkwardawesome text displayed on top`
        """

        await self.displayMeme(channel, 'awkward-awesome', message)

    @styrobot.plugincommand('Socially Awkward Penguin', name='awkward')
    async def _awkward_(self, server, channel, author, message):
        """
        Generate a Socially Awkward Penguin meme.
        `!meme awkward <message>`
        **Example with top & bottom text:** `!meme awkward top text:bottom text`
        **Example with top text:** `!meme awkward text displayed on top`
        """

        await self.displayMeme(channel, 'awkward', message)

    @styrobot.plugincommand('Stop Trying to Make Fetch Happen', name='fetch')
    async def _fetch_(self, server, channel, author, message):
        """
        Generate a Stop Trying to Make Fetch Happen meme.
        `!meme fetch <message>`
        **Example with top & bottom text:** `!meme fetch top text:bottom text`
        **Example with top text:** `!meme fetch text displayed on top`
        """

        await self.displayMeme(channel, 'fetch', message)

    @styrobot.plugincommand('Success Kid', name='success')
    async def _success_(self, server, channel, author, message):
        """
        Generate a Success Kid meme.
        `!meme success <message>`
        **Example with top & bottom text:** `!meme success top text:bottom text`
        **Example with top text:** `!meme success text displayed on top`
        """

        await self.displayMeme(channel, 'success', message)

    @styrobot.plugincommand('Super Cool Ski Instructor', name='ski')
    async def _ski_(self, server, channel, author, message):
        """
        Generate a Super Cool Ski Instructor meme.
        `!meme ski <message>`
        **Example with top & bottom text:** `!meme ski top text:bottom text`
        **Example with top text:** `!meme ski text displayed on top`
        """

        await self.displayMeme(channel, 'ski', message)

    @styrobot.plugincommand('That Would Be Great', name='officespace')
    async def _officespace_(self, server, channel, author, message):
        """
        Generate a That Would Be Great meme.
        `!meme officespace <message>`
        **Example with top & bottom text:** `!meme officespace top text:bottom text`
        **Example with top text:** `!meme officespace text displayed on top`
        """

        await self.displayMeme(channel, 'officespace', message)

    @styrobot.plugincommand('The Most Interesting Man in the World', name='interesting')
    async def _interesting_(self, server, channel, author, message):
        """
        Generate a The Most Interesting Man in the World meme.
        `!meme interesting <message>`
        **Example with top & bottom text:** `!meme interesting top text:bottom text`
        **Example with top text:** `!meme interesting text displayed on top`
        """

        await self.displayMeme(channel, 'interesting', message)

    @styrobot.plugincommand('The Rent Is Too Damn High', name='toohigh')
    async def _toohigh_(self, server, channel, author, message):
        """
        Generate a The Rent Is Too Damn High meme.
        `!meme toohigh <message>`
        **Example with top & bottom text:** `!meme toohigh top text:bottom text`
        **Example with top text:** `!meme toohigh text displayed on top`
        """

        await self.displayMeme(channel, 'toohigh', message)

    @styrobot.plugincommand('This is Bull, Shark', name='bs')
    async def _bs_(self, server, channel, author, message):
        """
        Generate a This is Bull, Shark meme.
        `!meme bs <message>`
        **Example with top & bottom text:** `!meme bs top text:bottom text`
        **Example with top text:** `!meme bs text displayed on top`
        """

        await self.displayMeme(channel, 'bs', message)

    @styrobot.plugincommand('What is this, a Center for Ants?!', name='center')
    async def _center_(self, server, channel, author, message):
        """
        Generate a This is Bull, Shark meme.
        `!meme bs <message>`
        **Example with top & bottom text:** `!meme bs top text:bottom text`
        **Example with top text:** `!meme bs text displayed on top`
        """

        await self.displayMeme(channel, 'center', message)

    @styrobot.plugincommand('Why Not Both?', name='both')
    async def _both_(self, server, channel, author, message):
        """
        Generate a Why Not Both? meme.
        `!meme both <message>`
        **Example with top & bottom text:** `!meme both top text:bottom text`
        **Example with top text:** `!meme both text displayed on top`
        """

        await self.displayMeme(channel, 'both', message)

    @styrobot.plugincommand('Winter is coming', name='winter')
    async def _winter_(self, server, channel, author, message):
        """
        Generate a Winter is coming meme.
        `!meme winter <message>`
        **Example with top & bottom text:** `!meme winter top text:bottom text`
        **Example with top text:** `!meme winter text displayed on top`
        """

        await self.displayMeme(channel, 'winter', message)

    @styrobot.plugincommand('X all the Y', name='xy')
    async def _xy_(self, server, channel, author, message):
        """
        Generate a X all the Y meme.
        `!meme xy <message>`
        **Example with top & bottom text:** `!meme xy top text:bottom text`
        **Example with top text:** `!meme xy text displayed on top`
        """

        await self.displayMeme(channel, 'xy', message)

    @styrobot.plugincommand('X, X Everywhere', name='buzz')
    async def _buzz_(self, server, channel, author, message):
        """
        Generate a X, X Everywhere meme.
        `!meme buzz <message>`
        **Example with top & bottom text:** `!meme buzz top text:bottom text`
        **Example with top text:** `!meme buzz text displayed on top`
        """

        await self.displayMeme(channel, 'buzz', message)

    @styrobot.plugincommand('Xzibit Yo Dawg', name='yodawg')
    async def _yodawg_(self, server, channel, author, message):
        """
        Generate a Xzibit Yo Dawg meme.
        `!meme yodawg <message>`
        **Example with top & bottom text:** `!meme yodawg top text:bottom text`
        **Example with top text:** `!meme yodawg text displayed on top`
        """

        await self.displayMeme(channel, 'yodawg', message)

    @styrobot.plugincommand('Y U NO Guy', name='yuno')
    async def _yuno_(self, server, channel, author, message):
        """
        Generate a Y U NO Guy meme.
        `!meme yuno <message>`
        **Example with top & bottom text:** `!meme yuno top text:bottom text`
        **Example with top text:** `!meme yuno text displayed on top`
        """

        await self.displayMeme(channel, 'yuno', message)

    @styrobot.plugincommand('Y\'all Got Any More of Them', name='yallgot')
    async def _yallgot_(self, server, channel, author, message):
        """
        Generate a Y'all Got Any More of Them meme.
        `!meme yallgot <message>`
        **Example with top & bottom text:** `!meme yallgot top text:bottom text`
        **Example with top text:** `!meme yallgot text displayed on top`
        """

        await self.displayMeme(channel, 'yallgot', message)

    @styrobot.plugincommand('You Should Feel Bad', name='bad')
    async def _bad_(self, server, channel, author, message):
        """
        Generate a You Should Feel Bad meme.
        `!meme bad <message>`
        **Example with top & bottom text:** `!meme bad top text:bottom text`
        **Example with top text:** `!meme bad text displayed on top`
        """

        await self.displayMeme(channel, 'bad', message)

    @styrobot.plugincommand('You Sit on a Throne of Lies', name='elf')
    async def _elf_(self, server, channel, author, message):
        """
        Generate a You Sit on a Throne of Lies meme.
        `!meme elf <message>`
        **Example with top & bottom text:** `!meme elf top text:bottom text`
        **Example with top text:** `!meme elf text displayed on top`
        """

        await self.displayMeme(channel, 'elf', message)

    @styrobot.plugincommand('You Were the Chosen One!', name='chosen')
    async def _chosen_(self, server, channel, author, message):
        """
        Generate a You Were the Chosen One! meme.
        `!meme chosen <message>`
        **Example with top & bottom text:** `!meme chosen top text:bottom text`
        **Example with top text:** `!meme chosen text displayed on top`
        """

        await self.displayMeme(channel, 'chosen', message)

    def parseMeme(self, message):
        message = message.replace("?", "")

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
