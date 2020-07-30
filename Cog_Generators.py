import discord
import glo

from datetime import date
from datetime import timedelta
from discord.ext import commands
from textgenrnn import textgenrnn

textgen = textgenrnn("local_Store/weights.hdf5") # CommentGenRNN backend loaded

class Generators(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(aliases = ["lg"])
    async def lifegen(ctx):
        gdpr_list = glo.JSONREAD("gdpr.json")
        try:
            if gdpr_list[str(ctx.author.id)] != 1: raise ValueError
        except:
            return await ctx.send(embed = glo.GDPR())
        embed = discord.Embed(title = "I'm thinking...", color = glo.COLOR
        ).add_field(name = "Consulting CommentGenRNN...", value = "Just one moment."
        ).set_footer(text = glo.FOOTER())
        message = await ctx.send(embed = embed)
        textgen.generate_to_file("local_Store/holding.txt", temperature = 1.0) # CommentGenRNN trained off of all LIFE until Kaiser
        new_embed = discord.Embed(title = "I'm done!", color = 0x00ff00
        ).add_field(name = "Results:", value = glo.FILEREAD("holding.txt")
        ).set_footer(text = glo.FOOTER())
        await message.edit(embed = new_embed) # CommentGenRNN integration

    @commands.command(aliases = ["sg"])
    async def stargen(ctx):
        gdpr_list = glo.JSONREAD("gdpr.json")
        try:
            if gdpr_list[str(ctx.author.id)] != 1: raise ValueError
        except:
            return await ctx.send(embed = glo.GDPR())
        read = len(glo.FILEREAD("starcastle.txt"))
        percent = float('{:g}'.format(float('{:.{p}g}'.format((read / 100000) * 100, p=4))))
        started = date(2020, 7, 4)
        today = date.today()
        diff = today - started
        until = (started + timedelta(days = round(100 / (percent / diff.days)))).strftime('%Y-%m-%d')
        print(until)
        await ctx.send(f"This isn't available yet! We are {percent}% of the way towards having enough data to implement this command. ETA: {until}.")
