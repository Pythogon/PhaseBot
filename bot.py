import ast
import asyncio # Imports
import json
import names
import operator
import os
import random
import time

import discord
import glo

from datetime import date
from datetime import timedelta
from discord.ext import commands
from logslist import getLogs
from textgenrnn import textgenrnn

from COGgdpr import GDPR
from COGinstagram import Instagram
from COGstarboard import Starboard

textgen = textgenrnn("local_Store/weights.hdf5") # CommentGenRNN backend loaded

def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])
    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)
    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)
    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.AsyncWith):
        insert_returns(body[-1].body)

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


bot = PhaseBot(command_prefix = glo.PREFIX) # Writing the embed
bot.add_cog(GDPR(bot))
bot.add_cog(Starboard(bot))
bot.remove_command('help') # Removing default help (I don't like it)

@bot.command(name = 'help', aliases = ["?"]) # New help command (help is a registered keyword so we just need to pretend we have a function called 'help')
async def help_command(ctx):
    gdpr_list = jsonRead("gdpr.json")
    try:
        if gdpr_list[str(ctx.author.id)] is not 1: raise ValueError
    except:
        return await ctx.send(embed = glo.GDPR())
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

@bot.command(aliases = ["a"])
async def avatar(ctx, user: discord.User):
    gdpr_list = jsonRead("gdpr.json")
    try:
        if gdpr_list[str(ctx.author.id)] != 1: raise ValueError
    except:
        return await ctx.send(embed = glo.GDPR())
    await ctx.send(user.avatar_url) # Anabot avatar command

@bot.command(aliases = ["sr"])
async def rate(ctx, user: discord.User):
    gdpr_list = jsonRead("gdpr.json")
    try:
        if gdpr_list[str(ctx.author.id)] != 1: raise ValueError
    except:
        return await ctx.send(embed = glo.GDPR())
    fpath = 'rate.json'
    try: scores = jsonRead(fpath)
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
        jsonWrite(fpath, scores)
    embed.set_footer(text = glo.FOOTER())
    msg = await ctx.send(embed=embed)
    await asyncio.sleep(2)
    await msg.edit(embed = glo.GETRATE(score, user)) # Stolen from Anabot

@bot.command(aliases = ["p"])
async def poll(ctx, question, *answers):
    gdpr_list = jsonRead("gdpr.json")
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

@bot.command(aliases = ["i"])
async def info(ctx):
    gdpr_list = jsonRead("gdpr.json")
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

@bot.command(aliases = ["l"])
async def logs(ctx, v: str):
    gdpr_list = jsonRead("gdpr.json")
    try:
        if gdpr_list[str(ctx.author.id)] != 1: raise ValueError
    except:
        return await ctx.send(embed = glo.GDPR())
    embed = await getLogs(v)
    await ctx.send(embed = embed) # See logsembed.py

@bot.command(aliases = ["lg"])
async def lifegen(ctx):
    gdpr_list = jsonRead("gdpr.json")
    try:
        if gdpr_list[str(ctx.author.id)] != 1: raise ValueError
    except:
        return await ctx.send(embed = glo.GDPR())
    embed = discord.Embed(title = "I'm thinking...", color = glo.COLOR
    ).add_field(name = "Consulting CommentGenRNN...", value = "Just one moment."
    ).set_footer(text = glo.FOOTER())
    message = await ctx.send(embed = embed)
    textgen.generate_to_file("local_Store/holding.txt", temperature = 1.0) # CommentGenRNN trained off of all LIFE until Kaiser
    new_embed = discord.Embed(title = "I'm done!", color = 0x00ff00
    ).add_field(name = "Results:", value = fileRead("holding.txt")
    ).set_footer(text = glo.FOOTER())
    await message.edit(embed = new_embed) # CommentGenRNN integration

@bot.command(aliases = ["r"])
async def reload(ctx):
    gdpr_list = jsonRead("gdpr.json")
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
async def votes(ctx, to_check: int):
    gdpr_list = jsonRead("gdpr.json")
    try:
        if gdpr_list[str(ctx.author.id)] != 1: raise ValueError
    except:
        return await ctx.send(embed = glo.GDPR())
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
    embed = discord.Embed(title = "Lemme do the maths...", color = glo.COLOR
    ).add_field(name = f"Running voting results for today:", value = to_send
    ).set_footer(text = glo.FOOTER())
    await ctx.send(embed = embed)

@bot.command(aliases = ["vr"])
async def votesraw(ctx, to_check, loose_checking=False):
    gdpr_list = jsonRead("gdpr.json")
    try:
        if gdpr_list[str(ctx.author.id)] != 1: raise ValueError
    except:
        return await ctx.send(embed = glo.GDPR())
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

@bot.command(aliases = ["c"])
async def comments(ctx, user):
    gdpr_list = jsonRead("gdpr.json")
    try:
        if gdpr_list[str(ctx.author.id)] != 1: raise ValueError
    except:
        return await ctx.send(embed = glo.GDPR())
    comments = ""
    data = jsonRead("sole_nyu/sole_nyu.json")["GraphImages"][0]["comments"]["data"]
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


@bot.command(aliases = ["an"])
@commands.is_owner()
async def announce(ctx, *message):
    gdpr_list = jsonRead("gdpr.json")
    try:
        if gdpr_list[str(ctx.author.id)] != 1: raise ValueError
    except:
        return await ctx.send(embed = glo.GDPR())
    message = " ".join(message)
    embed = discord.Embed(title = "An important update about PhaseBot.", color = glo.COLOR
    ).add_field(name = "Announcement:", value = message
    ).set_footer(text = glo.FOOTER())
    await ctx.send(embed = embed)

@bot.command(aliases = ["n"])
async def name(ctx, gender):
    gdpr_list = jsonRead("gdpr.json")
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

@bot.command(aliases = ["sg"])
async def stargen(ctx):
    gdpr_list = jsonRead("gdpr.json")
    try:
        if gdpr_list[str(ctx.author.id)] != 1: raise ValueError
    except:
        return await ctx.send(embed = glo.GDPR())
    read = len(fileRead("starcastle.txt"))
    percent = float('{:g}'.format(float('{:.{p}g}'.format((read / 100000) * 100, p=4))))
    started = date(2020, 7, 4)
    today = date.today()
    diff = today - started
    until = (started + timedelta(days = round(100 / (percent / diff.days)))).strftime('%Y-%m-%d')
    print(until)
    await ctx.send(f"This isn't available yet! We are {percent}% of the way towards having enough data to implement this command. ETA: {until}.")

@bot.command(aliases = ["id"])
async def checkid(ctx, unkID: int, channelID = 1):
    gdpr_list = jsonRead("gdpr.json")
    try:
        if gdpr_list[str(ctx.author.id)] != 1: raise ValueError
    except:
        return await ctx.send(embed = glo.GDPR())
    try:
        print("0a")
        h = bot.get_channel(unkID)
        if h == None: raise
        print("0b")
        case = 0
    except:
        try:
            print("1a")
            h = bot.get_user(unkID)
            if h == None: raise
            print("1b")
            case = 1
        except:
            try:
                print("2a")
                h = bot.get_emoji(unkID)
                if h == None: raise
                print("2b")
                case = 2
            except:
                try:
                    print("3a")
                    c = bot.get_channel(channelID.id)
                    h = await c.fetch_message(unkID)
                    if h == None: raise
                    print("3b")
                    case = 3
                except:
                    try:
                        print("4a")
                        g = bot.get_guild(709717828365844511)
                        h = g.get_role(unkID)
                        if h == None: raise
                        print("4b")
                        case = 4
                    except:
                        print("5")
                        case = 5
    to_send = {0: "channel", 1: "user", 2: "emoji", 3: "message", 4: "role", 5: "unknown"}.get(case)
    embed = discord.Embed(title = "Searching for ID...", color = glo.COLOR
    ).add_field(name = f"Detected ID type: {to_send}.", value = "If this seems incorrect, check again! If it's suspected to be a message, ensure to add the channel."
    ).set_footer(text = glo.FOOTER())
    await ctx.send(embed = embed)

@bot.command(aliases = ["eval"])
@commands.is_owner()
async def eval_fn(ctx, *, cmd):
    fn_name = "_eval_expr"
    cmd = cmd.strip("` ")
    # add a layer of indentation
    cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
    # wrap in async def body
    body = f"async def {fn_name}():\n{cmd}"
    parsed = ast.parse(body)
    body = parsed.body[0].body
    insert_returns(body)
    env = {'bot': bot, 'discord': discord, 'commands': commands, 'ctx': ctx, '__import__': __import__, "date": date, "timedelta": timedelta, "glo": glo}
    exec(compile(parsed, filename="<ast>", mode="exec"), env)
    result = (await eval(f"{fn_name}()", env))
    await ctx.send(result)


bot.run(fileRead("token"))
