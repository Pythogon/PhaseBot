import discord
import glo #pylint: disable=import-error
import traceback

from discord.ext import commands

import Cogs.CurrencyAlpha #pylint: disable=import-error

class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Error messages
        print(f"Exception in {ctx.command}: {error}")
        embed = discord.Embed(title = "An error has occured!", color = glo.ERROR_COLOR).set_footer(text = glo.FOOTER())

        if isinstance(error, commands.MissingRequiredArgument):
            embed.add_field(name = f"You are missing a required argument.", value = "If the error persists, please contact Ash.")

        elif isinstance(error, commands.MissingRole) or isinstance(error, commands.NotOwner) or isinstance(error, commands.MissingPermissions):
            embed.add_field(name = "You don't have permission to run that command.", value = "If you believe you should have permission, please contact Ash.")
        
        else:
            embed.add_field(name = error, value = "If the error persists, please contact Ash.")
        
        return await ctx.send(embed = embed)
        
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(glo.MAIN_CHANNEL_ID) 
        join_message = glo.FILEREAD("join-message.txt") # Loading join message
        try:
            await member.send(join_message)
        except:
            print(f"Member {member.id} has DMs disabled.") # Default case - message couldn't be sent
        embed = discord.Embed(title = f"Please welcome {member.name}!", color = glo.COLOR
        ).add_field(name = "We're glad to have you!", value  = F"I'm PhaseBot, and I'm here to help! Learn more about me with {glo.PREFIX}info and run {glo.PREFIX}help for a list of commands."
        ).set_footer(text = glo.FOOTER())
        await channel.send(embed = embed)     
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # TODO on_member_remove implementation
        pass
       
    @commands.Cog.listener()
    async def on_message(self, message):
        if "214771884544229382" in message.content:
            emoji = self.bot.get_emoji(710243429119950969)
            return await message.add_reaction(emoji) # React bean

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, p: discord.RawReactionActionEvent):
        channel: discord.TextChannel = self.bot.get_channel(p.channel_id)
        message = await channel.fetch_message(p.message_id)

        if len(message.embeds) > 0:
            if str(message.embeds[0].title) == ("Shop") and not p.member.bot:
                if p.emoji.name in Cogs.CurrencyAlpha.current_items:
                    if Cogs.CurrencyAlpha.purchase(p.user_id, p.emoji.name):
                        await channel.send("Thank you for purchasing " + p.emoji.name + "!")
                    else:
                        await channel.send("You don't have enough money to buy that!")
                else:
                    await channel.send("We don't have that for sale right now!")
        else:
            if p.emoji.name == "⭐":
                # Check the legacy system to ensure a previously starred message isn't restarred
                # Preprocessing
                if str(p.message_id) in glo.FILEREAD("starred.txt"): return
                # Bot messages banned from starcastle
                if message.author.bot: return 
                # Check new system to ensure a previously starred message isn't restarred
                if discord.utils.get(message.reactions, me = True, emoji = "✅") is not None: return
                reaction = discord.utils.get(message.reactions, emoji = "⭐")
                print(f"User {p.user_id} reacted to {p.message_id} in {p.channel_id}")
                if reaction.count != glo.STAR_COUNT: return
                print(f"Message {message.id} in {message.channel.id} added to starcastle")
                # Send to star handler
                await glo.STAR(message, self.bot.get_channel(glo.STAR_CHANNEL_ID))
                await message.add_reaction("✅")
