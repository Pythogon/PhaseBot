import discord
import glo #pylint: disable=import-error
import traceback

from discord.ext import commands

class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if "214771884544229382" in message.content:
            emoji = self.bot.get_emoji(710243429119950969)
            return await message.add_reaction(emoji) # React bean

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
        