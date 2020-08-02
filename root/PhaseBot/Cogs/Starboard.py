import discord
import glo #pylint: disable=import-error
import operator

from discord.ext import commands

class Starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        message = reaction.message # Let's get the message reaction
        if message.author.bot: return # NO BOTS
        if reaction.emoji != "⭐": return # NO ANYTHING BUT STAR BB
        print(f"User {user.id} reacted to {message.id} in {message.channel.id}")
        if reaction.count != glo.STAR_COUNT: return # NO NOT THE LIMIT!
        print(f"Message {message.id} in {message.channel.id} added to starcastle")
        await glo.STAR(message, self.bot.get_channel(glo.STAR_CHANNEL_ID))

    @commands.command(aliases = ["fs"])
    @commands.is_owner()
    async def forcestar(self, ctx, channel: discord.TextChannel, message_id: int):
        gdpr_list = glo.JSONREAD("gdpr.json")
        try: 
            if gdpr_list[str(ctx.author.id)] != 1: raise ValueError
        except: return await ctx.send(embed = glo.GDPR())
        try: 
            await glo.STAR(await channel.fetch_message(message_id), self.bot.get_channel(glo.STAR_CHANNEL_ID))
            await ctx.send(f"Message {message_id} starred.")
        except: await ctx.send("ERR. Invalid ID?")

    @commands.command(aliases = ["sc"])
    async def starcount(self, ctx):
        gdpr_list = glo.JSONREAD("gdpr.json")
        try:
            if gdpr_list[str(ctx.author.id)] != 1: raise ValueError
        except:
            return await ctx.send(embed = glo.GDPR())
        star_list = glo.JSONREAD("starcount.json")
        try: count = star_list[str(ctx.author.id)]
        except: count = 0; star_list[str(ctx.author.id)] = 0; glo.JSONWRITE("starcount.json", star_list)
        embed = discord.Embed(title = "Let me quickly check...", color = glo.COLOR
        ).add_field(name = f"You currently have {count} stars.", value = "Stars before 2020-07-11 weren't counted."
        ).set_footer(text = glo.FOOTER())
        await ctx.send(embed = embed)

    @commands.command(aliases = ["si"])
    async def starinfo(self, ctx):
        gdpr_list = glo.JSONREAD("gdpr.json")
        try:
            if gdpr_list[str(ctx.author.id)] != 1: raise ValueError
        except:
            return await ctx.send(embed = glo.GDPR())
        """Starboard info"""
        embed = discord.Embed (title = "What the hell is a starboard?", color = glo.COLOR)
        embed.add_field(name = "The starboard", value = f"""The starboard is a way of saving messages that the community finds funny, clever, etc. It operates like the Quote Vault, but is purely democratic.
        
        You can add to the starboard by reacting to a message with the ⭐ emoji. If the message gets {glo.STAR_COUNT} ⭐s, it will be added to the starcastle channel automatically.

        If one of your messages that you don't like made it to the board, you can just ask Ash to delete it.""")
        embed.set_footer(text = glo.FOOTER())
        await ctx.send(embed = embed) # Starboard help
