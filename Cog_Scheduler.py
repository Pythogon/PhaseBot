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

    @commands.command(aliases = ["ssa"])
    @commands.has_role(glo.DEVELOPER_ROLE_ID)
    async def schedule_add(self, ctx, day, user):
        schedule = glo.JSONREAD("schedule.json")
        try: datetime.strptime(day, "%Y-%m-%d")
        except: return await ctx.send("The date isn't valid. Please try again (CORRECT FORMAT IS YYYY-MM-DD).")
        schedule[day] = user
        glo.JSONWRITE("schedule.json", schedule)
        await ctx.send(f"Added {user} to schedule on {day}.")
    
    @commands.command(aliases = ["ssr"])
    @commands.has_role(glo.DEVELOPER_ROLE_ID)
    async def schedule_remove(self, ctx, day):
        schedule = glo.JSONREAD("schedule.json")
        schedule.pop(day)
        glo.JSONWRITE("schedule.json", schedule)
        await ctx.send("Attempted to remove that day. Please double check to see if it's been removed.")

    @commands.command(aliases = ["wd"])
    async def wonderland(self, ctx):
        schedule = glo.JSONREAD("schedule.json")
        today = date.today()
        to_send = ""
        transformed = {}
        for key, value in schedule.items():
            diff = (datetime.strptime(key, "%Y-%m-%d").date() - today).days
            if diff < 0: schedule.pop(key)
            transformed[diff] = [key, value]
        transformed = dict(sorted(transformed.items()))
        for key, value in transformed.items():
            conjugated = {0: "today", 1: "tomorrow"}.get(key, f"in {key} days")
            to_send += f"{value[0]} - {value[1]} ({conjugated})\n".replace("_", "\_")
        embed = discord.Embed(title = "PROJECT WONDERLAND", color = glo.COLOR
        ).add_field(name = "Schedule:", value = to_send
        ).set_footer(text = f"PhaseBot v{glo.VERSION} | Made by Pythogon Technologies | Let it wonder...")
        await ctx.send(embed = embed)
        glo.JSONWRITE("schedule.json", schedule)
        






        
