import discord
import glo #pylint: disable=import-error

from discord.ext import commands

class GDPR(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def accept(self, ctx):
        userdata = glo.USERDATA_READ(ctx.author.id)
        userdata["gdpr"] = 1
        glo.USERDATA_WRITE(ctx.author.id, userdata)
        await ctx.send("Thank you for agreeing to our DCA. You can revoke your permission at any time by contacting アシ#0001.")

    @commands.command()
    async def gdpr(self, ctx):
        await ctx.send(embed = discord.Embed(title = "GDPR", color = 0x00ff00
        ).add_field(name = "How we use your data.", value = f"""PhaseBot uses your data in several situations. Below is a full list.
Anonymised tracking and raw counts of starboard statistics.
Saving of internal data such as scores.
Temporary storage of user avatars.
Named and anonymised public information from Instagram from the last 24 hours.

If you wish to use the bot, type )accept."""
        ).set_footer(text = glo.FOOTER()))
