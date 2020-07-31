import ast
import discord
import glo
import operator

from datetime import date
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
        self.bot = bot
        self._last_member = None

    @commands.command(aliases = ["an"])
    @commands.is_owner()
    async def announce(self, ctx, *message):
        gdpr_list = glo.JSONREAD("gdpr.json")
        try:
            if gdpr_list[str(ctx.author.id)] != 1: raise ValueError
        except:
            return await ctx.send(embed = glo.GDPR())
        message = " ".join(message)
        embed = discord.Embed(title = "An important update about PhaseBot.", color = glo.COLOR
        ).add_field(name = "Announcement:", value = message
        ).set_footer(text = glo.FOOTER())
        await ctx.send(embed = embed)

    @commands.command(aliases = ["id"])
    @commands.has_role(glo.DEVELOPER_ROLE_ID)
    async def checkid(self, ctx, unkID: int, channelID = 1):
        gdpr_list = glo.JSONREAD("gdpr.json")
        try:
            if gdpr_list[str(ctx.author.id)] != 1: raise ValueError
        except:
            return await ctx.send(embed = glo.GDPR())
        
        try:
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
        embed = discord.Embed(title = "Searching for ID...", color = glo.COLOR
        ).add_field(name = f"Detected ID type: {to_send}.", value = "If this seems incorrect, check again! If it's suspected to be a message, ensure to add the channel."
        ).set_footer(text = glo.FOOTER())
        await ctx.send(embed = embed)
    
    @commands.command(aliases = ["dh"])
    @commands.has_role(glo.DEVELOPER_ROLE_ID)
    async def devhelp(self, ctx):
        embed = discord.Embed(title = "Developer help panel.", color = glo.COLOR
        ).add_field(name = "Developer only commands.", value = """checkid|id
        devhelp|dh
        leaderboard|ld""", inline = False
        ).add_field(name = "Bot admin only commands.", value = """evaluate|eval <to eval>
        forcestar|fs <channel> <message ID>"""
        ).set_footer(text = glo.FOOTER())
        await ctx.send(embed = embed)

    @commands.command(aliases = ["eval"])
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

    @commands.command(aliases=["ld"])
    @commands.has_role(glo.DEVELOPER_ROLE_ID)
    async def leaderboard(self, ctx):
        gdpr_list = glo.JSONREAD("gdpr.json")
        try:
            if gdpr_list[str(ctx.author.id)] != 1:
                raise ValueError
        except:
            return await ctx.send(embed=glo.GDPR())
        read = dict(sorted(glo.JSONREAD("starcount.json").items(),key=operator.itemgetter(1), reverse=True))
        to_send = ""
        for key, value in read.items():
            name = await self.bot.fetch_user(int(key))
            to_send += f"{name.name}: {value}\n"
        embed = discord.Embed(title="Starboard Leaderboard", color=glo.COLOR
        ).add_field(name="Scores:", value=to_send
        ).set_footer(text=glo.FOOTER())
        await ctx.send(embed=embed)
