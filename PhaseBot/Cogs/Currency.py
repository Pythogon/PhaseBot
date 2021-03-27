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
#    "TheaPixel",
    "⭐",
    "🌟",
    "🗡️",
    "👑",
    "🍪"#,
#    "bean"
]
global custom_emoji_map 
custom_emoji_map = {
    "bean": "710243429119950969"
}

global current_items
current_items = list()

def getprice(item):
#    if item in custom_emoji_map.values():
#        return glo.SHOP_BASE_PRICE + (pow(items.index(list(custom_emoji_map.keys())[list(custom_emoji_map.values()).index(str(item))]), glo.SHOP_RARITY_EXPONENT))
    return math.floor(glo.SHOP_BASE_PRICE + (pow(items.index(item), glo.SHOP_RARITY_EXPONENT)))

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
        item = items[len(items) - 1]
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

    @commands.command(aliases=["baltop", "bt"])
    async def balancetop(self, ctx):
        filtered = {}
        # Read all userdata
        read = glo.JSONREAD("userdata.json")
        to_send = "```Top balances\n\n"
        # Remove all 0 entries
        for k, v in read.items():
            if v["currency"] < 1:
                pass
            else: 
                # Store as {user_id: currency}
                filtered[k] = v["currency"]
        # Sort high to low
        filtered = {k: v for k, v in sorted(filtered.items(), key=lambda item: item[1], reverse = True)}
        # Generate full list for ordered values
        for key, value in filtered.items():
            name = glo.CURRENT_NAMES[int(key)]
            to_send += f"{name}: {value}\n"
        to_send += "```"
        # Send end
        await ctx.send(to_send)

    @commands.command()
    async def daily(self, ctx):
        userdata = glo.USERDATA_READ(ctx.author.id)
        if (time.time() - userdata["last_daily"]) < 86400: return await ctx.send("You've already claimed your daily today!")
        amount = random.randint(glo.DAILY_MIN, glo.DAILY_MAX)
        userdata["currency"] += amount
        userdata["last_daily"] = math.floor(time.time())
        await ctx.send(f"You've earned {amount} {glo.BANKFORMAT(amount)} today! Come back tomorrow for more.")
        glo.USERDATA_WRITE(ctx.author.id, userdata)

    @commands.command(aliases = ["randomise"])
    @commands.has_role(glo.DEVELOPER_ROLE_ID)
    async def randomize(self, ctx):
        randomise()
        await ctx.send("Randomised shop items!")

    @commands.command(aliases = ["sh"])
    async def shop(self, ctx):
        global current_items
        current_price = list()
        for item in current_items:
            current_price.append(str(getprice(item)))
        display = list()
        for item in current_items:
#            if item in custom_emoji_map.keys():
#                await ctx.send("item in emojimap")
#                custom_emoji = discord.utils.get(self.bot.emojis, id=int(custom_emoji_map[item]))
#                display.append(str(custom_emoji))
#            else:
            display.append(item)
        ebd = discord.Embed(title = "Shop", color = glo.COLOR) \
            .add_field(name = "Greetings!", value = "Welcome to shop, react with the item you want to purchase!", inline = False) \
            .add_field(name = "Item", value = '\n'.join(display), inline = True) \
            .add_field(name = "Price", value = '\n'.join(current_price), inline = True)
        msg: discord.Message = await ctx.send(embed = ebd)
        for r in current_items:
#            if r in custom_emoji_map.keys():
#                custom_emoji = discord.utils.get(self.bot.emojis, id=int(custom_emoji_map[item]))
#                await msg.add_reaction(custom_emoji)
#            else:
            await msg.add_reaction(r)

    @commands.command()
    async def steal(self, ctx):
        global current_items
        global custom_emoji_map
        current_price = list()
        for item in current_items:
            current_price.append(str(getprice(item)))
        display = list()
        for item in current_items:
#            if item in custom_emoji_map.keys():
#                custom_emoji = discord.utils.get(self.bot.emojis, id=int(custom_emoji_map[item]))
#                display.append(str(custom_emoji))
#            else:
            display.append(item)
        ebd = discord.Embed(title = "Steal from Shop", color = glo.COLOR) \
            .add_field(name = "Hey, psst!", value = "You can steal from the shop too, just don't get caught! React to the item you want to try to steal", inline = False) \
            .add_field(name = "Item", value = '\n'.join(display), inline = True)
        msg: discord.Message = await ctx.send(embed = ebd)
        for r in current_items:
#            if r in custom_emoji_map.keys():
#                custom_emoji = discord.utils.get(self.bot.emojis, id=int(custom_emoji_map[item]))
#                await msg.add_reaction(custom_emoji)
#            else:
            await msg.add_reaction(r)

    @commands.command(aliases = ["inv"])
    async def inventory(self, ctx):
        raw_inv = glo.USERDATA_READ(ctx.author.id)["inventory"]
        inv = list()
        for i in raw_inv:
            # custom item check
            inv.append(i)

        inv_str = '\n'.join(inv)
        if len(inv_str) == 0:
            inv_str = 'Nothing here!'

        ebd = discord.Embed(title = "Inventory", color = glo.COLOR) \
            .add_field(name = "Normal Items", value = inv_str, inline = True) \
            .add_field(name = "Special Items", value = 'Nothing here!', inline = True)

        await ctx.send(embed = ebd)