import os

#pylint: disable=import-error
import discord

import Cogs
import glo

from discord.ext import commands

class PhaseBot(commands.Bot):
    """ The bot """
    async def on_ready(self):
        print("LOAD") # Great, it's working
        await bot.change_presence(activity = discord.Activity(name = f"le noir | v{glo.VERSION}", type = discord.ActivityType.watching)) # Simplistic help

    async def on_message(self, message):
        if message.author.bot: return # We don't like bots
        return await bot.process_commands(message)


bot = PhaseBot(command_prefix = glo.PREFIX) # Writing the embed
bot.remove_command('help') # Removing default help (I don't like it)
bot.add_cog(Cogs.Admin(bot)) # Cogs
bot.add_cog(Cogs.GDPR(bot))
bot.add_cog(Cogs.General(bot))
bot.add_cog(Cogs.Generators(bot))
bot.add_cog(Cogs.Instagram(bot))
bot.add_cog(Cogs.Listeners(bot))
bot.add_cog(Cogs.Scheduler(bot))
bot.add_cog(Cogs.Starboard(bot))
bot.run(glo.FILEREAD("token"))
