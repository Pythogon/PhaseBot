import shlex
import discord
import glo
import subprocess
import instagram_scraper
from discord.ext import commands

class Voting(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None

	@commands.command()
	async def reload(self, ctx):
		subprocess.Popen(shlex.split(f"instagram-scraper sole_nyu -m 1 --comments --media-types=none -u life_vote_counter -p{glo.GLOBAL_READ('igpass')} -d ./local_Store"))
		await ctx.send("Updating the comments data now! Wait about 30 seconds before running )votes.")

	@commands.command()
	async def votes(self, ctx, number: int):
		options = {k: [] for i in range(number) for k in chr(65+i)}
		used_users = []

		for comment in glo.JSONREAD("sole_nyu.json")["GraphImages"][0]["comments"]["data"]:
			user_id = comment["owner"]["id"]
			if user_id in used_users: continue
			text = comment["text"].upper()
			vote = text[0]
			if vote not in options.keys(): continue
			if text != vote and not text.startswith(f"{vote} "): continue
			options[vote].append(user_id)
			used_users.append(user_id)
		
		vote_count = len([x for slist in list(options.values()) for x in slist])
		to_send = f"__Current vote totals__\n"
		for option in options.keys(): 
			votes = len(options[option])
			to_send += f"{option}: {votes} ({round((votes/vote_count)*100, 2)}%)\n"
		
		await ctx.send(to_send)

