import discord
import json
import os
from discord.ext import commands
import asyncio
from .utils import checks
import requests
import re

ext = ['jpg', 'png', 'gif', 'gifv', 'mp4', 'svg', 'bmp']

class NoMore:
    '''Prevents blacklisted users from posting images'''

    def __init__(self, bot):
        self.blacklist = json.loads(open("data/nomore/blacklist.json").read())
        self.bot = bot

    @commands.group(pass_context=True)
    async def nomore(self, ctx):
        """Blacklists users from posting images"""

        if ctx.invoked_subcommand is None:
            await self.bot.say("Type `%shelp nomore` for more info" % (ctx.prefix))

    @checks.admin_or_permissions(administrator=True)
    @nomore.command(name="add", pass_context=True)
    async def add(self, ctx, usr: int = None):
        '''Add user to blacklist'''
        try:
            username = await self.bot.get_user_info(usr)
            self.blacklist["blacklist"].append(int(usr))
            json.dump(self.blacklist, (open("data/nomore/blacklist.json", 'w')))
            await self.bot.say('`%s` added to blacklist' % (username))
        except Exception as e:
            await self.bot.say(e)

    @checks.admin_or_permissions(administrator=True)
    @nomore.command(name="remove", pass_context=True)
    async def remove(self, ctx, usr: int = None):
        '''Remove user from blacklist'''
        try:
            if int(usr) in self.blacklist["blacklist"]:
                username = await self.bot.get_user_info(usr)
                self.blacklist["blacklist"].remove(usr)
                json.dump(self.blacklist, (open("data/nomore/blacklist.json", 'w')))
                await self.bot.say('`%s` removed from blacklist' % (username))
        except Exception as e:
            await self.bot.say(e)

    @checks.mod_or_permissions(manage_messages=True)
    @nomore.command(name="list", pass_context=True)
    async def list(self):
        '''List blacklisted users'''
        message = []
        for user in self.blacklist["blacklist"]:
            username = await self.bot.get_user_info(user)
            message.append("%s\n" % (username))
        if message:
            await self.bot.say("Blacklisted users:\n```%s```" % (''.join(message)))
        else:
            await self.bot.say("`Blacklist is empty!`")

    async def on_message(self, msg):
        check_url = False
        if msg.author.id != self.bot.user.id:
            for blid in self.blacklist["blacklist"]:
                if blid == int(msg.author.id):
                    check_url = True
                    break
            if check_url:
                try:
                    url = msg.attachments[0]["url"]
                except:
                    url = ""
                if url != "":
                    for extension in ext:
                        if extension in url: # Delete image attachments
                            await self.bot.delete_message(msg)
                            await self.bot.send_message(msg.channel, "¯\_(ツ)_/¯")
                else:
                    re_urls = re.findall(r'(https?://\S+)', msg.content) # look for urls in message
                    if re_urls:
                        for link in re_urls:
                            if "gifv" in link: # Since gifv's content-type is 'html/text', it gets special treatment
                                await self.bot.delete_message(msg)
                                await self.bot.send_message(msg.channel, "¯\_(ツ)_/¯")
                                break
                            try: # if invalid url then skip this iteration (no point in checking if the url is invalid)
                                response = requests.head(link)
                            except:
                                continue
                            url_type = response.headers.get('content-type')
                            if "image" in url_type or "video" in url_type:
                                await self.bot.delete_message(msg)
                                await self.bot.send_message(msg.channel, "¯\_(ツ)_/¯")
                                break

def check_folder():
    if not os.path.exists('data/nomore'):
        print('Creating nomore folder...')
        os.makedirs('data/nomore')

def check_blacklist_file():
    contents = {'blacklist': []}
    if not os.path.exists("data/nomore/blacklist.json"):
        print('Creating empty blacklist.json...')
        json.dump(contents, (open("data/nomore/blacklist.json", 'w')))

def setup(bot):
    check_folder()
    check_blacklist_file()
    bot.add_cog(NoMore(bot))
