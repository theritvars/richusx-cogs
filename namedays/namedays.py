import discord
import json
import datetime
import os
import re
from redbot.core import commands
import urllib.request

emoji = ":champagne:"  # Iekļautie
emoji2 = ":beers:"  # Neiekļautie

BaseCog = getattr(commands, "Cog", object)

def findByDate(vd, day, month):
        for i in vd["namedays"]:
            if i["month"] == month:
                if i["day"] == day:
                    return [i["names"], i["noncalendarnames"]]
        return False

def findByName(vd, name):
    name = r"\b%s\b" % (name.lower())

    for i in vd["namedays"]:
        if re.search(name, i["names"].lower()) or re.search(name, i["noncalendarnames"].lower()):
            date = "%s/%s" % (i["day"], i["month"])
            return date
    return False

class Namedays(BaseCog):
    """Reply with today's name-days"""

    def __init__(self):
        self.data = json.loads(open("data/namedays/namedays.json", encoding='utf-8').read())

    @commands.command()
    async def vd(self, ctx, msg: str = None):
        """
        vd - Atgriež šodienas vārda dienu jubilārus
        vd [vārds] - Atgriež datumu kurā [vārds] svin vārda dienu
        vd [datums] - Atgriež [datums] vārda dienas jubilārus (formāts: dd.mm; dd/mm; dd,mm)
        """

        if msg is not None:
            date_regex = re.match(r"^(0[1-9]|1[0-9]|2[0-9]|3[0-1])(\.|\/|\,)(0[1-9]|1[0-2])$", msg)

        if msg is None:
            day = datetime.datetime.now().strftime("%d")
            month = datetime.datetime.now().strftime("%m")
            result = findByDate(self.data, day, month)

            included = result[0].replace(" ", ", ")
            excluded = result[1].replace(" ", ", ")

            if result:
                await ctx.send(f"{emoji} Šodien vārda dienu svin: `{included}`\n\n{emoji2} Kalendārā neiekļautie: *`{excluded}`*")
            else:
                await ctx.send(f"Kļūda! `{msg}` netika atrasts!")

        elif date_regex:
            day = date_regex.group(1)
            month = date_regex.group(3)
            result = findByDate(self.data, day, month)

            included = result[0].replace(" ", ", ")
            excluded = result[1].replace(" ", ", ")

            if result:
                await ctx.send(f"{emoji} Šodien vārda dienu svin: `{included}`\n\n{emoji2} Kalendārā neiekļautie: *`{excluded}`*")
            else:
                await ctx.send(f"Kļūda! `{msg}` netika atrasts!")

        else:
            result = findByName(self.data, msg)
            if result:
                await ctx.send(f"{emoji} {msg.title()} vārda dienu svin `{result}` datumā.")
            else:
                await ctx.send(f"Kļūda! `{msg}` netika atrasts!")



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
