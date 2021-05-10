import discord
import json
import math
import random
import sys

from discord.ext import commands

ANNOUNCEMENT_CHANNEL_ID = 797176212594098187 #phasebot_announcements
COLOR = 0xff00ff
COUNTING_CHANNEL = 828554535949041684
CURRENT_NAMES = {}
DAILY_MIN = 20 # Dailies
DAILY_MAX = 50
DATE_FORMAT_HOUR_EXCLUSIVE = "%Y-%m-%d" # Day format
DATE_FORMAT_HOUR_INCLUSIVE = "%H:%M:%S on %Y-%m-%d" # Time format
DEVELOPER_ROLE_ID = 732384059191328809 # Developer role
ERROR_COLOR = 0xff0000
GUILD_ID = 709717828365844511 # LIFE: The Game
MAIN_CHANNEL_ID = 709717829112561776 #le-noir
MONEY_MESSAGE_INTERVAL = 1000
MONEY_MESSAGE_MAX = 30
MONEY_MESSAGE_MIN = 10
MONEY_MESSAGE_MINLENGTH = 15
MONEY_MESSAGE_PERDAY = 7
PREFIX = ")" 
RANDOM_FOOTERS = {1: "with love. ❤",
2: "in discord.py.",
3: "on 2020-07-04.",
4: "| Error 404: Good code not found.",
5: "with special thanks to Erika!",
6: "with Anabot.",
7: "with no added sugar!",
8: "| It's nut free!",
9: "with magic and rainbows.",
10: "while consulting the deities.",
11: "on behalf of a very caffeinated frog.",
12: "| If you find a bug, feel free to report it!",
13: "with thanks to bekano_cat for her artistic talent!",
14: "because even monsters deserve love. ❤",
15: "rising from the ashes.",
16: "with unintentional help from distopioid!",
17: "to cultivate psychedelic cacti - not for consumption (for legal reasons)" #cool tomato
} 
RANDOM_CURRENCY_CHANCE = 25
RANDOM_SHOP_THRESHOLD = 2
REVIVE_COST = 1000
SHOP_BASE_PRICE = 15
SHOP_ITEM_COUNT = 4
SHOP_RARITY_EXPONENT = 1.9
STAR_COUNT = 3 # Amount of stars needed for a message to get onto the starboard
STAR_CHANNEL_ID = 728440495105114173 #starcastle
STAR_MESSAGE_MIN = 20
STAR_MESSAGE_MAX = 60
TAX_BRACKETS = {500: 90,
900: 87,
1000: 85,
1100: 80,
1300: 70,
1700: 60,
1900: 50,
2100: 40,
2200: 30,
2250: 20,
2300: 10,
2350: 0}
TEMP_MESSAGE_LIST = []
VERSION = "3.1.3" # Current version (entirely symbolic, means nothing)

def BANKFORMAT(num):
    if num == 1: out = "<:bean:710243429119950969>"
    else: out = "<:bean:710243429119950969>s"
    return out

def CALCULATE_TAX(income, balance):
    for x in range(len(TAX_BRACKETS)):
        if x == 0:
            bracket = tuple(TAX_BREACKETS.items())[x]
        else:
            bracket = tuple(TAX_BRACKETS.items())[x+1]
        max_balance = bracket[0]
        takehome = bracket[1]
        if balance <= max_balance:
            after_tax = math.ceil((income * (takehome/100)))
            tax = income - after_tax
            brace = 100 - takehome
            return [after_tax, tax, brace]

def FOOTER(): # Random footer generator
    x = random.randint(1, len(RANDOM_FOOTERS))
    return "PhaseBot v{} | Made by Pythogon Technologies {}".format(VERSION, RANDOM_FOOTERS.get(x))  # Random footer <3

def GETEMOJI(l):
    return {0: u"\U0001F7E4", 1: u"\U0001F7E3", 2: u"\U0001F7E2", 3: u"\U0001F7E0"}.get(l) # Returns unicode for coloured circles

def GETRATE(l, user):
    varset = {-1: ['Error 404: {} not found.', 0xffffff, '☆'],
    1: ["{} is a lowly triangle, 1/10, not very surreal.",0x5fa8ff,'★☆☆☆☆'],
    2: ["{} seems to be a square - they should visit the Void more often.",0xfffc00,'★★☆☆☆'],
    3: ["{} is a line. Infinite potential for surrealitude, but they're trapped behind their one dimensional view.", 0xffc000,'★★★☆☆'],
    4: ["I think {} is a sphere. Solidly surreal.", 0xff6000,'★★★★☆'],
    5: ['{} is a hypercube, probably working with the surreal council (hide your illegalities).',0xff3030,'★★★★★'],
    6: ['{} is the void itself. What did you expect?',0xff0000,'★★★★★★']}.get(l)
    embed = discord.Embed(title = varset[0].format(user.name), color = varset[1]) \
    .add_field(name = f'Rating: {varset[2]}', value = f'Do you want to know what I think about someone? Do {PREFIX}rate [@user].') \
    .set_footer(text = FOOTER())
    return embed # Fully formed embed using a dictionary jump table

def SETNAME(user, name):
    global CURRENT_NAMES
    CURRENT_NAMES[user] = name

async def STAR(message, star_channel):
    reward = random.randint(STAR_MESSAGE_MIN, STAR_MESSAGE_MAX)
    userdata = USERDATA_READ(message.author.id)
    tax = CALCULATE_TAX(reward, userdata["currency"])
    embed = discord.Embed(title = f"⭐ | {message.author}", color = COLOR) \
    .add_field(name = "Message:", value = message.content, inline = False) \
    .add_field(name = "Jump link:", value = message.jump_url, inline = False) \
    .add_field(name = f"Reward given after tax (tax charged at {tax[2]}%):", value = f"{tax[0]} {BANKFORMAT(tax[0])}", inline=False) \
    .set_footer(text = FOOTER())
    await star_channel.send(embed = embed) # PhaseBot class
    FILEAPPEND("starcastle.txt", message.content.encode(encoding = "ascii", errors = "ignore").decode().replace("\n", "")) # Adding to starcastle.txt
    userdata["starcount"] += 1
    userdata["currency"] += tax[0]
    USERDATA_WRITE(message.author.id, userdata)
    tax_amount = int(GLOBAL_READ("tax"))
    tax_amount = str(tax_amount + tax[1])
    GLOBAL_WRITE("tax", tax_amount)


# Global file mod functions

def FILEAPPEND(fpath, data):
    try:
        fpath = f"{sys.argv[1]}/{fpath}"
    except:
        fpath = f"local_Store/{fpath}"
    with open(fpath, "a", encoding = "utf-8") as file: file.write("\n" + data)

def FILEREAD(fpath):
    try:
        fpath = f"{sys.argv[1]}/{fpath}"
    except:
        fpath = f"local_Store/{fpath}"
    with open(fpath, "r", encoding = "utf-8") as file: return file.read() 

def FILEWRITE(fpath, data):
    try:
        fpath = f"{sys.argv[1]}/{fpath}"
    except:
        fpath = f"local_Store/{fpath}"
    with open(fpath, "w", encoding = "utf-8") as file: file.write(data)

def JSONREAD(fpath):
    try:
        fpath = f"{sys.argv[1]}/{fpath}"
    except:
        fpath = f"local_Store/{fpath}"
    with open(fpath, 'r', encoding = "utf-8") as json_file: return json.load(json_file) 

def JSONWRITE(fpath, data):
    try:
        fpath = f"{sys.argv[1]}/{fpath}"
    except:
        fpath = f"local_Store/{fpath}"
    with open(fpath, 'w', encoding = "utf-8") as outfile: json.dump(data,outfile)

def USERDATA_READ(user):
    """
    Usage: "user" = ctx.author.id
    """
    full_data = JSONREAD("userdata.json")
    try:
        return full_data[str(user)]
    except:
        return full_data["default"]

def USERDATA_WRITE(user, data):
    full_data = JSONREAD("userdata.json")
    full_data[str(user)] = data
    JSONWRITE("userdata.json", full_data)

def GLOBAL_READ(var):
    full_data = JSONREAD("globaldata.json")
    return full_data[var]

def GLOBAL_WRITE(var, data):
    full_data = JSONREAD("globaldata.json")
    full_data[var] = data
    JSONWRITE("globaldata.json", full_data)
