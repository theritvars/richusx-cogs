import discord
import json
import datetime
import os
import re
from discord.ext import commands

emoji = ":cake:" # Iekļautie
emoji2 = ":beers:" # Neiekļautie

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
            await self.bot.say("%s Šodien vārda dienu svin: `%s`\n\n%s Kalendārā neiekļautie: *`%s`*" % (emoji, vd["namedays"][int(t.strftime('%j'))]["names"].replace(" ",", "), emoji2, vd["namedays"][int(t.strftime('%j'))]["noncalendarnames"].replace(" ",", ")))
        elif msg.lower() == "help":
             await self.bot.say("```\n%svd - Atgriež šodienas vārda dienu jubilārus\n%svd [vārds] - Atgriež datumu kurā [vārds] svin vārda dienu\n%svd [datums] - Atgriež [datums] vārda dienas jubilārus (formāts: dd.mm)```" % (ctx.prefix, ctx.prefix, ctx.prefix))
        else:
            found = False
            for day in vd["namedays"]:
                date = "%s.%s" % (day["day"], day["month"])
                day["date"] = date
                if findName(msg)(day["names"]):
                    await self.bot.say("%s %s vārda dienu svin %s." % (emoji, msg.title(), date))
                    found = True
                elif msg == day["date"]:
                    if day["noncalendarnames"] == "<NAV_NEVIENS_VĀRDS>":
                        await self.bot.say("%s %s. vārda dienu svin: `%s`" % (emoji, date, day["names"].replace(" ",", ")))
                    else:
                        await self.bot.say("%s %s. vārda dienu svin: `%s`\n\n%s Kalendārā neiekļautie: *`%s`*" % (emoji, date, day["names"].replace(" ",", "), emoji2, day["noncalendarnames"].replace(" ",", ")))
                    found = True
            if not found:
                await self.bot.say('Kļūda - "%s" netika atrasts' % (msg))



def setup(bot):
    bot.add_cog(Namedaycog(bot))
