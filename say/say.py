import discord
import json
import os
from discord.ext import commands
import asyncio
from .utils import checks

class Say:
    '''Sends messages as bot'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def say(self, ctx, msg: str = None):
        '''Sends messages as bot'''
        if msg is not None:
            await self.bot.say(msg)

def setup(bot):
    bot.add_cog(Say(bot))