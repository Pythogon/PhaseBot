#pylint: disable=import-error
import discord
import glo

from datetime import date
from datetime import timedelta
from discord.ext import commands

class Generators(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(aliases = ["star"])
    async def startotal(self, ctx):
        read = len(glo.FILEREAD("starcastle.txt")) + 55610
        percent = float('{:g}'.format(float('{:.{p}g}'.format((read / 100000) * 100, p=4)))) # Number to 4 s.f.
        started = date(2020, 9, 30) # Unchanging start date of development and collection of starboard entries
        today = date.today() 
        diff = today - started
        until = (started + timedelta(days = round(100 / (percent / diff.days)))).strftime(glo.DATE_FORMAT_HOUR_EXCLUSIVE) # Calculus
        # print(until) # Debug (kept for quick enable and disabling purposes)
        await ctx.send(f"We are {percent}% of the way towards getting 100000 characters. ETA: {until}.")
