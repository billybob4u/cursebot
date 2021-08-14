import discord
from discord.ext import commands
from discord import Activity, ActivityType
from discord import DMChannel
from discord import Intents
import logging
from pathlib import Path
import json

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

secret_file = json.load(open(cwd+'/bot_config/secrets.json'))
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", case_insensitive=True, intents=intents)
bot.config_token = secret_file['token']
logging.basicConfig(level=logging.INFO)
embed = discord.Embed()

bad_words = ["8ITCH", "8itch", "$H!T", "$h!t", "ARSE", "Arse", "arse", "ASSHOLE", "asshole", "B I T C H", "b i t c h", "bit ch", "BITCH", "Bitch", "bitch", "COCK", "cock", "CUNT", "cunt", "Cunt", "DICK", "Dick", "dick", "F U C K", "f u c k", "f uck", "f uq", "FCK", "fck", "FU CK", "fu q", "fuc k", "FUCK", "FuCk", "Fuck", "fUcK", "fuck", "FUQ", "fuq", "MORON", "Moron", "moron", "NEGRO", "negro", "NIGGA", "nigga", "NIGGER", "Nigger", "nigger", "PORN", "Porn", "porn", "PUSSY", "pussy", "s hit", "SH IT", "sh it", "shi t", "SHIOT", "shiot", "SHIT", "Shit", "shit", "STFU", "Stfu", "stfu"]


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='!ANNOUNCEMENT'))

    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nCurrent prefix: !\n-----")
    print(f"{str(len(bot.guilds))} servers\n-----")
    print(f"{str(len(set(bot.get_all_members())))} members\n-----")


@bot.event
async def on_message(message):
    msg = message.content

    if message.author == bot.user:
        return

    if any(word in msg for word in bad_words):
        await message.channel.purge(limit=1)

    if msg.startswith("poop"):
        await message.channel.send("EWWWWW")

    if msg.startswith("butt"):
        await message.channel.send("EWWWWW")

    if msg.startswith("fart"):
        await message.channel.send("EWWWWW")

    if msg.startswith("puke"):
        await message.channel.send("EWWWWW")

    await bot.process_commands(message)


@bot.command(name='hello', aliases=['hi', 'hey', 'wassup'], description='HI!!!')
async def hello(ctx):
    await ctx.channel.send("Sup, I'm CurseBot. I delete bad words. Bill created me. He is so cool and I respect him. Type '!badwords' for a list of words I can detect. ")


@bot.command(name='badwords', aliases=['badword', 'words', 'cursewords', 'swearwords'], description='Sends a list of words the bot can detect')
async def badwords(ctx):
    await ctx.send(f"Don't say these words: {bad_words}", delete_after=10)


@bot.command(name='stats', aliases=['statistics, stat, information, info'], description='Sends stats about the bot')
async def stats(ctx):
    await ctx.send(f"Server Count: {len(bot.guilds)}\nMember Count: {len(set(bot.get_all_members()))}")


@bot.command(name='announcement', aliases=['announcements', 'announce', 'news'], description='Sends an announcement in a dm', pass_context=True)
async def announcement(ctx):
    userowner = bot.get_user(int(ctx.guild.owner.id))
    usermember = ctx.message.author
    username = usermember.name
    message = [f'Hi {username}! This is a message from Bill, the owner and creator of CurseBot:\nI just wanted to thank everyone for using CurseBot and I really hope the bot is benefiting you and everyone in your server. I made this bot when I just wanted my friends to stop swearing and now CurseBot is being used in 60 servers!!! Again, thank you for all the support and feel free to reach out to me at billybob4u#9526.\n\n[Invite Link](https://discord.com/oauth2/authorize?bot_id=797124326594969690&permissions=8&scope=bot)\n[Bot Website](https://cursebot.weebly.com)\n[Top.gg](https://top.gg/bot/797124326594969690)\n[DiscordBotList](https://discordbotlist.com/bots/cursebot)']

    embed = discord.Embed(
        title = 'Thank You',

        description = ''.join(message),

        color = discord.Color.red()
    )

    await DMChannel.send(usermember, embed=embed)


@bot.command(name='logout', aliases=['shutsdown', 'signout', 'disconnect'], description='Shuts down the bot')
@commands.is_owner()
async def logout(ctx):
    await ctx.send(f"Logging out... :wave:")
    await bot.logout()


@logout.error
async def logout_error(ctx, error):
    """
    Logout error
    """
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You lack permission to use this command as you do not own the bot.")
    else:
        raise error

bot.run(bot.config_token)
