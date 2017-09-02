"""
todo:
randomly @ someone and ask "PUBG?"
"""

from discord.ext import commands
import random
import time

desc = "Somenbot. Provides little to no utilities."
token = 'token'  # replace with actual token
bot = commands.Bot(command_prefix='!', description=desc, pm_help=True)


@bot.event
async def on_ready():
    print('Logged in as', bot.user.name)
    print('ID:', bot.user.id)
    print('--------------------')


@bot.command(help="Ping/Pong")
async def somen():
    await bot.say("I'm gay!")


@bot.command(pass_context=True, aliases=['clear'], help="Wipes past 100 bot messages.")
async def clean(ctx):  # deletes past Somenbot messages
    async for message in bot.logs_from(ctx.message.channel):
        if message.author == bot.user:
            await bot.delete_message(message)
    await bot.say("Deleted past 100 messages", delete_after=2)


@bot.command(help="Picks an item from the gamelist at random.\n"
                  "In true Somen fashion, sometimes it won't make a choice.", no_pm=True)
async def choosegame(*args):
    try:
        presult = random.random()
        if presult > 0.10:  # 90% chance
            result = random.choice(args)
            await bot.say("Lets play...")
            time.sleep(1)
            await bot.say(result)
        else:  # 10% chance
            await bot.say("Uhhh... I don't know.")
    except IndexError:
        await bot.say("List some games you libtard!")


bot.run(token)  # loops
