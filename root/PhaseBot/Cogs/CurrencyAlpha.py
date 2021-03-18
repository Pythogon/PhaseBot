import asyncio
import discord
import glo #pylint: disable=import-error
import random

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
    "👑"
]
global current_items
current_items = list()

def getprice(item):
    return glo.SHOP_BASE_PRICE + (pow(items.index(item), glo.SHOP_RARITY_EXPONENT))

def randomise():
    global current_items
    global items
    current_items = list()
    for item in items:
        if(len(current_items) == glo.SHOP_ITEM_COUNT):
            return
        elif(random.randint(0, 100) < 20):
            current_items.append(item)
    if(len(current_items) == 0):
        current_items.append(items[len(items) - 1])

def purchase(uid, item):
    global purchases
    if int(glo.USERDATA_READ(uid)["currency"]) >= getprice(item):
        purchases += 1
        if purchases == glo.RANDOM_SHOP_THRESHOLD:
            purchases = 0
            randomise()
        data = glo.USERDATA_READ(uid)
        data["currency"] = str(int(data["currency"]) - getprice(item))
        glo.USERDATA_WRITE(uid, data)
        return True
    else:
        return False

class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        randomise()

    @commands.command(aliases = ["bal"])
    async def balance(self, ctx):
        bal = glo.USERDATA_READ(ctx.author.id)["currency"]
        return await ctx.send(f"Your current balance is {bal}.")

    @commands.command(aliases = ["setbal"])
    async def setbalance(self, ctx, value):
        data = glo.USERDATA_READ(ctx.author.id)
        data["currency"] = str(value)
        glo.USERDATA_WRITE(ctx.author.id, data)

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
            await msg.add_reaction(r)
