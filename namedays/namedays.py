import discord
import json
import datetime
import os
import re
from discord.ext import commands
import urllib.request

emoji = ":champagne:"  # Iekļautie
emoji2 = ":beers:"  # Neiekļautie


def findname(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

class Namedays:
    """Reply with todays name-days"""

    def __init__(self, bot):
        self.data = json.loads(open("data/namedays/namedays.json", encoding='utf-8').read())
        self.bot = bot

    @commands.command(pass_context=True)
    async def vd(self, ctx, msg: str = None):
        """
        vd - Atgriež šodienas vārda dienu jubilārus
        vd [vārds] - Atgriež datumu kurā [vārds] svin vārda dienu
        vd [datums] - Atgriež [datums] vārda dienas jubilārus (formāts: dd.mm)
        """
        path = os.path.dirname(os.path.realpath(__file__))
        if os.path.exists('data/namedays/namedays.json'):
            t = datetime.datetime.now()
            vd = self.data
            if msg is None:
                await self.bot.say("%s Šodien vārda dienu svin: `%s`\n\n%s Kalendārā neiekļautie: *`%s`*" % (
                    emoji, vd["namedays"][int(t.strftime('%j'))-1]["names"].replace(" ", ", "), emoji2,
                    vd["namedays"][int(t.strftime('%j'))-1]["noncalendarnames"].replace(" ", ", ")))
            else:
                found = False
                for day in vd["namedays"]:
                    date = "%s.%s" % (day["day"], day["month"])
                    day["date"] = date
                    if findname(msg)(day["names"]):
                        await self.bot.say("%s %s vārda dienu svin %s" % (emoji, msg.title(), date))
                        found = True
                    if findname(msg)(day["noncalendarnames"]):
                        await self.bot.say("%s %s vārda dienu svin %s" % (emoji, msg.title(), date))
                        found = True
                    if msg == day["date"]:
                        if day["noncalendarnames"] == "<NAV_NEVIENS_VĀRDS>":
                            await self.bot.say(
                                "%s %s vārda dienu svin: `%s`" % (emoji, date, day["names"].replace(" ", ", ")))
                        else:
                            await self.bot.say("%s %s vārda dienu svin: `%s`\n\n%s Kalendārā neiekļautie: *`%s`*" % (
                                emoji, date, day["names"].replace(" ", ", "), emoji2,
                                day["noncalendarnames"].replace(" ", ", ")))
                        found = True
                if not found:
                    await self.bot.say('Kļūda - "%s" netika atrasts' % (msg))
        else:
            await self.bot.say('Something went wrong.')

def check_folder():
    if not os.path.exists('data/namedays'):
        print('Creating namedays folder...')
        os.makedirs('data/namedays')

def check_file():
    if not os.path.exists("data/namedays/namedays.json"):
        print('Downloading namedays.json...')
        urllib.request.urlretrieve("https://raw.githubusercontent.com/RichusX/richusx-cogs/master/namedays/namedays.json", "data/namedays/namedays.json")

def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(Namedays(bot))
