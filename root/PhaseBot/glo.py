import discord
import json
import random

COLOR = 0xff00ff
DEVELOPER_ROLE_ID = 732384059191328809
GUILD_ID = 709717828365844511
MAIN_CHANNEL_ID = 709717829112561776
PREFIX = ")"
STAR_COUNT = 3
STAR_CHANNEL_ID = 728440495105114173
DATE_FORMAT_HOUR_EXCLUSIVE = "%Y-%m-%d"
DATE_FORMAT_HOUR_INCLUSIVE = "%H:%M:%S on %Y-%m-%d"
VERSION = "2.0-pre"

def FOOTER():
    """
    The random footer generator for PhaseBot embeds.
    """
    return "PhaseBot v{} | Made by Pythogon Technologies {}".format(VERSION, {1: "with love. ❤",
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
                                                                              13: "with thanks to our bug fixers: <insert them here>"}.get(random.randint(1,12)))  # Random footer <3

def GDPR():
    """
    Privacy agreement not signed handling.
    """
    return discord.Embed(title = "Sorry, but you need to agree to our privacy agreement!", color = 0xff0000
    ).add_field(name = "Your privacy is important to us...", value = f"""In compliance with the EU's General Data Protection Regulation (GDPR), we're requiring all users to agree to their data being stored.
    PhaseBot uses and stores only the data that is essential to its operaton.
    You can learn more about the data we store by running {PREFIX}gdpr, or accept it by typing {PREFIX}accept."""
    ).set_footer(text = FOOTER())

def GETEMOJI(l):
    return {0: u"\U0001F7E4", 1: u"\U0001F7E3", 2: u"\U0001F7E2", 3: u"\U0001F7E0"}.get(l) # My beautiful getEmoji

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
    return embed # # Splitting code

async def STAR(message, star_channel):
    star_list = JSONREAD("starcount.json")
    embed = discord.Embed(title = f"⭐ | {message.author}", color = COLOR
    ).add_field(name = "Message:", value = message.content, inline = False
    ).add_field(name = "Jump link:", value = message.jump_url, inline = False
    ).set_footer(text = FOOTER())
    await star_channel.send(embed = embed) # PhaseBot class
    FILEAPPEND("starcastle.txt", message.content.encode(encoding = "ascii", errors = "ignore").decode())
    try:
        star_list[str(message.author.id)] += 1
    except:
        star_list[str(message.author.id)] = 1
    JSONWRITE("starcount.json", star_list)

# Global file mod functions

def JSONREAD(fpath):
    fpath = f"local_Store/{fpath}"
    with open(fpath, 'r', encoding = "utf-8") as json_file: return json.load(json_file) # Anabot JSON read

def JSONWRITE(fpath, data):
    fpath = f"local_Store/{fpath}"
    with open(fpath, 'w', encoding = "utf-8") as outfile: json.dump(data,outfile) # Anabot JSON write

def FILEREAD(fpath):
    fpath = f"local_Store/{fpath}"
    with open(fpath, "r", encoding = "utf-8") as file: return file.read() # TXT read

def FILEAPPEND(fpath, data):
    fpath = f"local_Store/{fpath}"
    with open(fpath, "a", encoding = "utf-8") as file: file.write("\n" + data)
