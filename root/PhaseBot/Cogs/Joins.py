import discord
import glo #pylint: disable=import-error

from discord.ext import commands

class Joins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    @commands.command(aliases = ["jm"])
    @glo.gdpr_check()
    async def joinmessage(self, ctx): await ctx.send(glo.FILEREAD("join-message.txt")) # 1 liner pythonic solution