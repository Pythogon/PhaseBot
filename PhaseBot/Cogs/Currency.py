import asyncio
import discord
import glo #type: ignore
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
            tax = int(glo.GLOBAL_READ("tax"))
            tax -= getprice(item)
            glo.GLOBAL_WRITE("tax", tax)
            return 0
        else:
            purchases = 0
            data = glo.USERDATA_READ(uid)
            fine = int((getprice(item) * 2))
            data["currency"] -= fine
            glo.USERDATA_WRITE(uid, data)
            tax = int(glo.GLOBAL_READ("tax"))
            tax += fine
            glo.GLOBAL_WRITE("tax", tax)
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
        return await ctx.send(f"Your current balance is {glo.BANKFORMAT(bal)}.")

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
            try:
                name = glo.CURRENT_NAMES[int(key)]
            except KeyError:
                u = self.bot.get_user(int(key))
                if u is None:
                    glo.SETNAME(int(key), "Member left")
                else:
                    glo.SETNAME(int(key), u.name)
                name = glo.CURRENT_NAMES[int(key)]
            to_send += f"{name}: {value}\n"
        to_send += "```"
        # Send end
        await ctx.send(to_send)

    @commands.command()
    async def daily(self, ctx):
        userdata = glo.USERDATA_READ(ctx.author.id)
        diff = time.time() - userdata["last_daily"]
        if diff < 86400: 
            time_left = time.strftime("%Hh %Mm %Ss", time.gmtime(86400 - diff))
            return await ctx.send(f"You've already claimed your daily today, it will be available in {time_left}.")
        amount = random.randint(glo.DAILY_MIN, glo.DAILY_MAX)
        tax = glo.CALCULATE_TAX(amount, userdata["currency"])
        userdata["currency"] += tax[0]
        userdata["last_daily"] = math.floor(time.time())
        await ctx.send(f"Amount earned: {glo.BANKFORMAT(amount)}\nTax at {tax[2]}%: {glo.BANKFORMAT(tax[1])}\nAmount recieved: {glo.BANKFORMAT(tax[0])}.\nCome back tomorrow for more!")
        glo.USERDATA_WRITE(ctx.author.id, userdata)
        tax_amount = int(glo.GLOBAL_READ("tax"))
        tax_amount = str(tax_amount + tax[1])
        glo.GLOBAL_WRITE("tax", tax_amount)

    @commands.command()
    async def pay(self, ctx, payee: discord.Member, amount: int, *system):
        if amount < 0:
            return await ctx.send("You can't send negative money!")
        payee_data = glo.USERDATA_READ(payee.id)
        payer_data = glo.USERDATA_READ(ctx.author.id)
        if system != tuple():
            if "-s" in system:
                role = ctx.guild.get_role(glo.DEVELOPER_ROLE_ID)
                if not (role in ctx.author.roles):
                    return await ctx.send("You don't have system permissions.")
                if "-t" in system:
                    tax = glo.CALCULATE_TAX(amount, payee_data["currency"])
                    payee_data["currency"] += tax[0]
                    glo.USERDATA_WRITE(payee.id, payee_data)
                    tax_amount = int(glo.GLOBAL_READ("tax"))
                    tax_amount = tax_amount + tax[1]
                    glo.GLOBAL_WRITE("tax", tax_amount)
                    return await ctx.send(f"Payment successful!\nAmount: {glo.BANKFORMAT(amount)}\nTax at {tax[2]}%: {glo.BANKFORMAT(tax[1])}\nAmount recieved: {glo.BANKFORMAT(tax[0])}")
                payee_data["currency"] += amount
                glo.USERDATA_WRITE(payee.id, payee_data)
                return await ctx.send(f"Gave {payee.name} {glo.BANKFORMAT(amount)} with system permissions.")
            return await ctx.send("That wasn't a correct argument.")
        if payer_data["currency"] < amount:
            return await ctx.send("You don't have enough money to do that!")
        if payee_data == payer_data:
            return await ctx.send("You can't pay yourself!")
        payer_data["currency"] -= amount
        tax = glo.CALCULATE_TAX(amount, payee_data["currency"])
        payee_data["currency"] += tax[0]
        glo.USERDATA_WRITE(ctx.author.id, payer_data)
        glo.USERDATA_WRITE(payee.id, payee_data)
        embed = discord.Embed(title = "Payment successful!", color = glo.COLOR) \
        .add_field(name = "Amount paid", value = amount, inline = False) \
        .add_field(name = f"Tax paid (charged at {tax[2]}%)", value = tax[1], inline = False) \
        .add_field(name = f"{ctx.author.name}'s new balance", value = payer_data["currency"], inline = False) \
        .add_field(name = f"{payee.name}'s new balance", value = payee_data["currency"]) \
        .set_footer(text = glo.FOOTER())
        await ctx.send(embed = embed)
        tax_amount = int(glo.GLOBAL_READ("tax"))
        tax_amount = str(tax_amount + tax[1])
        glo.GLOBAL_WRITE("tax", tax_amount)


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
            """            
            if item in custom_emoji_map.keys():
                await ctx.send("item in emojimap")
                custom_emoji = discord.utils.get(self.bot.emojis, id=int(custom_emoji_map[item]))
                display.append(str(custom_emoji))
            else:
            """
            display.append(item)
        ebd = discord.Embed(title = "Shop", color = glo.COLOR) \
            .add_field(name = "Greetings!", value = "Welcome to shop, react with the item you want to purchase!", inline = False) \
            .add_field(name = "Item", value = '\n'.join(display), inline = True) \
            .add_field(name = "Price", value = '\n'.join(current_price), inline = True)
        msg: discord.Message = await ctx.send(embed = ebd)
        for r in current_items:
            """
            if r in custom_emoji_map.keys():
                custom_emoji = discord.utils.get(self.bot.emojis, id=int(custom_emoji_map[item]))
                await msg.add_reaction(custom_emoji)
            else:
            """    
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
            """
            if item in custom_emoji_map.keys():
                custom_emoji = discord.utils.get(self.bot.emojis, id=int(custom_emoji_map[item]))
                display.append(str(custom_emoji))
            else:
            """
            display.append(item)
        ebd = discord.Embed(title = "Steal from Shop", color = glo.COLOR) \
            .add_field(name = "Hey, psst!", value = "You can steal from the shop too, just don't get caught! React to the item you want to try to steal", inline = False) \
            .add_field(name = "Item", value = '\n'.join(display), inline = True)
        msg: discord.Message = await ctx.send(embed = ebd)
        for r in current_items:
            """
            if r in custom_emoji_map.keys():
                custom_emoji = discord.utils.get(self.bot.emojis, id=int(custom_emoji_map[item]))
                await msg.add_reaction(custom_emoji)
            else:
            """
            await msg.add_reaction(r)

    @commands.command(aliases = ["inv"])
    async def inventory(self, ctx):
        raw_inv = glo.USERDATA_READ(ctx.author.id)["inventory"]
        inv = list()
        for i in raw_inv:
            # custom item 
            inv.append(i)

        inv_str = '\n'.join(inv)
        if len(inv_str) == 0:
            inv_str = 'Nothing here!'

        ebd = discord.Embed(title = "Inventory", color = glo.COLOR) \
            .add_field(name = "Normal Items", value = inv_str, inline = True) \
            .add_field(name = "Special Items", value = 'Nothing here!', inline = True)

        await ctx.send(embed = ebd)

    @commands.command()
    async def taxbrackets(self, ctx):
        brackets = list(glo.TAX_BRACKETS.items())
        brackets[0] = (0, 100)
        to_send = "**Current tax brackets**\n\n"
        for t in brackets:
            max = t[0]
            amount = 100 - t[1]
            if max == 0: continue
            index = brackets.index(t)
            min = brackets[index - 1][0] + 1
            try:
                brackets[index + 1]
            except:
                to_send += f"{glo.BANKFORMAT(min)}+: {amount}%\n"
                continue
            to_send += f"{min}-{glo.BANKFORMAT(max)}: {amount}%\n"
        await ctx.send(to_send)
    
    @commands.command(aliases = ["tax"])
    async def taxpot(self, ctx):
        tax = glo.GLOBAL_READ("tax")
        await ctx.send(f"{glo.BANKFORMAT(tax)} is the amount currently in the tax pot.")
    
    @commands.command(aliases = ["contr"])
    async def contribute(self, ctx, amount: int):
        if amount < 0: return await ctx.send("You can't contribute less than nothing!")
        userdata = glo.USERDATA_READ(ctx.author.id)
        if userdata["currency"] < amount: return await ctx.send("You don't have enough money for this contribution.")
        tax = int(glo.GLOBAL_READ("tax"))
        tax_bracket = glo.CALCULATE_TAX(amount, userdata["currency"])
        tax += (amount + tax_bracket[1])
        userdata["currency"] -= amount
        glo.GLOBAL_WRITE("tax", tax)
        glo.USERDATA_WRITE(ctx.author.id, userdata)
        await ctx.send(f"You paid {glo.BANKFORMAT(amount)} as a voluntary contribution! Given your tax bracket, {glo.BANKFORMAT(tax_bracket[1])} has been added to the tax pot in addition to your donation.")