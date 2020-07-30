import discord
import glo

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
    async def announce(ctx, *message):
        gdpr_list = jsonRead("gdpr.json")
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
    async def checkid(ctx, unkID: int, channelID = 1):
        gdpr_list = jsonRead("gdpr.json")
        try:
            if gdpr_list[str(ctx.author.id)] != 1: raise ValueError
        except:
            return await ctx.send(embed = glo.GDPR())
        try:
            print("0a")
            h = bot.get_channel(unkID)
            if h == None: raise
            print("0b")
            case = 0
        except:
            try:
                print("1a")
                h = bot.get_user(unkID)
                if h == None: raise
                print("1b")
                case = 1
            except:
                try:
                    print("2a")
                    h = bot.get_emoji(unkID)
                    if h == None: raise
                    print("2b")
                    case = 2
                except:
                    try:
                        print("3a")
                        c = bot.get_channel(channelID.id)
                        h = await c.fetch_message(unkID)
                        if h == None: raise
                        print("3b")
                        case = 3
                    except:
                        try:
                            print("4a")
                            g = bot.get_guild(709717828365844511)
                            h = g.get_role(unkID)
                            if h == None: raise
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

    @commands.command(aliases = ["eval"])
    @commands.is_owner()
    async def eval_fn(ctx, *, cmd):
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
