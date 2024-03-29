import ast
import discord
import operator
import random

import glo #type: ignore
from datetime import date
from datetime import datetime
from datetime import timedelta
from discord.ext import commands

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

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot # Initception
        self._last_member = None

    @commands.command(aliases = ["an"])
    @commands.is_owner()
    async def announce(self, ctx, *message):
        # Channel fetching
        main_channel = ctx.guild.get_channel(glo.MAIN_CHANNEL_ID)
        announcement_channel = ctx.guild.get_channel(glo.ANNOUNCEMENT_CHANNEL_ID)
        # Join message
        message = " ".join(message)
        # Construct embed
        embed = discord.Embed(title = f"An important update about PhaseBot.", color = glo.COLOR
        ).add_field(name = "Announcement:", value = message
        ).set_footer(text = glo.FOOTER())
        # Send to main_channel and announcement_channel
        await main_channel.send(embed = embed)
        await announcement_channel.send(embed = embed)

    @commands.command(aliases = ["id"])
    @commands.has_role(glo.DEVELOPER_ROLE_ID)
    async def checkid(self, ctx, unkID: int, channelID = 1):
        try: # Simple type checker with deductive reasoning
            print("0a")
            h = self.bot.get_channel(unkID)
            if h == None: raise TypeError
            print("0b")
            case = 0
        except:
            try:
                print("1a")
                h = self.bot.get_user(unkID)
                if h == None: raise TypeError
                print("1b")
                case = 1
            except:
                try:
                    print("2a")
                    h = self.bot.get_emoji(unkID)
                    if h == None: raise TypeError
                    print("2b")
                    case = 2
                except:
                    try:
                        print("3a")
                        c = self.bot.get_channel(channelID.id)
                        h = await c.fetch_message(unkID)
                        if h == None: raise TypeError
                        print("3b")
                        case = 3
                    except:
                        try:
                            print("4a")
                            g = self.bot.get_guild(glo.GUILD_ID)
                            h = g.get_role(unkID)
                            if h == None: raise TypeError
                            print("4b")
                            case = 4
                        except:
                            print("5")
                            case = 5
        to_send = {0: "channel", 1: "user", 2: "emoji", 3: "message", 4: "role", 5: "unknown"}.get(case)
        embed = discord.Embed(title = "Searching for ID...", color = glo.COLOR) \
        .add_field(name = f"Detected ID type: {to_send}.", value = "If this seems incorrect, check again! If it's suspected to be a message, ensure to add the channel.") \
        .set_footer(text = glo.FOOTER())
        await ctx.send(embed = embed)

    @commands.group()
    @commands.has_role(glo.DEVELOPER_ROLE_ID)
    async def call(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Correct usage is )call <add|list|remove>")

    @call.command(name = "add")
    @commands.has_role(glo.DEVELOPER_ROLE_ID)
    async def call_add(self, ctx, call, response):
        calls = glo.GLOBAL_READ("calls")
        calls[call] = response
        glo.GLOBAL_WRITE("calls", calls)
        await ctx.send("Call successfully added.")
    
    @call.command(name = "list")
    @commands.has_role(glo.DEVELOPER_ROLE_ID)
    async def call_list(self, ctx):
        calls = glo.GLOBAL_READ("calls")
        out = "__List of calls__ \n\n"
        for call in calls:
            out += f"{call}: {calls[call]} \n"
        await ctx.send(out)

    @call.command(name = "remove")
    @commands.has_role(glo.DEVELOPER_ROLE_ID)
    async def call_remove(self, ctx, call):
        calls = glo.GLOBAL_READ("calls")
        calls.pop(call)
        glo.GLOBAL_WRITE("calls", calls)
        await ctx.send("Call removed.")

    @commands.command(aliases = ["dh"])
    @commands.has_role(glo.DEVELOPER_ROLE_ID)
    async def devhelp(self, ctx):
        # Embed contructor
        embed = discord.Embed(title = "Developer help panel", color = glo.COLOR
        ).add_field(name = "Developer only commands", value = """checkid|id
devhelp|dh
embed|eb "TITLE" "NAME,VALUE;NAME,VALUE" "FOOTER"
listall|la <channels|c, members|m, roles|r>
lockdown
metrics|met <guild|g, user|u>
schedule|ss <add|a, purge|p, remove|r>
pay <payee> <amount> -s""", inline = False) \
.add_field(name = "Bot admin only commands", value = """evaluate|eval <to eval>
forcestar|fs <channel> <message ID>
modify <user> <aspect> <value>""") \
        .set_footer(text = glo.FOOTER())
        await ctx.send(embed = embed)

    @commands.command(aliases = ["eb"]) # Credit to Th3T3chn0G1t
    @commands.has_role(glo.DEVELOPER_ROLE_ID)
    async def embed(self, ctx, title, data, footer=glo.FOOTER()):
        embed = discord.Embed(title = title, color = glo.COLOR)
        embed_data = data.split(';') # Split into embed entries
        for s in embed_data:
            field = s.split(',') # Split into embed componants
            embed.add_field(name = field[0], value = field[1], inline = False)
        embed.set_footer(text = footer)
        await ctx.send(embed = embed)

    @commands.command(aliases = ["eval", "return"])
    @commands.is_owner()
    async def evaluate(self, ctx, *, cmd):
        fn_name = "_eval_expr"
        cmd = cmd.strip("` ")
        # add a layer of indentation
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
        # wrap in async def body
        body = f"async def {fn_name}():\n{cmd}"
        parsed = ast.parse(body)
        body = parsed.body[0].body
        insert_returns(body)
        env = {'bot': self.bot, 'discord': discord, 'commands': commands, 'ctx': ctx, '__import__': __import__, "date": date, "timedelta": timedelta, "glo": glo}
        exec(compile(parsed, filename="<ast>", mode="exec"), env)
        result = (await eval(f"{fn_name}()", env))
        await ctx.send(result)

    @commands.group(aliases = ["la"])
    @commands.has_role(glo.DEVELOPER_ROLE_ID)
    async def listall(self, ctx):
        if ctx.invoked_subcommand == None:
            await ctx.send(f"Correct usage is {glo.PREFIX}list all <channels|members|roles>.") # Default case

    @listall.command(name = "channels", aliases = ["c"])
    async def listall_channels(self, ctx):
        channel_list = ""
        for channel in ctx.guild.channels:
            # Skipping all CategoryChannels
            if isinstance(channel, discord.CategoryChannel): continue 
            channel_list += f"{channel.name}\n"
        await ctx.send(channel_list)

    @listall.command(name = "members", aliases = ["m"])
    async def listall_members(self, ctx):
        member_list = ""
        for member in ctx.guild.members: member_list += f"{member.name}\n"
        await ctx.send(member_list)

    @listall.command(name = "roles", aliases = ["r"])
    async def listall_roles(self, ctx):
        role_list = ""
        for role in ctx.guild.roles: role_list += f"{role.name}\n"
        await ctx.send(role_list)

    @commands.command()
    @commands.has_role(glo.DEVELOPER_ROLE_ID)
    async def lockdown(self, ctx):
        ld_state = glo.GLOBAL_READ("lockdown")
        if ld_state == "1":
            glo.GLOBAL_WRITE("lockdown", "0")
            return await ctx.send("Lockdown disabled. Welcome back!")
        glo.GLOBAL_WRITE("lockdown", "1")
        return await ctx.send("Lockdown enabled. Stay safe.")

    @commands.group(aliases = ["met"])
    async def metrics(self, ctx):
        if ctx.invoked_subcommand == None:
            await ctx.send(f"Correct usage is {glo.PREFIX}metrics <guild|user>.") # Default case

    @metrics.command(name = "guild", aliases = ["g"])
    async def metrics_guild(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title = "Metrics for this guild", color = glo.COLOR) \
        .add_field(name = "User count", value = str(len(guild.members))) \
        .add_field(name = "Created at", value = guild.created_at.strftime(glo.DATE_FORMAT_HOUR_INCLUSIVE)) \
        .add_field(name = "Channel count", value = str(len(guild.channels))) \
        .add_field(name = "Role count", value = str(len(guild.roles))) \
        .add_field(name = "Server owner", value = guild.owner.name) \
        .set_footer(text = glo.FOOTER())
        await ctx.send(embed = embed)

    @metrics.command(name = "user", aliases = ["u"])
    async def metrics_user(self, ctx, member: discord.Member):
        userdata = glo.USERDATA_READ(member.id)
        if userdata["rate"] == None:
            rate = "Unknown"
        else: 
            rate = userdata["rate"]
        if userdata["role"] == None:
            role = "None"
        else:
            role = userdata["role"]
        
        embed = discord.Embed(title = "Metrics for that user", color = glo.COLOR) \
        .add_field(name = "Username", value = member.name) \
        .add_field(name = "User ID", value = str(member.id)) \
        .add_field(name = "Account created at", value = member.created_at.strftime(glo.DATE_FORMAT_HOUR_INCLUSIVE)) \
        .add_field(name = "Joined guild at", value = member.joined_at.strftime(glo.DATE_FORMAT_HOUR_INCLUSIVE)) \
        .add_field(name = "Surreal rating", value = rate) \
        .add_field(name = "Role ID", value = role) \
        .add_field(name = "Last )superstar", value = userdata["laststar"]) \
        .add_field(name = "Starcount", value = userdata["starcount"]) \
        .add_field(name = "Balance", value = userdata["currency"]) \
        .add_field(name = "Inventory", value = str(userdata["inventory"])) \
        .set_footer(text = glo.FOOTER())
        await ctx.send(embed = embed)

    @commands.command(aliases = ["mod"])
    @commands.is_owner()
    async def modify(self, ctx, user: discord.User, aspect, value: int):
        # Error check to deal with typos (which happen too often)
        if aspect not in glo.USERDATA_READ("default"):
            return await ctx.send(f"Aspect {aspect} not found.")
        # Do a RW
        userdata = glo.USERDATA_READ(user.id)
        userdata[aspect] = value
        glo.USERDATA_WRITE(user.id, userdata)
        await ctx.send(f"Aspect {aspect} is now {value}.")
    
    @commands.command(aliases = ["eg"])
    @commands.has_role(glo.DEVELOPER_ROLE_ID)
    async def endgiveaway(self, ctx, channel: discord.TextChannel, message_id: int, fee: int, winner_count: int):
        entries = []
        message = await channel.fetch_message(message_id)
        for reaction in message.reactions:
            async for user in reaction.users():
                ud = glo.USERDATA_READ(user.id)
                ud["currency"] -= fee
                tax = int(glo.GLOBAL_READ("tax"))
                tax += fee
                glo.USERDATA_WRITE(user.id, ud)
                glo.GLOBAL_WRITE("tax", tax)
                entries.append(user.id)
        to_send = "__The winners of the giveaway__\n"
        for x in range(winner_count):
            if entries == []: continue
            winner = random.choice(entries)
            entries.remove(winner)
            to_send += f"<@{winner}>\n"
        await channel.send(to_send)
        
