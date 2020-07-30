import os

import discord
import glo

from discord import commands

class Instagram(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @bot.command(aliases = ["c"])
    async def comments(ctx, user):
        gdpr_list = glo.JSONREAD("gdpr.json")
        try:
            if gdpr_list[str(ctx.author.id)] != 1: raise ValueError
        except:
            return await ctx.send(embed = glo.GDPR())
        comments = ""
        data = glo.JSONREAD("sole_nyu/sole_nyu.json")["GraphImages"][0]["comments"]["data"]
        for comment in data:
            if user == comment["owner"]["username"]: comments += comment["text"] + "\n"
        if comments == "":
            embed = discord.Embed(title = "No comments found!", color = 0xff0000
            ).add_field(name = "Maybe they got dissolved by adimensia...", value = "Ensure you're typing the username correctly."
            ).set_footer(text = glo.FOOTER())
            return await ctx.send(embed = embed)
        embed = discord.Embed(title = "Comments found!", color = glo.COLOR
        ).add_field(name = f"{user}'s comments:", value = comments
        ).set_footer(text = glo.FOOTER())
        await ctx.send(embed = embed)

    @bot.command(aliases = ["r"])
    async def reload(ctx):
        gdpr_list = glo.JSONREAD("gdpr.json")
        try:
            if gdpr_list[str(ctx.author.id)] != 1: raise ValueError
        except:
            return await ctx.send(embed = glo.GDPR())
        embed = discord.Embed(title = "Polling Instagram...", color = glo.COLOR
        ).add_field(name = "It won't be a minute.", value = "Apologies for the wait!"
        ).set_footer(text = glo.FOOTER())
        message = await ctx.send(embed = embed)
        await bot.change_presence(activity = discord.Activity(name = f"Instagram - Loading...", type = discord.ActivityType.watching)) # Simplistic help
        os.system("scrape.bat")
        await bot.change_presence(activity = discord.Activity(name = f"le noir | v{glo.VERSION}", type = discord.ActivityType.watching)) # Simplistic help
        new_embed = discord.Embed(title = "Poll complete!", color = 0x00ff00
        ).add_field(name = f"{glo.PREFIX}votes has now been filled with new information!", value = "You can see how this worked over at [InstaScrape](https://github.com/Pythogon/InstaScrape/)."
        ).set_footer(text = glo.FOOTER())
        await message.edit(embed = new_embed)

    @bot.command(aliases = ["v"])
    async def votes(self, ctx, to_check: int):
        gdpr_list = glo.JSONREAD("gdpr.json")
        try:
            if gdpr_list[str(ctx.author.id)] != 1: raise ValueError
        except:
            return await ctx.send(embed = glo.GDPR())
        letters = []
        no = []
        percentage = []
        read = glo.JSONREAD("sole_nyu/sole_nyu.json")["GraphImages"][0]["comments"]["data"]
        to_send = ""
        total_percentage = 0.0
        total_yes = 0.0
        voted = []
        yes = []

        for x in range(to_check):
            letters.append(chr(65 + x))
            percentage.append("")
            no.append(0)
            yes.append(0)

            for comment in read:
                author = comment["owner"]["username"]
                if author in voted: continue
                if letters[x] == comment["text"][0].upper(): yes[x] += 1; voted.append(author)
                else: no[x] += 1

            percentage[x] = str((yes[x] / (yes[x] + no[x])) * 100)[:5]
            total_percentage += float(percentage[x])
            total_yes += yes[x]

        for x in range(to_check): to_send += f"{letters[x]}: {str((yes[x] / total_yes) * 100)[:5]}% ({yes[x]} counted).\n"
        embed = discord.Embed(title = "Lemme do the maths...", color = glo.COLOR
        ).add_field(name = f"Running voting results for today:", value = to_send
        ).set_footer(text = glo.FOOTER())
        await ctx.send(embed = embed)

    @bot.command(aliases = ["vr"])
    async def votesraw(ctx, to_check, loose_checking=False):
        gdpr_list = glo.JSONREAD("gdpr.json")
        try:
            if gdpr_list[str(ctx.author.id)] != 1: raise ValueError
        except:
            return await ctx.send(embed = glo.GDPR())
        letters = list(to_check)
        no = []
        percentage = []
        read = glo.JSONREAD("sole_nyu/sole_nyu.json")["GraphImages"][0]["comments"]["data"]
        to_check = len(letters)
        to_send = ""
        total_percentage = 0.0
        total_yes = 0.0
        voted = []
        yes = []
        for x in range(to_check):
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
