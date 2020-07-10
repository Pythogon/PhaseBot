import discord
import glo

async def getLogs(v):
    valid_embed = discord.Embed(title = f"Changelogs for v{v}:", color = glo.COLOR)
    if v == "1.1":
        valid_embed.add_field(name = "Additions:", value = f"""{glo.PREFIX}stargen command.
{glo.PREFIX}comments command.
{glo.PREFIX}votesraw command.
Automatic #starcastle saver along with automatic progress updates on {glo.PREFIX}stargen.
{glo.PREFIX}announce command for bot developers.""", inline = False)
        valid_embed.add_field(name = "Modifications:", value = f"""Added more random footers.
Changed the logic behind {glo.PREFIX}votes' counting system (hopefully removing false positives).
Optimised {glo.PREFIX}votes' code to make it easier to read.
Siginificant changes to the global variable definitions.
COLOR is now a global variable.
Anti-duplicate vote counting in {glo.PREFIX}votes.""")
    elif v == "1.0.4":
        valid_embed.add_field(name = "Additions:", value = f"""Bot now automatically polls Instagram upon startup.
{glo.PREFIX}name command.""", inline = False)
        valid_embed.add_field(name = "Modifications:", value = f"""Started work on a new feature (it will not release for several months).
Minor appearance changes to {glo.PREFIX}votes.
Removed the startup message to prevent channel clogging.""", inline = False)
        valid_embed.add_field(name = "Bug fixes:", value = "Fixed a bug where v1.0.3's changelog didn't load correctly.", inline = False)
    elif v == "1.0.3":
        valid_embed.add_field(name = "Modifications:", value = f"""Changed {glo.PREFIX}votes' embed title to seem more Phaser-y.
Added PhaseBot to [GitHub](https://github.com/Pythogon/Phasebot)!
Edited {glo.PREFIX}info to include more up-to-date information.""", inline = False)
    elif v == "1.0.2":
        valid_embed.add_field(name = "Additions:", value = f"""{glo.PREFIX}reload command (thanks to my InstaScrape meta-grabber).
{glo.PREFIX}votes command.""", inline = False)
        valid_embed.add_field(name = "Modifications:", value = f"""Edited embeds to be easier to read on mobile devices.
Added more information to {glo.PREFIX}info command.
Added 2 new random footers, including one thanking SoleNyu for their work on LIFE.""", inline = False)
        valid_embed.add_field(name = "Bug fixes:", value = f"""Fixed a bug where {glo.PREFIX}help did not correctly load.
Fixed a bug whereby PhaseBot checking an existing users' rating, the command would error without a message.
Fixed a spelling mistake in v0.1.2's changelog.""", inline = False)
    elif v == "1.0.1":
        valid_embed.add_field(name = "Modifications:", value = """Changed the name formatting of all variables.
Changed glo.STAR_COUNT to 3 (was 2, was starcount).
Changed glo.PREFIX to ) (was ^, was p).""")
    elif v == "1.0":
        valid_embed.add_field(name = "Additions:", value = f"""{glo.PREFIX}generate command.
Global variables file.""", inline = False)
        valid_embed.add_field(name = "Modifications:", value = f"""Changed how {glo.PREFIX}logs fetches log data to decrease the size of the main bot file.
Interfaced PhaseBot backend with [CommentGenRNN](https://github.com/Pythogon/CommentGenRNN).
Renamed the core bot file to "bot.py" to follow the standard bot procedure.
Considerable code remodelling to make it easier to add to in the future.""", inline = False)
        valid_embed.add_field(name = "Bug fixes:", value = f"Fixed a bug with {glo.PREFIX}logs where the footer didn't load correctly.")
    elif v == "0.1.3":
        valid_embed.add_field(name = "Additions:", value = f"{glo.PREFIX}logs command.\n{glo.PREFIX}info command.")
        valid_embed.add_field(name = "Modifications:", value = """The footer of embeds now randomly changes.
Changed credit on footers from Ashie to [PyTec](https://github.com/Pythogon).""", inline = False)
    elif v == "0.1.2":
        valid_embed.add_field(name = "Additions:", value = f"{glo.PREFIX}poll command.")
        valid_embed.add_field(name = "Modifications", value = f"""Changed the amount of stars needed to be added to the starboard to 2 (was 4).
Updated the {glo.PREFIX}starinfo command to be easier to read on mobile.
Changed the way footers are processed in the code, allowing easier changes to them in the future.""", inline = False)
    elif v == "0.1.1":
        valid_embed.add_field(name = "Additions:", value = f"""{glo.PREFIX}rate command.
{glo.PREFIX}avatar command.
Permanent storage of user IDs for key bot-related metadata (eg. a user's {glo.PREFIX}rate score.""", inline = False)
        valid_embed.add_field(name = "Modifications:", value = """Imported large amounts of [PyTec](https://github.com/Pythogon) backend code which will help in importing Anabot features.
Swapped all read-write operations of files out with more efficient versions.
Repurposed ~100 lines of old code to be used for PhaseBot.
Modified how reaction_add gets logged to make checking for bugs and issues easier.""", inline = False)
    elif v == "0.1":
        valid_embed.add_field(name = "Additions:", value = f"""{glo.PREFIX}starinfo command.
Large amounts of essential backwork for starboard.""", inline = False)
    else:
        invalid_embed = discord.Embed(title = f"v{v}..? I don't know what v{v} is...", color = 0xff0000)
        invalid_embed.add_field(name = "Invalid version provided.", value = "Have you tried double checking the version you provided? Pre-releases (x.x.x-pre) do not have changelogs, try running the command without the -pre suffix.")
        return invalid_embed
    return valid_embed
