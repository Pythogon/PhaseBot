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
        await bot.change_presence(activity = discord.Activity(name = f"my startup...", type = discord.ActivityType.watching)) # Simplistic help
        ud = glo.JSONREAD("userdata.json")
        del ud["default"]
        for k in ud:
            k = int(k)
            u = bot.get_user(k)
            if u is None: 
                name = "Member left"
            else: 
                name = u.name
            glo.SETNAME(k, name)
        await bot.change_presence(activity = discord.Activity(name = f"le noir | v{glo.VERSION}", type = discord.ActivityType.watching)) # Simplistic help

    async def on_message(self, message):
        if message.channel.id == 796374619900084255:
            os.system("git pull")
            os.system("pm2 restart Phase")
        if message.author.bot: return # We don't like bots
        return await bot.process_commands(message)


bot = PhaseBot(command_prefix = glo.PREFIX, intents = discord.Intents.all()) # Writing the embed
bot.remove_command('help') # Removing default help (I don't like it)
bot.add_cog(Cogs.Admin(bot)) # Many cog
bot.add_cog(Cogs.Bank(bot))
bot.add_cog(Cogs.General(bot))
bot.add_cog(Cogs.Listeners(bot))
bot.add_cog(Cogs.Starboard(bot))
bot.add_cog(Cogs.Tasks(bot))
bot.run(glo.FILEREAD("token"))
