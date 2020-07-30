import discord
import glo

from discord.ext import commands

from Cog_Admin import Admin
from Cog_GDPR import GDPR
from Cog_General import General
from Cog_Generators import Generators
from Cog_Instagram import Instagram
from Cog_Starboard import Starboard

def jsonRead(fpath):
    fpath = f"local_Store/{fpath}"
    with open(fpath, 'r', encoding = "utf-8") as json_file: return json.load(json_file) # Anabot JSON read

def jsonWrite(fpath, data):
    fpath = f"local_Store/{fpath}"
    with open(fpath, 'w', encoding = "utf-8") as outfile: json.dump(data,outfile) # Anabot JSON write

def fileRead(fpath):
    fpath = f"local_Store/{fpath}"
    with open(fpath, "r", encoding = "utf-8") as file: return file.read() # TXT read

def fileAppend(fpath, data):
    fpath = f"local_Store/{fpath}"
    with open(fpath, "a", encoding = "utf-8") as file: file.write("\n" + data)

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
bot.add_cog(Starboard(bot))
bot.run(fileRead("token"))
