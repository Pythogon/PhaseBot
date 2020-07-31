import os

import discord
import glo

from discord.ext import commands

from Cog_Admin import Admin
from Cog_GDPR import GDPR
from Cog_General import General
from Cog_Generators import Generators
from Cog_Instagram import Instagram
from Cog_Scheduler import Scheduler
from Cog_Starboard import Starboard

class PhaseBot(commands.Bot):
    """ The bot """
    async def on_ready(self):
        print("LOAD") # Great, it's working
        await bot.change_presence(activity = discord.Activity(name = f"Instagram - Loading...", type = discord.ActivityType.watching)) # Simplistic help
        os.system("scrape.bat")
        await bot.change_presence(activity = discord.Activity(name = f"le noir | v{glo.VERSION}", type = discord.ActivityType.watching)) # Simplistic help

    async def on_message(self, message):
        if message.author.bot: return # We don't like bots
        return await bot.process_commands(message)


bot = PhaseBot(command_prefix = glo.PREFIX) # Writing the embed
bot.remove_command('help') # Removing default help (I don't like it)
bot.add_cog(Admin(bot)) # Cogs
bot.add_cog(GDPR(bot))
bot.add_cog(General(bot))
bot.add_cog(Generators(bot))
bot.add_cog(Instagram(bot))
bot.add_cog(Scheduler(bot))
bot.add_cog(Starboard(bot))
bot.run(glo.FILEREAD("token"))
