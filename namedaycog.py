import discord
import json
import datetime
import os
import re
from discord.ext import commands

def findName(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

class Namedaycog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def vd(self, ctx, msg:str=None):
        ''' Reply with todays name-days '''
        path = os.path.dirname(os.path.realpath(__file__))
        t = datetime.datetime.now()
        vd = json.loads(open("%s/namedays.json" % (path)).read())
        if msg is None:
            await self.bot.say("[VDiena] - [Šodien: '%s', Neiekļautie: '%s'] - %s" % (vd["namedays"][int(t.strftime('%j'))]["names"], vd["namedays"][int(t.strftime('%j'))]["noncalendarnames"], t.strftime('%d.%m.%Y')))
        elif msg.lower() == "help":
             await self.bot.say("```\n!vd - Šodienas vārda dienu jubilāri\n!vd [vārds] - Datums kurā [vārds] svin vārda dienu```")
        else:
            nameFound = False
            for day in vd["namedays"]:
                if findName(msg)(day["names"]):
                    await self.bot.say("[VDiena] %s vārda dienu svin %s.%s." % (msg.title(), day["day"], day["month"]))
                    nameFound = True
            if not nameFound:
                await self.bot.say('[VDiena] - Vārds "%s" netika atrasts' % (msg))



def setup(bot):
    bot.add_cog(Namedaycog(bot))
