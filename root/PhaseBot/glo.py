import discord
import json
import random

from discord.ext import commands

COLOR = 0xff00ff # Magenta, 255 0 255
DEVELOPER_ROLE_ID = 732384059191328809 # Developer role
ERROR_COLOR = 0xff0000
GUILD_ID = 709717828365844511 # LIFE: The Game
MAIN_CHANNEL_ID = 709717829112561776 #le-noir
PREFIX = ")" 
RANDOM_FOOTERS = {1: "with love. ❤",
2: "in discord.py.",
3: "on 2020-07-04.",
4: "| Error 404: Good code not found.",
5: "with special thanks to SoleNyu!",
6: "with Anabot.",
7: "with CommentGenRNN.",
8: "| It's nut free!",
9: "with magic and rainbows.",
10: "while consulting the deities.",
11: "on behalf of a very caffeinated frog.",
12: "| If you find a bug, feel free to report it!",
13: "with thanks to bekano_cat for her artistic talent!"} 
STAR_COUNT = 3 # Amount of stars needed for a message to get onto the starboard
STAR_CHANNEL_ID = 728440495105114173 #starcastle
DATE_FORMAT_HOUR_EXCLUSIVE = "%Y-%m-%d" # Day format
DATE_FORMAT_HOUR_INCLUSIVE = "%H:%M:%S on %Y-%m-%d" # Time format
VERSION = "2.0-pre" # Current version (entirely symbolic, means nothing)

def FOOTER(x = random.randint(1, len(RANDOM_FOOTERS))): # Random footer generator
    return "PhaseBot v{} | Made by Pythogon Technologies {}".format(VERSION, RANDOM_FOOTERS.get(x))  # Random footer <3

def GDPR(): # Embed for GDPR handler (no relation to Cogs.GDPR or the command )gdpr)
    return discord.Embed(title = "Sorry, but you need to agree to our privacy agreement!", color = 0xff0000
    ).add_field(name = "Your privacy is important to us...", value = f"""In compliance with the EU's General Data Protection Regulation (GDPR), we're requiring all users to agree to their data being stored.
    PhaseBot uses and stores only the data that is essential to its operaton.
    You can learn more about the data we store by running {PREFIX}gdpr, or accept it by typing {PREFIX}accept."""
    ).set_footer(text = FOOTER())

def GETEMOJI(l):
    return {0: u"\U0001F7E4", 1: u"\U0001F7E3", 2: u"\U0001F7E2", 3: u"\U0001F7E0"}.get(l) # Returns unicode for coloured circles

def GETRATE(l, user):
    varset = {1: ["{} is a lowly triangle, 1/10, not very surreal.",0x5fa8ff,'★☆☆☆☆'],
    2: ["{} seems to be a square - they should visit the Void more often.",0xfffc00,'★★☆☆☆'],
    3: ["{} is a line. Infinite potential for surrealitude, but they're trapped behind their one dimensional view.", 0xffc000,'★★★☆☆'],
    4: ["I think {} is a sphere. Solidly surreal.", 0xff6000,'★★★★☆'],
    5: ['{} is a hypercube, probably working with the surreal council (hide your illegalities).',0xff3030,'★★★★★'],
    6: ['{} is the void itself. What did you expect?',0xff0000,'★★★★★★']}.get(l)
    embed = discord.Embed(title = varset[0].format(user.name), color = varset[1])
    embed.add_field(name = f'Rating: {varset[2]}', value = f'Do you want to know what I think about someone? Do {PREFIX}rate [@user].')
    embed.set_footer(text = FOOTER())
    return embed # Fully formed embed using a dictionary jump table

async def STAR(message, star_channel):
    star_list = JSONREAD("starcount.json")
    embed = discord.Embed(title = f"⭐ | {message.author}", color = COLOR
    ).add_field(name = "Message:", value = message.content, inline = False
    ).add_field(name = "Jump link:", value = message.jump_url, inline = False
    ).set_footer(text = FOOTER())
    await star_channel.send(embed = embed) # PhaseBot class
    FILEAPPEND("starcastle.txt", message.content.encode(encoding = "ascii", errors = "ignore").decode().replace("\n", "")) # Adding to starcastle.txt
    try:
        star_list[str(message.author.id)] += 1 # Add 1
    except:
        star_list[str(message.author.id)] = 1 # Create an entry for the user (they haven't run )sc or recieved a starboard msg before)
    JSONWRITE("starcount.json", star_list) 

# Global file mod functions


def FILEAPPEND(fpath, data):
    fpath = f"local_Store/{fpath}"
    with open(fpath, "a", encoding = "utf-8") as file: file.write("\n" + data)

def FILEREAD(fpath):
    fpath = f"local_Store/{fpath}"
    with open(fpath, "r", encoding = "utf-8") as file: return file.read() 

def JSONREAD(fpath):
    fpath = f"local_Store/{fpath}"
    with open(fpath, 'r', encoding = "utf-8") as json_file: return json.load(json_file) 

def JSONWRITE(fpath, data):
    fpath = f"local_Store/{fpath}"
    with open(fpath, 'w', encoding = "utf-8") as outfile: json.dump(data,outfile)

# Custom errors

class GDPRFailError(commands.CommandError): pass

# Custom checks

def gdpr_check():
    def predicate(ctx):
        gdpr_list = JSONREAD("gdpr.json")
        try:
            if gdpr_list[str(ctx.author.id)] != 1: raise ValueError
            return True
        except:
            return False
    return commands.check(predicate)
    