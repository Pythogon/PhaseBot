import asyncio # Imports
import discord
import glo
import json
import os
import random
import time

from discord.ext import commands # From imports
from logslist import getLogs
from textgenrnn import textgenrnn

textgen = textgenrnn("local_Store/weights.hdf5") # CommentGenRNN backend loaded

def jsonRead(fpath):
    fpath = f"local_Store/{fpath}"
    with open(fpath, 'r', encoding = "utf-8") as json_file: return json.load(json_file) # Anabot JSON read

def jsonWrite(fpath, data):
    fpath = f"local_Store/{fpath}"
    with open(fpath, 'w', encoding = "utf-8") as outfile: json.dump(data,outfile) # Anabot JSON write

def fileRead(fpath):
    fpath = f"local_Store/{fpath}"
    with open(fpath, "r", encoding = "utf-8") as file: return file.read() # TXT read

class PhaseBot(commands.Bot):
    """ The bot """
    async def on_ready(self):
        print("LOAD") # Great, it's working
        os.system("scrape.bat")
        embed = discord.Embed(title = "Phaser has phased in!", color = 0xff00ff)
        embed.add_field(name = "We're online!", value = "All messages before this have been cleared from cache and are no longer eligible for starcastle.")
        embed.set_footer(text = glo.FOOTER())
        #await bot.get_channel(709717829112561776).send(embed = embed) # Optional file send
        await bot.change_presence(activity = discord.Activity(name = f"le noir | v{glo.VERSION}", type = discord.ActivityType.watching)) # Simplistic help

    async def on_message(self, message):
        if message.author.bot: return # We don't like bots
        if "214771884544229382" in message.content:
            emoji = bot.get_emoji(710243429119950969)
            return await message.add_reaction(emoji) # BEAN
        return await bot.process_commands(message)

    async def on_reaction_add(self, reaction, user):
        message = reaction.message # Let's get the message reactions
        star_channel = bot.get_channel(728440495105114173) #starcastle on LIFE: The Game
        if message.author.bot: return # NO BOTS
        print("a")
        if reaction.emoji != "⭐": return # NO ANYTHING BUT STAR BB
        print("b")
        if reaction.count != glo.STAR_COUNT: return # NO NOT THE LIMIT!
        print("c")
        embed = discord.Embed(title = f"⭐ | {message.author}", color = 0xff00ff) # Making the embed (Magenta)
        embed.add_field(name = "Message:", value = message.content, inline = False)
        embed.add_field(name = "Jump link:", value = message.jump_url, inline = False)
        embed.set_footer(text = glo.FOOTER())
        await star_channel.send(embed = embed) # PhaseBot class

bot = PhaseBot(command_prefix = glo.PREFIX) # Writing the embed
bot.remove_command('help') # Removing default help (I don't like it)

@bot.command(name = 'help') # New help command (help is a registered keyword so we just need to pretend we have a function called 'help')
async def help_command(ctx):
    """ Basic bitch help command (by Ash) """
    title = discord.Embed(title = 'Help', color = 0xff00ff)
    title.add_field(name = 'Welcome to PhaseBot!', value = f"""
Commands:
{glo.PREFIX}starinfo
{glo.PREFIX}avatar <user>
{glo.PREFIX}rate <user>
{glo.PREFIX}poll \"Question\" answers|here
{glo.PREFIX}info
{glo.PREFIX}logs <version>
{glo.PREFIX}generate
{glo.PREFIX}reload
{glo.PREFIX}votes <letter>""", inline = True) # Help and informmation #
    title.set_footer(text = glo.FOOTER())
    await ctx.send(embed = title) # Anabot help

@bot.command()
async def starinfo(ctx):
    """Starboard info"""
    embed = discord.Embed (title = "What the hell is a starboard?", color = 0xff00ff)
    embed.add_field(name = "The starboard", value = f"""The starboard is a way of saving messages that the community finds funny, clever, etc. It operates like the Quote Vault, but is purely democratic.

You can add to the starboard by reacting to a message with the ⭐ emoji. If the message gets {glo.STAR_COUNT} ⭐s, it will be added to the starcastle channel automatically.

If a message of your's that you don't like made it to the board, you can just ask Ash to delete it.""")
    embed.set_footer(text = glo.FOOTER())
    await ctx.send(embed = embed) # Starboard help

@bot.command()
async def avatar(ctx, user: discord.User):
    await ctx.send(user.avatar_url) # Anabot avatar command

@bot.command()
async def rate(ctx, user: discord.User):
    fpath = 'rate.json'
    try: scores = jsonRead(fpath)
    except: await ctx.send('ERR')
    try:
        score = int(scores[str(user.id)])
        embed = discord.Embed(title=f"Someone's already asked about {user.name}. One moment...", color = 0xbdbdbd)
        embed.add_field(name = 'Fetching...', value = "Please wait, this won't take long.")
    except:
        embed = discord.Embed(title=f"Nobody's asked me about {user.name} yet. Let's have a look.", color = 0xbdbdbd)
        embed.add_field(name = 'Calculating...', value = "Please wait, this won't take long.")
        score = random.randint(1,5)
        scores[str(user.id)] = str(score)
        jsonWrite(fpath, scores)
    embed.set_footer(text = glo.FOOTER())
    msg = await ctx.send(embed=embed)
    await asyncio.sleep(2)
    await msg.edit(embed = glo.GETRATE(score, user)) # Stolen from Anabot

@bot.command()
async def poll(ctx, question, *answers):
    answers = " ".join(answers) # Anabot interpreter
    answers = list(answers.split("|")) # Listify!
    if len(answers) > 4: return await ctx.send("You can have a maximum of 4 answers.") # ERR
    to_send = f"__New poll: **{question}**__"
    for x in range(len(answers)): to_send += "\n" + glo.GETEMOJI(x) + ": " + answers[x]
    message = await ctx.send(to_send)
    for x in range(len(answers)): await message.add_reaction(glo.GETEMOJI(x)) # GETEMOJI[x]

@bot.command()
async def info(ctx):
    embed = discord.Embed(title = "About PhaseBot", color = 0xff00ff)
    embed.add_field(name = "Developer", value = "PhaseBot was created for LIFE: The Game by [Ash](https://kaidev.uk) on behalf of [Pythogon Technologies](https://github.com/Pythogon).", inline = False)
    embed.add_field(name = "More Info", value = f"PhaseBot is currently on Version {glo.VERSION}. The project started on 2020-07-04.", inline = False)
    embed.add_field(name = "Special Thanks", value = "Special thanks to all who worked on [Anabot](https://github.com/Pythogon/Anabot) and [CommentGenRNN](https://github.com/Pythogon/CommentGenRNN) for providing considerable contributions to PhaseBot.", inline = False)
    embed.add_field(name = "GitHub.", value = "You can find PhaseBot's GitHub [here](https://github.com/Pythogon/PhaseBot) and take a look at its source code! If you posess developing talents, feel free to send a PR our way, we'd be happy to take on any suggestions.", inline = False)
    embed.set_footer(text = glo.FOOTER())
    await ctx.send(embed = embed) # Credits :)

@bot.command()
async def logs(ctx, v: str):
    embed = await getLogs(v)
    embed.set_footer(text = glo.FOOTER())
    await ctx.send(embed = embed) # See logsembed.py

@bot.command()
async def generate(ctx):
    embed = discord.Embed(title = "I'm thinking...", color = 0xff00ff)
    embed.add_field(name = "Consulting CommentGenRNN...", value = "Just one moment.")
    embed.set_footer(text = glo.FOOTER())
    message = await ctx.send(embed = embed)
    textgen.generate_to_file("local_Store/holding.txt", temperature = 1.0) # CommentGenRNN trained off of all LIFE until Kaiser
    new_embed = discord.Embed(title = "I'm done!", color = 0x00ff00)
    new_embed.add_field(name = "Results:", value = fileRead("holding.txt"))
    new_embed.set_footer(text = glo.FOOTER())
    await message.edit(embed = new_embed) # CommentGenRNN integration

@bot.command()
async def reload(ctx):
    embed = discord.Embed(title = "Polling Instagram...", color = 0xff00ff)
    embed.add_field(name = "It won't be a minute.", value = "Apologies for the wait!")
    embed.set_footer(text = glo.FOOTER())
    message = await ctx.send(embed = embed)
    os.system("scrape.bat")
    new_embed = discord.Embed(title = "Poll complete!", color = 0x00ff00)
    new_embed.add_field(name = f"{glo.PREFIX}votes has now been filled with new information!", value = "You can see how this worked over at [InstaScrape](https://github.com/Pythogon/InstaScrape/).")
    new_embed.set_footer(text = glo.FOOTER())
    await message.edit(embed = new_embed)

@bot.command()
async def votes(ctx, to_check: int):
    yes = []
    no = []
    letters = []
    percentage = []
    total_percentage = 0.0
    for x in range(to_check):
        yes.append(0)
        no.append(0)
        letters.append(chr(65 + x))
        percentage.append("")
    read = jsonRead("sole_nyu/sole_nyu.json")
    data = read["GraphImages"][0]["comments"]["data"]
    for x in range(to_check):
        for comment in data:
            if letters[x] in comment["text"]:
                yes[x] += 1
            else:
                no[x] += 1
    to_send = ""
    for x in range(to_check):
        percentage[x] = str((yes[x] / (yes[x] + no[x])) * 100)[:5]
        to_send += f"{percentage[x]}% of people voted for {letters[x]} ({yes[x]} counted.)\n"
        total_percentage += float(percentage[x])
    embed = discord.Embed(title = "Lemme do the maths...", color = 0xff00ff)
    embed.add_field(name = f"Running voting results for today ({str(abs(100 - total_percentage))[:5]}% potential error):", value = to_send)
    embed.set_footer(text = glo.FOOTER())
    await ctx.send(embed = embed)

@bot.command()
@commands.is_owner()
async def announce(ctx, *message):
    message = " ".join(message)
    embed = discord.Embed(title = "An important update about PhaseBot.", color = 0xff00ff)
    embed.add_field(name = "Announcement:", value = message)
    embed.set_footer(text = glo.FOOTER())
    await ctx.send(embed = embed)

bot.run(fileRead("token"))
