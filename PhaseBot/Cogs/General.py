import asyncio
import discord
import glo #type: ignore
import random

from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(aliases = ["a"])
    async def avatar(self, ctx, user: discord.User):
        await ctx.send(user.avatar_url) # Anabot avatar command

    @commands.command(aliases = ["clr","color"])
    async def colour(self, ctx, h):
        # Make an RGB tuple to appease the Disgods
         rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
         # Variable definition
         color = discord.Color.from_rgb(rgb[0], rgb[1], rgb[2])
         userdata = glo.USERDATA_READ(ctx.author.id)
         if userdata["role"] == None:
             # Generate new role
             role = await ctx.guild.create_role(name = str(ctx.author.id))
             await ctx.author.add_roles(role)
             # Move role relative to PhaseBot's top role 
             await role.edit(position = ctx.me.top_role.position - 2, color = color)
             userdata["role"] = role.id
             glo.USERDATA_WRITE(ctx.author.id, userdata)
             return await ctx.send("New user detected. Modification complete.")
        # Modify precreated role's colour
         role = ctx.guild.get_role(userdata["role"])
         await role.edit(color = color)
         await ctx.send("Modification complete.")

    @commands.command(name = 'help', aliases = ["?"]) 
    async def help_command(self, ctx):
        title = discord.Embed(title = 'Help', color = glo.COLOR) \
        .add_field(name = 'Welcome to PhaseBot!', value = f"""Welcome to the PhaseBot {glo.VERSION} help menu.
All commands use the {glo.PREFIX} prefix.
Below are commands listed by category.""", inline = False) \
        .add_field(name = "Economy", value = """balance|bal
balancetop|baltop|bt
daily
pay <payee> <amount>
shop
steal""", inline=False) \
        .add_field(name = "General", value = """avatar|a <user>
colour|color|clr <hex code>
help|?
info|i
poll|p "Question" answer1|answer2|answer3|answer4
rate|sr <user>""", inline = False) \
        .add_field(name = "Starboard", value = """starcount|sc
starinfo|si
startop|top
startotal|st
superstar|super #channel <message id>""", inline = False) \
        .set_footer(text = glo.FOOTER())
        await ctx.send(embed = title) # Anabot help

    @commands.command(aliases = ["i"])
    async def info(self, ctx):
        embed = discord.Embed(title = f"About PhaseBot", color = glo.COLOR) \
        .add_field(name = "Developer", value = "PhaseBot was created for LIFE: The Game by Ash on behalf of [Pythogon Technologies](https://github.com/Pythogon).", inline = False) \
        .add_field(name = "More Info", value = f"PhaseBot is currently on Version {glo.VERSION}. The project started on 2020-07-04.", inline = False) \
        .add_field(name = "Special Thanks", value = """Many thanks to @bekano_cat for the permission to use her wonderful drawing of Phaser as the bot's avatar.""", inline = False) \
        .add_field(name = "GitHub.", value = "You can find PhaseBot's GitHub [here](https://github.com/Pythogon/PhaseBot) and take a look at its source code! If you're a dev, feel free to send a PR our way! We'd be happy to take on any suggestions.", inline = False) \
        .set_footer(text = glo.FOOTER())
        await ctx.send(embed = embed) # Credits

    @commands.command(aliases = ["jm"])
    async def joinmessage(self, ctx): await ctx.send(glo.FILEREAD("join-message.txt")) 

    @commands.command(aliases = ["p"])
    async def poll(self, ctx, question, *answers):
        # Preprocessing
        answers = " ".join(answers) 
        answers = list(answers.split("|")) 
        # Prevent errors
        if len(answers) > 4: return await ctx.send("You can have a maximum of 4 answers.") 
        to_send = f"__New poll: **{question}**__"
        # Prepare to_send message
        for x in range(len(answers)): to_send += "\n" + glo.GETEMOJI(x) + ": " + answers[x]
        message = await ctx.send(to_send)
        for x in range(len(answers)): await message.add_reaction(glo.GETEMOJI(x)) 

    @commands.command(aliases = ["sr"])
    async def rate(self, ctx, user: discord.User):
        userdata = glo.USERDATA_READ(user.id)
        try:
            score = userdata["rate"]
            if score == None: raise ValueError
            embed = discord.Embed(title=f"Someone's already asked about {user.name}. One moment...", color = 0xbdbdbd) \
            .add_field(name = 'Fetching...', value = "Please wait, this won't take long.")
        except:
            embed = discord.Embed(title=f"Nobody's asked me about {user.name} yet. Let's have a look.", color = 0xbdbdbd) \
            .add_field(name = 'Calculating...', value = "Please wait, this won't take long.")
            score = random.randint(1,5) 
            userdata["rate"] = score
            glo.USERDATA_WRITE(user.id, userdata)
        embed.set_footer(text = glo.FOOTER())
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(2)
        await msg.edit(embed = glo.GETRATE(score, user)) # Stolen from Anabot

