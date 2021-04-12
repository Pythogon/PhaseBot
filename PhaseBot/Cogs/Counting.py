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
        message = " ".join(message)
        record = glo.FILEREAD("counting_record.txt")
        user = glo.USERDATA_READ(ctx.author.id)
        if user["currency"] < glo.REVIVE_COST: return await ctx.send("You don't have enough money to do that!")
        user["currency"] -= 1000
        glo.FILEWRITE("counting_lastnumber.txt", record)
        glo.USERDATA_WRITE(ctx.author.id, user)
        embed = discord.Embed(title = f"Revive activated by {ctx.author.name}!", description = f"Current count: {record}.", color = 0x00ff00) \
        .set_thumbnail(url=ctx.author.avatar_url) \
        .set_footer(text=glo.FOOTER())
        if message != "":
            embed.add_field(name = "Revive message", value = message)
        await counting_channel.send(embed = embed)
    
    @commands.Cog.listener(name = "on_message") 
    async def counting_handler(self, message):
        """
        Borrowing code is actually good for your health, trust me
        """
        if message.author.bot: return
        if message.channel.id != glo.COUNTING_CHANNEL: return      

        counting_channel = message.channel
        counting_lastnumber = "counting_lastnumber.txt"
        counting_lastuser = "counting_lastuser.txt"   
        err = 0
        last_user = glo.FILEREAD(counting_lastuser)
        glo.FILEWRITE(counting_lastuser, str(message.author.id)) 
        n = int(glo.FILEREAD(counting_lastnumber))
        nn = n + 1

        await message.delete()
        embed = discord.Embed(title="New count", description=message.content, color = glo.COLOR) \
        .set_author(name=message.author.name, icon_url=message.author.avatar_url) \
        .set_thumbnail(url=message.author.avatar_url) \
        .set_footer(text = glo.FOOTER())
        await counting_channel.send(embed = embed)  
        
        if message.content.startswith(str(nn)) != True: err = 1
        if str(message.author.id) == last_user: err = 2

        if err == 0: 
            ud = glo.USERDATA_READ(message.author.id)
            ud["currency"] += 1
            glo.USERDATA_WRITE(message.author.id, ud)
            return glo.FILEWRITE(counting_lastnumber, str(nn))
        
        await counting_channel.send({1: f"The next number was {nn}. Restarting at 1.", 
        2: f"You can't send two numbers in a row. The next number was {nn}. Restarting at 1."}.get(err))
        glo.FILEWRITE(counting_lastuser, "0")
        glo.FILEWRITE(counting_lastnumber, "0")

        if n > int(glo.FILEREAD("counting_record.txt")):
            await counting_channel.send(f"That was a new record! The record is now: {n}.")
            await counting_channel.edit(topic = f"Last Record: {n}")
            glo.FILEWRITE("counting_record.txt", str(n))

    