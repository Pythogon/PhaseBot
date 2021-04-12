import discord
import glo #pylint: disable=import-error

from discord.ext import commands

class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

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
        .set_thumbnail(url=message.author.avatar_url)
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
            await counting_channel.edit(topic = f"Last record: {n}")
            glo.FILEWRITE("counting_record.txt", str(n))

    