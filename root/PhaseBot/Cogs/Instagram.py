import os

import discord
import glo #pylint: disable=import-error

from discord.ext import commands

class Instagram(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(aliases = ["c"])
    @glo.gdpr_check()
    async def comments(self, ctx, user):
        comments = ""
        data = glo.JSONREAD("sole_nyu/sole_nyu.json")["GraphImages"][0]["comments"]["data"] # Storing only essential info in bot
        for comment in data:
            if user == comment["owner"]["username"]: comments += comment["text"] + "\n" # Check for username match
        if comments == "":
            embed = discord.Embed(title = "No comments found!", color = 0xff0000
            ).add_field(name = "Maybe they got dissolved by adimensia...", value = "Ensure you're typing the username correctly."
            ).set_footer(text = glo.FOOTER())
            return await ctx.send(embed = embed) # Default case - No comment found
        embed = discord.Embed(title = "Comments found!", color = glo.COLOR
        ).add_field(name = f"{user}'s comments:", value = comments
        ).set_footer(text = glo.FOOTER())
        await ctx.send(embed = embed)

    @commands.command(aliases = ["r"])
    @glo.gdpr_check()
    async def reload(self, ctx):
        embed = discord.Embed(title = "Polling Instagram...", color = glo.COLOR
        ).add_field(name = "It won't be a minute.", value = "Apologies for the wait!"
        ).set_footer(text = glo.FOOTER())
        message = await ctx.send(embed = embed)
        await self.bot.change_presence(activity = discord.Activity(name = f"Instagram - Loading...", type = discord.ActivityType.watching)) # Simplistic help
        async with ctx.typing(): os.system("scrape.bat") # with typing to show the bot is processing
        await self.bot.change_presence(activity = discord.Activity(name = f"le noir | v{glo.VERSION}", type = discord.ActivityType.watching)) # Simplistic help
        new_embed = discord.Embed(title = "Poll complete!", color = 0x00ff00 # Green embed - success
        ).add_field(name = f"{glo.PREFIX}votes has now been filled with new information!", value = "You can see how this worked over at [InstaScrape](https://github.com/Pythogon/InstaScrape/)."
        ).set_footer(text = glo.FOOTER())
        await message.edit(embed = new_embed)

    @commands.command(aliases = ["v"])
    @glo.gdpr_check()
    async def votes(self, ctx, to_check: int):
        letters = []
        no = []
        percentage = []
        read = glo.JSONREAD("sole_nyu/sole_nyu.json")["GraphImages"][0]["comments"]["data"] # Essential information
        to_send = ""
        total_percentage = 0.0
        total_yes = 0.0
        voted = []
        yes = []

        for x in range(to_check):
            letters.append(chr(65 + x)) # Automatic letter system
            percentage.append("")
            no.append(0)
            yes.append(0)

            for comment in read:
                author = comment["owner"]["username"]
                if author in voted: continue
                if letters[x] == comment["text"][0].upper(): yes[x] += 1; voted.append(author)
                else: no[x] += 1

            percentage[x] = str((yes[x] / (yes[x] + no[x])) * 100)[:5] # Maths
            total_percentage += float(percentage[x])
            total_yes += yes[x]

        for x in range(to_check): to_send += f"{letters[x]}: {str((yes[x] / total_yes) * 100)[:5]}% ({yes[x]} counted).\n" 
        embed = discord.Embed(title = "Lemme do the maths...", color = glo.COLOR
        ).add_field(name = f"Running voting results for today:", value = to_send
        ).set_footer(text = glo.FOOTER())
        await ctx.send(embed = embed)

    @commands.command(aliases = ["vr"])
    @glo.gdpr_check()
    async def votesraw(self, ctx, to_check, loose_checking=False):
        letters = list(to_check)
        no = []
        percentage = []
        read = glo.JSONREAD("sole_nyu/sole_nyu.json")["GraphImages"][0]["comments"]["data"]
        to_check = len(letters) # Getting a number for the for loops
        to_send = ""
        total_percentage = 0.0
        total_yes = 0.0
        voted = []
        yes = []
        for x in range(to_check): # See votes()
            percentage.append("")
            no.append(0)
            yes.append(0)
            voted.append([])
            for comment in read:
                author = comment["owner"]["username"]
                is_yes = False
                if author in voted: continue
                if loose_checking == False:
                    if letters[x] == comment["text"][0].upper(): yes[x] += 1; voted[x].append(author); is_yes = True
                else:
                    if letters[x] in comment["text"].upper(): yes[x] += 1; voted[x].append(author); is_yes = True
                if is_yes == False: no[x] += 1
            percentage[x] = str((yes[x] / (yes[x] + no[x])) * 100)[:5]
            total_percentage += float(percentage[x])
            total_yes += yes[x]

        for x in range(to_check): to_send += f"{letters[x]}: {str((yes[x] / total_yes) * 100)[:5]}% ({yes[x]} counted).\n"
        embed = discord.Embed(title = "Lemme do the maths...", color = glo.COLOR
        ).add_field(name = f"Running voting results for today:", value = to_send
        ).set_footer(text = glo.FOOTER())
        await ctx.send(embed = embed)