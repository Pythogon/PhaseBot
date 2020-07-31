import asyncio
import discord
import glo
import names
import random

from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_message(self, message):
        if "214771884544229382" in message.content:
            emoji = self.bot.get_emoji(710243429119950969)
            return await message.add_reaction(emoji) # BEAN

    @commands.command(aliases = ["a"])
    async def avatar(self, ctx, user: discord.User):
        gdpr_list = glo.JSONREAD("gdpr.json")
        try:
            if gdpr_list[str(ctx.author.id)] != 1: raise ValueError
        except:
            return await ctx.send(embed = glo.GDPR())
        await ctx.send(user.avatar_url) # Anabot avatar command

    @commands.command(name = 'help', aliases = ["?"]) # New help command (help is a registered keyword so we just need to pretend we have a function called 'help')
    async def help_command(self, ctx):
        gdpr_list = glo.JSONREAD("gdpr.json")
        try:
            if gdpr_list[str(ctx.author.id)] is not 1: raise ValueError
        except:
            return await ctx.send(embed = glo.GDPR())
        """ Basic bitch help command (by Ash) """
        title = discord.Embed(title = 'Help', color = glo.COLOR
        ).add_field(name = 'Welcome to PhaseBot!', value = f"""Welcome to the PhaseBot {glo.VERSION} help menu.
        All commands use the {glo.PREFIX} prefix.
        Below are commands listed by category.""", inline = False
        ).add_field(name = "General", value = """avatar|a <user>
        help|?
        info|i
        name|n <m|f|n>
        poll|p "Question" answer1|answer2|answer3|answer4
        rate|sr <user>""", inline = False
        ).add_field(name = "Instagram", value = """comments|c <IG user>
        reload|r
        votes|v <number of choices>
        votesraw|vr <letters to search for> [loose checking = False]""", inline = False
        ).add_field(name = "Starboard", value = """starcount|sc
        starinfo|si""", inline = False
        ).add_field(name = "Generators", value = """lifegen|lg
        stargen|sg""", inline = False
        ).add_field(name = "GDPR", value = "accept\ngdpr"
        ).set_footer(text = glo.FOOTER())
        await ctx.send(embed = title) # Anabot help

    @commands.command(aliases = ["i"])
    async def info(self, ctx):
        gdpr_list = glo.JSONREAD("gdpr.json")
        try:
            if gdpr_list[str(ctx.author.id)] != 1: raise ValueError
        except:
            return await ctx.send(embed = glo.GDPR())
        embed = discord.Embed(title = "About PhaseBot", color = glo.COLOR
        ).add_field(name = "Developer", value = "PhaseBot was created for LIFE: The Game by [Ash](https://kaidev.uk) on behalf of [Pythogon Technologies](https://github.com/Pythogon).", inline = False
        ).add_field(name = "More Info", value = f"PhaseBot is currently on Version {glo.VERSION}. The project started on 2020-07-04.", inline = False
        ).add_field(name = "Special Thanks", value = "Special thanks to all who worked on [Anabot](https://github.com/Pythogon/Anabot) and [CommentGenRNN](https://github.com/Pythogon/CommentGenRNN) for providing considerable contributions to PhaseBot.", inline = False
        ).add_field(name = "GitHub.", value = "You can find PhaseBot's GitHub [here](https://github.com/Pythogon/PhaseBot) and take a look at its source code! If you posess developing talents, feel free to send a PR our way, we'd be happy to take on any suggestions.", inline = False
        ).set_footer(text = glo.FOOTER())
        await ctx.send(embed = embed) # Credits :)

    @commands.command(aliases = ["n"])
    async def name(self, ctx, gender):
        gdpr_list = glo.JSONREAD("gdpr.json")
        try:
            if gdpr_list[str(ctx.author.id)] != 1: raise ValueError
        except:
            return await ctx.send(embed = glo.GDPR())
        if gender == "m" or gender == "f":
            name = names.get_full_name(gender = {"m": "male", "f": "female"}.get(gender))
        else:
            name = names.get_full_name()
        label = {"m": "male", "f": "female"}.get(gender, "random")
        embed = discord.Embed(title = f"Generating a {label} name...", color = glo.COLOR
        ).add_field(name = f"The name I came up with is {name}.", value = "Feel free to run the command again!"
        ).set_footer(text = glo.FOOTER())
        await ctx.send(embed = embed)

    @commands.command(aliases = ["p"])
    async def poll(self, ctx, question, *answers):
        gdpr_list = glo.JSONREAD("gdpr.json")
        try:
            if gdpr_list[str(ctx.author.id)] != 1: raise ValueError
        except:
            return await ctx.send(embed = glo.GDPR())
        answers = " ".join(answers) # Anabot interpreter
        answers = list(answers.split("|")) # Listify!
        if len(answers) > 4: return await ctx.send("You can have a maximum of 4 answers.") # ERR
        to_send = f"__New poll: **{question}**__"
        for x in range(len(answers)): to_send += "\n" + glo.GETEMOJI(x) + ": " + answers[x]
        message = await ctx.send(to_send)
        for x in range(len(answers)): await message.add_reaction(glo.GETEMOJI(x)) # GETEMOJI[x]

    @commands.command(aliases = ["sr"])
    async def rate(self, ctx, user: discord.User):
        gdpr_list = glo.JSONREAD("gdpr.json")
        try:
            if gdpr_list[str(ctx.author.id)] != 1: raise ValueError
        except:
            return await ctx.send(embed = glo.GDPR())
        fpath = 'rate.json'
        try: scores = glo.JSONREAD(fpath)
        except: await ctx.send('ERR')
        try:
            score = int(scores[str(user.id)])
            embed = discord.Embed(title=f"Someone's already asked about {user.name}. One moment...", color = 0xbdbdbd
            ).add_field(name = 'Fetching...', value = "Please wait, this won't take long.")
        except:
            embed = discord.Embed(title=f"Nobody's asked me about {user.name} yet. Let's have a look.", color = 0xbdbdbd
            ).add_field(name = 'Calculating...', value = "Please wait, this won't take long.")
            score = random.randint(1,5)
            scores[str(user.id)] = str(score)
            glo.JSONWRITE(fpath, scores)
        embed.set_footer(text = glo.FOOTER())
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(2)
        await msg.edit(embed = glo.GETRATE(score, user)) # Stolen from Anabot
