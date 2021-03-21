import discord
import glo #pylint: disable=import-error

from datetime import datetime
from discord.ext import commands, tasks

class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @tasks.loop(minutes=60)
    async def money_message_reset(self):
        if datetime.now().hour == 23:
            ud = glo.JSONREAD("userdata.json")
            for k in ud:
                ud[k]["mmnumber"] = 0
            glo.JSONWRITE("userdata.json", ud)
            channel = self.bot.get_channel(glo.MAIN_CHANNEL_ID)
            await channel.send("The daily caps on random message rewards have been reset. You are now allowed to get more random bean encounters.")
                