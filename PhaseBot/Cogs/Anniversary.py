import discord
import glo #pylint: disable=import-error

from discord.ext import commands

class Anniversary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # TODO: ANNIVERSARYCODE