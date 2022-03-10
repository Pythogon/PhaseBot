import discord
import glo
import os
import instascrape
from discord.ext import commands

class Voting(commands.Cog):
	async def __init__(self, bot):
		self.bot = bot
		self._last_member = None

	@commands.command()
	async def votes(self, ctx, number: int):
		options = {k:[] for i in range(number) for k in chr(i+65)}
		used_users = []
		post = instascrape.Profile("https://www.instagram.com/sole_nyu/").get_recent_posts(1)
		comments = post.get_recent_comments()

		for comment in comments:
			if comment.username in used_users: continue
			vote = comment.text[0].upper()
			if vote not in options.keys(): continue
			options[vote].append(comment.username)
			used_users.append(comment.username)

		vote_count = len([x for slist in list(options.values()) for x in slist])
		to_send = f"__Current vote totals__\n"
		for option in options.keys(): 
			to_send += f"{option}: {options[option]} ({round((len(option)/vote_count)*100, 2)}%)\n"
		
		await ctx.send(to_send)

