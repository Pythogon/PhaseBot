import discord
import humanize
import glo
import shlex
import subprocess
import re

from datetime import datetime

from discord.ext import commands
from discord.ext import tasks

class Instagram(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None
		self.reload.start()
		self.check_new_posts.start()

	def cog_unload(self):
		self.reload.cancel()
		self.check_new_posts.cancel()

	@tasks.loop(minutes = 30)
	async def reload(self):
		subprocess.Popen(shlex.split(f"instagram-scraper sole_nyu -m 1 --comments --media-types=none -u angy_garnedd -p {glo.GLOBAL_READ('igpass')} -d ./local_Store --cookiejar=./local_Store/instagram_cookies"))
		glo.GLOBAL_WRITE('lastreload', round(datetime.now().timestamp()))

	@tasks.loop(minutes = 30)
	async def check_new_posts(self):
		await self.bot.wait_until_ready()
		print("Checking new posts...")
		c = self.bot.get_channel(709719731472564224)
		if c is not None:
			graphimage = glo.GETGRAPHIMAGE()
			shortcode = graphimage["shortcode"]
			if shortcode != glo.GLOBAL_READ("lastshortcode"): 
				glo.GLOBAL_WRITE("lastshortcode", shortcode)
				await c.send(f"A new episode of LIFE has been released!\n{graphimage['edge_media_to_caption']['edges'][0]['node']['text']}\nhttps://instagram.com/p/{shortcode}/")
				print("New post found!")

	@commands.command()
	async def votes(self, ctx, number: int):
		options = {k: [] for i in range(number) for k in chr(65+i)}
		used_users = []

		for comment in glo.GETGRAPHIMAGE()["comments"]["data"]:
			user_id = comment["owner"]["id"]
			if user_id in used_users: continue
			text = comment["text"].upper()
			vote = text[0]
			if vote not in options.keys(): continue
			if text != vote and re.match(r"[a-zA-Z]", text[1]) is not None and text[1] != text[0]: continue
			options[vote].append(user_id)
			used_users.append(user_id)
		
		vote_count = len([x for slist in list(options.values()) for x in slist])
		field = ""
		for option in options.keys(): 
			votes = len(options[option])
			field += f"{option}: {votes} ({round((votes/vote_count)*100, 2)}%)\n"
		field += f"**Total votes: {vote_count}**"
		eb = discord.Embed(title = "Current votes", color = glo.COLOR) \
		.add_field(name = f"(last reloaded {humanize.naturaltime(datetime.now() - datetime.fromtimestamp(glo.GLOBAL_READ('lastreload')))})", value = field) \
		.set_footer(text = glo.FOOTER())
		await ctx.send(embed = eb)

