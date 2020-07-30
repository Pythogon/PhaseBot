import discord
import glo

from discord.ext import commands

class GDPR(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @bot.command()
    async def accept(self, ctx):
        gdpr_list = glo.JSONREAD("gdpr.json")
        gdpr_list[str(ctx.author.id)] = 1
        glo.JSONWRITE("gdpr.json", gdpr_list)
        await ctx.send("Thank you for agreeing to our DCA. You can revoke your permission at any time by contacting Ashie#9999.")

    @bot.command()
    async def gdpr(self, ctx):
        await ctx.send(embed = discord.Embed(title = "GDPR", color = 0x00ff00
        ).add_field(name = "How we use your data.", value = """PhaseBot uses your data in several situations. Below is a full list.
Anonymised tracking and raw counts of starboard statistics.
Saving of internal data such as scores.
Temporary storage of user avatars.
Named and anonymised public information from Instagram from the last 24 hours.

If you wish to use the bot, type )accept."""
        ).set_footer(text = glo.FOOTER()))
