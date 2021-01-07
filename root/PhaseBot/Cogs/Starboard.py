import discord
import glo #pylint: disable=import-error
import operator

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
        except: await ctx.send("ERR. Invalid ID?")

    @commands.command(aliases = ["sc"])
    async def starcount(self, ctx):
        userdata = glo.USERDATA_READ(ctx.author.id)
        try: count = userdata["starcount"]
        except: count = 0; userdata["starcount"] = 0; glo.USERDATA_WRITE(ctx.author.id, userdata)
        embed = discord.Embed(title = "Let me quickly check...", color = glo.COLOR
        ).add_field(name = f"You currently have {count} stars.", value = "Stars before 2021-01-06 weren't counted."
        ).set_footer(text = glo.FOOTER())
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
