import discord
import glo #pylint: disable=import-error

from discord.ext import commands

class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def revive(self, ctx, *message):
        counting_channel = ctx.guild.get_channel(glo.COUNTING_CHANNEL)
        data = glo.JSONREAD("counting.json")
        message = " ".join(message)
        user = glo.USERDATA_READ(ctx.author.id)
        if user["currency"] < glo.REVIVE_COST: return await ctx.send("You don't have enough money to do that!")
        user["currency"] -= 1000
        data["number"] = data["record"]
        glo.JSONWRITE("counting.json", data)
        glo.USERDATA_WRITE(ctx.author.id, user)
        embed = discord.Embed(title = f"Revive activated by {ctx.author.name}!", description = f"Current count: {data['record']}.", color = 0x00ff00) \
        .set_thumbnail(url=ctx.author.avatar_url) \
        .set_footer(text=glo.FOOTER())
        if message != "":
            embed.add_field(name = "Revive message", value = message)
        await counting_channel.send(embed = embed)
        await ctx.send(f"Revived! You have been debited {glo.REVIVE_COST} {glo.BANKFORMAT(glo.REVIVE_COST)}.")
    
    @commands.Cog.listener(name = "on_message") 
    async def counting_handler(self, message):
        """
        Borrowing code is actually good for your health, trust me
        """
        if message.author.bot: return
        if message.channel.id != glo.COUNTING_CHANNEL: return      

        counting_channel = message.channel
        data = glo.JSONREAD("counting.json")
        err = 0 
        n = data["number"]
        nn = n + 1
        record = data["record"]

        await message.delete()
        embed = discord.Embed(title="New count", description=message.content, color = glo.COLOR) \
        .set_author(name=message.author.name, icon_url=message.author.avatar_url) \
        .set_thumbnail(url=message.author.avatar_url) \
        .set_footer(text = glo.FOOTER())
        await counting_channel.send(embed = embed)  
        
        if message.content.startswith(str(nn)) != True: err = 1
        if message.author.id == data["user"]: err = 2

        if err == 0: 
            data["number"] = nn
            data["user"] = message.author.id
            ud = glo.USERDATA_READ(message.author.id)
            ud["currency"] += 1
            glo.USERDATA_WRITE(message.author.id, ud)
            return glo.JSONWRITE("counting.json", data)
        
        reason = {1: "That wasn't the correct next number!", 2: "You can't send 2 numbers in a row!"}.get(err)

        embed = discord.Embed(title = "You failed!", description = f"The next number was {nn}. Restarting at 1.", color = 0xff0000) \
        .add_field(name = "Fail reason", value = reason, inline = False) \
        .set_thumbnail(url = message.author.avatar_url) \
        .set_footer(text = glo.FOOTER())
        
        data["number"] = 0
        data["user"] = 0

        if n > record:
            diff = n - record
            embed.add_field(name = "That was a new record!", value = f"By a difference of {diff}, this beat {record}.", inline = False)
            await counting_channel.edit(topic = f"Last Record: {n}")
            data["record"] = n

        glo.JSONWRITE("counting.json", data)
        await counting_channel.send(embed = embed)
    