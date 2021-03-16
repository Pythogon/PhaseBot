import asyncio
import discord
from discord.ext.commands import Context
import glo #pylint: disable=import-error
import random

from discord.ext import commands

bankdb = "local_Store/bank.txt"

class Currency(commands.Cog):
    account: list = []
    data: list = []

    def readfsdb(self):
        with open(bankdb, 'r') as bankdb_r:
            lines = bankdb_r.readlines()
            for i in range(0, len(lines)):
                lnloc = lines[i].split(':')
                self.account.append(int(lnloc[0]))
                self.data.append(int(lnloc[1]))

    def syncfsdb(self):
        with open(bankdb, 'w') as bankdb_w:
            lines: list = []
            for i in range(0, len(self.account)):
                lines.append(str(self.account[i]) + ':' + str(self.data[i]))
                bankdb_w.writelines(lines)
        
    def getaccountidx(self, id):
        if id in self.account:
            return self.account.index(id)
        else:
            return -1

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.readfsdb()

    @commands.command(aliases = ["bal"])
    async def balance(self, ctx: Context):
        try:
            await ctx.send(self.data[self.getaccountidx(ctx.author.id)])
        except IndexError:
            await ctx.send("You don't have an account yet!")

    @commands.command(aliases = ["setbal"])
    async def setbalance(self, ctx: Context, value):
        try:
            self.data[self.getaccountidx(ctx.author.id)] = int(value)
            await ctx.send("Your balance has been updated")
            self.syncfsdb()        
        except IndexError:
            await ctx.send("You don't have an account yet!")
