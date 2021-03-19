import asyncio
import discord
import glo #pylint: disable=import-error
import math
import random
import time

from discord.ext import commands
from discord.utils import get

global purchases
purchases = 0
# Items further down the list are rarer
global items
items = [
    "📱",
    "🪓",
    "💡",
    "📀",
    "🛡️",
    "🔮",
    "⭐",
    "🌟",
    "🗡️",
    "👑",
    "bean"
]
global custom_emoji_map 
custom_emoji_map = {
    "bean": "710243429119950969"
}

global current_items
current_items = list()

def getprice(item):
    if item in custom_emoji_map.values():
        return glo.SHOP_BASE_PRICE + (pow(items.index(custom_emoji_map.values()[list(custom_emoji_map.keys()).index(item)]), glo.SHOP_RARITY_EXPONENT))
    return glo.SHOP_BASE_PRICE + (pow(items.index(item), glo.SHOP_RARITY_EXPONENT))

def randomise():
    global current_items
    global items
    current_items = list()
    for item in items:
        if(len(current_items) == glo.SHOP_ITEM_COUNT):
            return
        elif(random.randint(0, 100) < 20):
            if item in custom_emoji_map.keys():
                current_items.append(custom_emoji_map[item])
            else:
                current_items.append(item)
    if(len(current_items) == 0):
        item = items[len(items) - 1]
        if item in custom_emoji_map.keys():
            current_items.append(item)
        else:
            current_items.append(item)

def purchase(uid, item, steal = False):
    global purchases
    if steal:
        successful = random.randint(0, getprice(item)) < (getprice(item) / 4)
        if successful:
            data = glo.USERDATA_READ(uid)
            data["inventory"].append(item)
            glo.USERDATA_WRITE(uid, data)
            return 0
        else:
            purchases = 0
            data = glo.USERDATA_READ(uid)
            data["currency"] = int(data["currency"] - (getprice(item) * 2))
            glo.USERDATA_WRITE(uid, data)
            randomise()
            return getprice(item) * 2
    else:
        if glo.USERDATA_READ(uid)["currency"] >= getprice(item):
            purchases += 1
            if purchases == glo.RANDOM_SHOP_THRESHOLD:
                purchases = 0
                randomise()
            data = glo.USERDATA_READ(uid)
            data["currency"] = int(data["currency"] - getprice(item))
            data["inventory"].append(item)
            glo.USERDATA_WRITE(uid, data)
            return True
        else:
            return False

class Bank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        randomise()

    @commands.command(aliases = ["bal"])
    async def balance(self, ctx):
        bal = glo.USERDATA_READ(ctx.author.id)["currency"]
        return await ctx.send(f"Your current balance is {bal} {glo.BANKFORMAT(bal)}.")

    @commands.command(aliases = ["sh"])
    async def shop(self, ctx):
        global current_items
        current_price = list()
        for item in current_items:
            current_price.append(str(getprice(item)))
        ebd = discord.Embed(title = "Shop", color = glo.COLOR) \
            .add_field(name = "Greetings!", value = "Welcome to shop, react with the item you want to purchase!", inline = False) \
            .add_field(name = "Item", value = '\n'.join(current_items), inline = True) \
            .add_field(name = "Price", value = '\n'.join(current_price), inline = True)
        msg: discord.Message = await ctx.send(embed = ebd)
        for r in current_items:
            if r in custom_emoji_map:
                await msg.add_reaction(f"{await ctx.guild.fetch_emoji(int(custom_emoji_map[r]))}")
            else:
                await msg.add_reaction(r)

    @commands.command()
    async def steal(self, ctx):
        global current_items
        global custom_emoji_map
        current_price = list()
        for item in current_items:
            current_price.append(str(getprice(item)))
        ebd = discord.Embed(title = "Steal from Shop", color = glo.COLOR) \
            .add_field(name = "Hey, psst!", value = "You can steal from the shop too, just don't get caught! React to the item you want to try to steal", inline = False) \
            .add_field(name = "Item", value = '\n'.join(current_items), inline = True)
        msg: discord.Message = await ctx.send(embed = ebd)
        for r in current_items:
            if r in custom_emoji_map:
                await msg.add_reaction(f"{r}:{custom_emoji_map[r]}")
            else:
                await msg.add_reaction(r)

    @commands.command()
    async def daily(self, ctx):
        userdata = glo.USERDATA_READ(ctx.author.id)
        if (time.time() - userdata["last_daily"]) < 86400: return await ctx.send("You've already claimed your daily today!")
        amount = random.randint(glo.DAILY_MIN, glo.DAILY_MAX)
        userdata["currency"] += amount
        userdata["last_daily"] = math.floor(time.time())
        await ctx.send(f"You've earned {amount} {glo.BANKFORMAT(amount)} today! Come back tomorrow for more.")
        glo.USERDATA_WRITE(ctx.author.id, userdata)
