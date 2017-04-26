import discord
import json
import datetime
import os
from discord.ext import commands

class Namedaycog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def vd(self):
        ''' Reply with todays name-days '''
        path = os.path.dirname(os.path.realpath(__file__))
        t = datetime.datetime.now()
        vd = json.loads(open("%s/namedays.json" % (path)).read())
        await self.bot.say("[VDiena] - [Šodien: '%s', Neiekļautie: '%s'] - %s" % (vd["namedays"][int(t.strftime('%j'))]["names"], vd["namedays"][int(t.strftime('%j'))]["noncalendarnames"], t.strftime('%d.%m.%Y')))

def setup(bot):
    bot.add_cog(Namedaycog(bot))
