import discord
import glo

from datetime import date
from datetime import datetime
from datetime import timedelta
from discord.ext import commands

class Scheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.group(aliases = ["ss"])
    @commands.has_role(glo.DEVELOPER_ROLE_ID)
    async def schedule(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"Correct usage is `{glo.PREFIX}schedule [add|purge|remove]`.")

    @schedule.command(aliases = ["a"])
    async def add(self, ctx, day, user): 
        scheduled = glo.JSONREAD("schedule.json")
        try: datetime.strptime(day, "%Y-%m-%d")
        except: return await ctx.send("The date isn't valid. Please try again (CORRECT FORMAT IS YYYY-MM-DD).")
        scheduled[day] = user
        glo.JSONWRITE("schedule.json", scheduled)
        await ctx.send(f"Added {user} to schedule on {day}.")

    @schedule.command(aliases = ["p"])
    async def purge(self, ctx):
        scheduled = glo.JSONREAD("schedule.json")
        today = date.today()
        to_write = {k: v for k,v in scheduled.items() if (datetime.strptime(k, glo.DATE_FORMAT_HOUR_EXCLUSIVE).date() - today).days >= 0}
        glo.JSONWRITE("schedule.json", to_write)
        await ctx.send("Purged old entries in the database.")

    @schedule.command(aliases = ["r"])
    async def remove(self, ctx, day):
        scheduled = glo.JSONREAD("schedule.json")
        scheduled.pop(day)
        glo.JSONWRITE("schedule.json", scheduled)
        await ctx.send("Attempted to remove that day. Please double check to see if it's been removed.")

    @commands.command(aliases = ["wd"])
    async def wonderland(self, ctx):
        scheduled = glo.JSONREAD("schedule.json")
        today = date.today()
        to_send = ""
        transformed = {}
        for key, value in scheduled.items():
            diff = (datetime.strptime(key, glo.DATE_FORMAT_HOUR_EXCLUSIVE).date() - today).days
            if diff < 0: continue
            transformed[diff] = [key, value]
        transformed = dict(sorted(transformed.items()))
        for key, value in transformed.items():
            conjugated = {0: "today", 1: "tomorrow"}.get(key, f"in {key} days")
            to_send += f"{value[0]} - {value[1]} ({conjugated})\n".replace("_", "\_") #pylint: disable=anomalous-backslash-in-string
        embed = discord.Embed(title = "PROJECT WONDERLAND", color = glo.COLOR
        ).add_field(name = "Schedule:", value = to_send
        ).set_footer(text = f"PhaseBot v{glo.VERSION} | Made by Pythogon Technologies | Let it wonder...")
        await ctx.send(embed = embed)
        



        
