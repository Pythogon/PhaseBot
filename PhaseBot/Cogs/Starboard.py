import discord
import glo #pylint: disable=import-error
import math
import operator
import time

from datetime import date
from datetime import timedelta
from discord.ext import commands

class Starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(aliases = ["fs"])
    @commands.is_owner()
    async def forcestar(self, ctx, channel: discord.TextChannel, message_id: int):
        try: 
            await glo.STAR(await channel.fetch_message(message_id), self.bot.get_channel(glo.STAR_CHANNEL_ID))
            await ctx.send(f"Message {message_id} starred.")
            glo.FILEAPPEND("starred.txt", str(message_id))
        except: await ctx.send("ERR. Invalid ID?")

    @commands.command(aliases=["top"])
    async def startop(self, ctx):
        filtered = {}
        # Read all userdata
        read = glo.JSONREAD("userdata.json")
        to_send = "```Current starcastle leaderboard\n\n"
        # Remove all 0 entries
        for k, v in read.items():
            if v["starcount"] < 1:
                pass
            else: 
                # Store as {user_id: starcount}
                filtered[k] = v["starcount"]
        # Sort high to low
        filtered = {k: v for k, v in sorted(filtered.items(), key=lambda item: item[1], reverse = True)}
        # Generate full list for ordered values
        for key, value in filtered.items():
            name = glo.CURRENT_NAMES[int(key)]
            to_send += f"{name}: {value}\n"
        to_send += "```"
        # Send end
        await ctx.send(to_send)

    @commands.command(aliases = ["sc"])
    async def starcount(self, ctx):
        userdata = glo.USERDATA_READ(ctx.author.id)
        try: count = userdata["starcount"]
        except: count = 0; userdata["starcount"] = 0; glo.USERDATA_WRITE(ctx.author.id, userdata)
        embed = discord.Embed(title = "Let me quickly check...", color = glo.COLOR) \
        .add_field(name = f"You currently have {count} stars.", value = "Stars before 2021-01-06 weren't counted.") \
        .set_footer(text = glo.FOOTER())
        await ctx.send(embed = embed)

    @commands.command(aliases = ["si"])
    async def starinfo(self, ctx):
        """Starboard info"""
        embed = discord.Embed (title = "What the hell is a starboard?", color = glo.COLOR)
        embed.add_field(name = "The starboard", value = f"""The starboard is a way of saving messages that the community finds funny, clever, etc. It operates like the Quote Vault, but is purely democratic.
        
        You can add to the starboard by reacting to a message with the ⭐ emoji. If the message gets {glo.STAR_COUNT} ⭐s, it will be added to the starcastle channel automatically.

        If one of your messages that you don't like made it to the board, you can just ask Ash to delete it.""")
        embed.set_footer(text = glo.FOOTER())
        await ctx.send(embed = embed) # Starboard help

    @commands.command(aliases = ["st"])
    async def startotal(self, ctx):
        read = len(glo.FILEREAD("starcastle.txt")) + 55610
        percent = float('{:g}'.format(float('{:.{p}g}'.format((read / 100000) * 100, p=4)))) # Number to 4 s.f.
        started = date(2020, 7, 4) # Unchanging start date of development and collection of starboard entries
        today = date.today() 
        diff = today - started
        until = (started + timedelta(days = round(100 / (percent / diff.days)))).strftime(glo.DATE_FORMAT_HOUR_EXCLUSIVE) # Calculus
        # print(until) # Debug (kept for quick enable and disabling purposes)
        await ctx.send(f"We are {percent}% of the way towards getting 100000 characters. ETA: {until}.")

    @commands.command(aliases = ["super"])
    async def superstar(self, ctx, channel: discord.TextChannel, message_id: int):
        message = await channel.fetch_message(message_id)
        userdata = glo.USERDATA_READ(ctx.author.id)
        if discord.utils.get(message.reactions, me = True, emoji = "⭐") is not None: return await ctx.send("I have already reacted to this message.")
        if (time.time() - userdata["laststar"]) < 86400: return await ctx.send("This command is on cooldown. Come back soon!")
        userdata["laststar"] = math.floor(time.time())
        glo.USERDATA_WRITE(ctx.author.id, userdata)
        await message.add_reaction("⭐")
        await ctx.send("Star added successfully.")
