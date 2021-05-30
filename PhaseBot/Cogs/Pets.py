import discord
import glo #type: ignore

from discord import commands

class Pets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    @commands.command()
    async def pet(self, ctx):
        pass # TODO: Pets