import discord
import glo

from discord.ext import commands

class Joins(commands.Cog):
    #pylint: disable=unused-variable
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(glo.MAIN_CHANNEL_ID) 
        join_message = glo.JSONREAD("join-message.txt")
        try:
            await member.send(join_message)
        except:
            print(f"Member {member.id} has DMs disabled.")
        embed = discord.Embed(title = f"Please welcome {member.name}!", color = glo.COLOR
        ).add_field(name = "We're glad to have you!", value  = F"I'm PhaseBot, and I'm here to help! Learn more about me with {glo.PREFIX}info and run {glo.PREFIX}help for a list of commands."
        ).set_footer(text = glo.FOOTER())
        await channel.send(embed = embed)     
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(glo.MAIN_CHANNEL_ID) 
        """
        TODO on_member_remove implementation
        """
    
    @commands.command(aliases = ["jm"])
    async def joinmessage(self, ctx):
        """
        TODO jm implemenation
        """
        raise NotImplementedError