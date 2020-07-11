import asyncio # Imports
import discord
import glo
import json
import names
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
        if "214771884544229382" in message.content:
            emoji = bot.get_emoji(710243429119950969)
            return await message.add_reaction(emoji) # BEAN
        return await bot.process_commands(message)

    async def on_reaction_add(self, reaction, user):
        message = reaction.message # Let's get the message reactions
        star_list = jsonRead("starcount.json")
        if message.author.bot: return # NO BOTS
        print("a")
        if reaction.emoji != "⭐": return # NO ANYTHING BUT STAR BB
        print("b")
        if reaction.count != glo.STAR_COUNT: return # NO NOT THE LIMIT!
        print("c")
        glo.STAR(message, bot.get_channel(glo.STAR_CHANNEL_ID))
        embed = discord.Embed(title = f"⭐ | {message.author}", color = glo.COLOR) # Making the embed (Magenta)
        embed.add_field(name = "Message:", value = message.content, inline = False)
        embed.add_field(name = "Jump link:", value = message.jump_url, inline = False)
        embed.set_footer(text = glo.FOOTER())
        await star_channel.send(embed = embed) # PhaseBot class
        fileAppend("starcastle.txt", message.content.encode(encoding = "ascii", errors = "ignore").decode())
        try:
            star_list[str(user.id)] += 1
        except:
            star_list[str(user.id)] = 1
        jsonWrite("starcount.json", star_list)

bot = PhaseBot(command_prefix = glo.PREFIX) # Writing the embed
bot.remove_command('help') # Removing default help (I don't like it)

@bot.command(name = 'help', aliases = ["?"]) # New help command (help is a registered keyword so we just need to pretend we have a function called 'help')
async def help_command(ctx):
    """ Basic bitch help command (by Ash) """
    title = discord.Embed(title = 'Help', color = glo.COLOR)
    title.add_field(name = 'Welcome to PhaseBot!', value = f"""
Commands:
{glo.PREFIX}starinfo|si
{glo.PREFIX}avatar|a <user>
{glo.PREFIX}rate|sr <user>
{glo.PREFIX}poll|p \"Question\" answers|here
{glo.PREFIX}info|i
{glo.PREFIX}logs|l <version>
{glo.PREFIX}generate|lg
{glo.PREFIX}stargen|sg
{glo.PREFIX}reload|r
{glo.PREFIX}votes|v <number of choices>
{glo.PREFIX}votesraw|vr <chars to check>
{glo.PREFIX}name|n <m|f|n>
{glo.PREFIX}comments|c <IG user>""", inline = True) # Help and informmation #
    title.set_footer(text = glo.FOOTER())
    await ctx.send(embed = title) # Anabot help

@bot.command(aliases = ["si"])
async def starinfo(ctx):
    """Starboard info"""
    embed = discord.Embed (title = "What the hell is a starboard?", color = glo.COLOR)
    embed.add_field(name = "The starboard", value = f"""The starboard is a way of saving messages that the community finds funny, clever, etc. It operates like the Quote Vault, but is purely democratic.

You can add to the starboard by reacting to a message with the ⭐ emoji. If the message gets {glo.STAR_COUNT} ⭐s, it will be added to the starcastle channel automatically.

If a message of your's that you don't like made it to the board, you can just ask Ash to delete it.""")
    embed.set_footer(text = glo.FOOTER())
    await ctx.send(embed = embed) # Starboard help

@bot.command(aliases = ["a"])
async def avatar(ctx, user: discord.User):
    await ctx.send(user.avatar_url) # Anabot avatar command

@bot.command(aliases = ["sr"])
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

@bot.command(aliases = ["p"])
async def poll(ctx, question, *answers):
    answers = " ".join(answers) # Anabot interpreter
    answers = list(answers.split("|")) # Listify!
    if len(answers) > 4: return await ctx.send("You can have a maximum of 4 answers.") # ERR
    to_send = f"__New poll: **{question}**__"
    for x in range(len(answers)): to_send += "\n" + glo.GETEMOJI(x) + ": " + answers[x]
    message = await ctx.send(to_send)
    for x in range(len(answers)): await message.add_reaction(glo.GETEMOJI(x)) # GETEMOJI[x]

@bot.command(aliases = ["i"])
async def info(ctx):
    embed = discord.Embed(title = "About PhaseBot", color = glo.COLOR)
    embed.add_field(name = "Developer", value = "PhaseBot was created for LIFE: The Game by [Ash](https://kaidev.uk) on behalf of [Pythogon Technologies](https://github.com/Pythogon).", inline = False)
    embed.add_field(name = "More Info", value = f"PhaseBot is currently on Version {glo.VERSION}. The project started on 2020-07-04.", inline = False)
    embed.add_field(name = "Special Thanks", value = "Special thanks to all who worked on [Anabot](https://github.com/Pythogon/Anabot) and [CommentGenRNN](https://github.com/Pythogon/CommentGenRNN) for providing considerable contributions to PhaseBot.", inline = False)
    embed.add_field(name = "GitHub.", value = "You can find PhaseBot's GitHub [here](https://github.com/Pythogon/PhaseBot) and take a look at its source code! If you posess developing talents, feel free to send a PR our way, we'd be happy to take on any suggestions.", inline = False)
    embed.set_footer(text = glo.FOOTER())
    await ctx.send(embed = embed) # Credits :)

@bot.command(aliases = ["l"])
async def logs(ctx, v: str):
    embed = await getLogs(v)
    embed.set_footer(text = glo.FOOTER())
    await ctx.send(embed = embed) # See logsembed.py

@bot.command(aliases = ["lg"])
async def generate(ctx):
    embed = discord.Embed(title = "I'm thinking...", color = glo.COLOR)
    embed.add_field(name = "Consulting CommentGenRNN...", value = "Just one moment.")
    embed.set_footer(text = glo.FOOTER())
    message = await ctx.send(embed = embed)
    textgen.generate_to_file("local_Store/holding.txt", temperature = 1.0) # CommentGenRNN trained off of all LIFE until Kaiser
    new_embed = discord.Embed(title = "I'm done!", color = 0x00ff00)
    new_embed.add_field(name = "Results:", value = fileRead("holding.txt"))
    new_embed.set_footer(text = glo.FOOTER())
    await message.edit(embed = new_embed) # CommentGenRNN integration

@bot.command(aliases = ["r"])
async def reload(ctx):
    embed = discord.Embed(title = "Polling Instagram...", color = glo.COLOR)
    embed.add_field(name = "It won't be a minute.", value = "Apologies for the wait!")
    embed.set_footer(text = glo.FOOTER())
    message = await ctx.send(embed = embed)
    await bot.change_presence(activity = discord.Activity(name = f"Instagram - Loading...", type = discord.ActivityType.watching)) # Simplistic help
    os.system("scrape.bat")
    await bot.change_presence(activity = discord.Activity(name = f"le noir | v{glo.VERSION}", type = discord.ActivityType.watching)) # Simplistic help
    new_embed = discord.Embed(title = "Poll complete!", color = 0x00ff00)
    new_embed.add_field(name = f"{glo.PREFIX}votes has now been filled with new information!", value = "You can see how this worked over at [InstaScrape](https://github.com/Pythogon/InstaScrape/).")
    new_embed.set_footer(text = glo.FOOTER())
    await message.edit(embed = new_embed)

@bot.command(aliases = ["v"])
async def votes(ctx, to_check: int, ):
    letters = []
    no = []
    percentage = []
    read = jsonRead("sole_nyu/sole_nyu.json")["GraphImages"][0]["comments"]["data"]
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
    embed = discord.Embed(title = "Lemme do the maths...", color = glo.COLOR)
    embed.add_field(name = f"Running voting results for today ({str(abs(100 - total_percentage))[:5]}% potential error):", value = to_send)
    embed.set_footer(text = glo.FOOTER())
    await ctx.send(embed = embed)

@bot.command(aliases = ["vr"])
async def votesraw(ctx, to_check, loose_checking=False):
    letters = list(to_check)
    no = []
    percentage = []
    read = jsonRead("sole_nyu/sole_nyu.json")["GraphImages"][0]["comments"]["data"]
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
        for comment in read:
            author = comment["owner"]["username"]
            is_yes = False
            if author in voted: continue
            if loose_checking == False:
                if letters[x] == comment["text"][0].upper(): yes[x] += 1; voted.append(author); is_yes = True
            else:
                if letters[x] in comment["text"].upper(): yes[x] += 1; voted.append(author); is_yes = True
            if is_yes == False: no[x] += 1
        percentage[x] = str((yes[x] / (yes[x] + no[x])) * 100)[:5]
        total_percentage += float(percentage[x])
        total_yes += yes[x]

    for x in range(to_check): to_send += f"{letters[x]}: {str((yes[x] / total_yes) * 100)[:5]}% ({yes[x]} counted).\n"
    embed = discord.Embed(title = "Lemme do the maths...", color = glo.COLOR)
    embed.add_field(name = f"Running voting results for today ({str(abs(100 - total_percentage))[:5]}% potential error):", value = to_send)
    embed.set_footer(text = glo.FOOTER())
    await ctx.send(embed = embed)

@bot.command(aliases = ["c"])
async def comments(ctx, user):
    comments = ""
    data = jsonRead("sole_nyu/sole_nyu.json")["GraphImages"][0]["comments"]["data"]
    for comment in data:
        if user == comment["owner"]["username"]: comments += comment["text"] + "\n"
    if comments == "":
        embed = discord.Embed(title = "No comments found!", color = 0xff0000)
        embed.add_field(name = "Maybe they got dissolved by adimensia...", value = "Ensure you're typing the username correctly.")
        embed.set_footer(text = glo.FOOTER())
        return await ctx.send(embed = embed)
    embed = discord.Embed(title = "Comments found!", color = glo.COLOR)
    embed.add_field(name = f"{user}'s comments:", value = comments)
    embed.set_footer(text = glo.FOOTER())
    await ctx.send(embed = embed)


@bot.command(aliases = ["an"])
@commands.is_owner()
async def announce(ctx, *message):
    message = " ".join(message)
    embed = discord.Embed(title = "An important update about PhaseBot.", color = glo.COLOR)
    embed.add_field(name = "Announcement:", value = message)
    embed.set_footer(text = glo.FOOTER())
    await ctx.send(embed = embed)

@bot.command(aliases = ["n"])
async def name(ctx, gender):
    if gender == "m" or gender == "f":
        name = names.get_full_name(gender = {"m": "male", "f": "female"}.get(gender))
    else:
        name = names.get_full_name()
    label = {"m": "male", "f": "female"}.get(gender, "random")
    embed = discord.Embed(title = f"Generating a {label} name...", color = glo.COLOR)
    embed.add_field(name = f"The name I came up with is {name}.", value = "Feel free to run the command again!")
    embed.set_footer(text = glo.FOOTER())
    await ctx.send(embed = embed)

@bot.command(aliases = ["sg"])
async def stargen(ctx):
    read = len(fileRead("starcastle.txt"))
    read = read / 1000
    await ctx.send(f"This isn't available yet! We are {read}% of the way towards having enough data to implement this command.")

@bot.command(aliases = ["sc"])
async def starcount(ctx):
    star_list = jsonRead("starcount.json")
    try: count = star_list[str(ctx.author.id)]
    except: count = 0; star_list[str(ctx.author.id)] = 0; jsonWrite("starcount.json", star_list)
    embed = discord.Embed(title = "Let me quickly check...", color = glo.COLOR).add_field(name = f"You currently have {count} stars.", value = "Stars before 2020-07-11 weren't counted.").set_footer(text = glo.FOOTER())
    await ctx.send(embed = embed)

@bot.command(aliases = ["fs"])
async def forcestar(ctx, id: int):
    try:
        glo.STAR(bot.get_message(id), bot.get_channel(glo.STAR_CHANNEL_ID))

bot.run(fileRead("token"))
