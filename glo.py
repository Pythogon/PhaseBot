import discord
import random

STAR_COUNT = 3
VERSION = "1.1-pre"
PREFIX = ")"
COLOR = 0xff00ff

def FOOTER():
    return "PhaseBot v{} | Made by Pythogon Technologies {}".format(VERSION, {1: "with love. ❤",
                                                                              2: "in discord.py.",
                                                                              3: "on 2020-07-04.",
                                                                              4: "| Error 404: Good code not found.",
                                                                              5: "with special thanks to SoleNyu!",
                                                                              6: "with Anabot.",
                                                                              7: "with CommentGenRNN.",
                                                                              8: "| It's nut free!",
                                                                              9: "with magic and rainbows.",
                                                                              10: "while consulting the deities."}.get(random.randint(1,10)))  # Random footer <3

def GETRATE(l, user):
    varset = {1: ["{} is a lowly triangle, 1/10, not very surreal.",0x5fa8ff,'★☆☆☆☆'],
    2: ["{} seems to be a square - they should visit the Void more often.",0xfffc00,'★★☆☆☆'],
    3: ["{} is a line. Infinite potential for surrealitude, but they're trapped behind their one dimensional view.", 0xffc000,'★★★☆☆'],
    4: ["I think {} is a sphere. Solidly surreal.", 0xff6000,'★★★★☆'],
    5: ['{} is a hypercube, probably working with the surreal council (hide your illegalities).',0xff3030,'★★★★★'],
    6: ['{} is the void itself. What did you expect?',0xff0000,'★★★★★★']}.get(l)
    embed = discord.Embed(title = varset[0].format(user.name), color = varset[1])
    embed.add_field(name = f'Rating: {varset[2]}', value = f'Do you want to know what I think about someone? Do {PREFIX}rate [@user].')
    embed.set_footer(text = footerStr())
    return embed # # Splitting code


def GETEMOJI(l):
    return {0: u"\U0001F7E4",
    1: u"\U0001F7E3",
    2: u"\U0001F7E2",
    3: u"\U0001F7E0"}.get(l) # My beautiful getEmoji
