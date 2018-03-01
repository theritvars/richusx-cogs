import discord
import json
import datetime
import os
import re
from discord.ext import commands
import urllib.request

emoji = ":champagne:"  # Iekļautie
emoji2 = ":beers:"  # Neiekļautie

def findByDate(vd, day, month):
        for i in vd["namedays"]:
            if i["month"] == month:
                if i["day"] == day:
                    return [i["names"], i["noncalendarnames"]]
        return False

def findByName(vd, name):
    for i in vd["namedays"]:
        if name.lower() in i["names"].lower() or name.lower() in i["noncalendarnames"].lower():
            date = "%s/%s" % (i["day"], i["month"])
            return date
    return False

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
        vd [datums] - Atgriež [datums] vārda dienas jubilārus (formāts: dd.mm; dd/mm; dd,mm)
        """

        if msg is not None:
            date_regex = re.match("^(0[1-9]|1[0-9]|2[0-9]|3[0-1])(\.|\/|\,)(0[1-9]|1[1-2])$", msg)

        if msg is None:
            day = datetime.datetime.now().strftime("%d")
            month = datetime.datetime.now().strftime("%m")
            result = findByDate(self.data, day, month)

            if result:
                await self.bot.say("%s Šodien vārda dienu svin: `%s`\n\n%s Kalendārā neiekļautie: *`%s`*" % (
                    emoji, result[0].replace(" ", ", "), emoji2, result[1].replace(" ", ", ")))
            else:
                await self.bot.say("Kļūda! `%s` netika atrasts!" % (msg))

        elif date_regex:
            day = date_regex.group(1)
            month = date_regex.group(3)
            result = findByDate(self.data, day, month)

            if result:
                await self.bot.say("%s Šodien vārda dienu svin: `%s`\n\n%s Kalendārā neiekļautie: *`%s`*" % (
                    emoji, result[0].replace(" ", ", "), emoji2, result[1].replace(" ", ", ")))
            else:
                await self.bot.say("Kļūda! `%s` netika atrasts!" % (msg))

        else:
            result = findByName(self.data, msg)
            if result:
                await self.bot.say("%s %s vārda dienu svin `%s` datumā." % (emoji, msg.title(), result))
            else:
                await self.bot.say("Kļūda! `%s` netika atrasts!" % (msg))



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
