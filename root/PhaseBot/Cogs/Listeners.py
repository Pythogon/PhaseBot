import discord
import glo #pylint: disable=import-error
import traceback

from discord.ext import commands

class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(error)
        embed = discord.Embed(title = "An error has occured!", color = glo.ERROR_COLOR).set_footer(text = glo.FOOTER())

        if isinstance(error, commands.CheckFailure):
            embed.add_field(name = "You need to read our data collection agreement.", value = f"""In compliance with the EU's General Data Protection Regulation (GDPR), we're requiring all users to agree to their data being stored.
            PhaseBot uses and stores only the data that is essential to its operaton.
            You can learn more about the data we store by running {glo.PREFIX}gdpr, or accept it by typing {glo.PREFIX}accept.""")

        elif isinstance(error, commands.MissingRequiredArgument):
            embed.add_field(name = f"You are missing a required argument.", value = "If the error persists, please contact Ash.")

        elif isinstance(error, commands.MissingRole) or isinstance(error, commands.NotOwner) or isinstance(error, commands.MissingPermissions):
            embed.add_field(name = "You don't have permission to run that command.", value = "If you believe you should have permission, please contact Ash.")
        
        else:
            embed.add_field(name = "...but I don't know what caused it.", value = "If the error persists, please contact Ash.")
        
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