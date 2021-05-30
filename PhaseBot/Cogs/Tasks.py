import discord
import glo #type: ignore

from datetime import datetime
from discord.ext import commands, tasks

class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.mmnumber_batch_update.start() #pylint: disable=no-member
    
    @tasks.loop(minutes=60)
    async def mmnumber_batch_update(self):
        if datetime.now().hour == 12:
            ud = glo.JSONREAD("userdata.json")
            for k in ud:
                ud[k]["mmnumber"] = 0
            glo.JSONWRITE("userdata.json", ud)

                