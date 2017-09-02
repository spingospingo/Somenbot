"""
todo:
change all open('Games') to when statements, to avoid having to use games_list.close()
"""

from discord.ext import commands
import time
import random

desc = "Somenbot. Provides little to no utilities."
token = 'MzUyOTY5MzQ1OTkyNzUzMTU0.DIo61w.5rVeEXN6lzGiZikMb7p1u177uiI'
bot = commands.Bot(command_prefix='!', description=desc, pm_help=True)

no_games_message = "There's no games on the list, you libcuck."


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
    await bot.say("Deleting past 100 bot messages.")
    time.sleep(2)
    async for message in bot.logs_from(ctx.message.channel):
        if message.author == bot.user:
            await bot.delete_message(message)


@bot.command(help="Returns a list of games.", no_pm=True)
async def games():
    try:
        games_list = open('Games')
        result = games_list.read()
        games_list.close()
        await bot.say(result)
    except Exception:
        await bot.say(no_games_message)


@bot.command(help="Adds an item to a list of games to choose from.\n"
                  "For names longer than one word, put quotes around entry.", no_pm=True)
async def addgame(game):
    games_list = open('Games', 'a')
    output = game + "\n"
    games_list.write(output)
    games_list.close()
    output = "Added " + game
    await bot.say(output)


@bot.command(help="Removes an item from the game list.\n"
                  "For names longer than one word, put quotes around entry.", no_pm=True, parent='games')
async def removegame(game):  # can only delete one game at a time as of now
    games_list = open('Games', 'r+')
    lines = games_list.readlines()
    games_list.seek(0)
    for item in lines:
        if item != (game+"\n"):
            games_list.write(item)
        else:
            output = "Deleting " + game
            await bot.say(output)
    games_list.truncate()
    games_list.close()


@bot.command(help="Picks an item from the gamelist at random.\n"
                  "In true Somen fashion, sometimes it won't make a choice.", no_pm=True)
async def choosegame():
    try:
        presult = random.random()
        if presult > 0.10:
            games_list = open('Games')
            lines = games_list.readlines()
            result = random.choice(lines)
            output = result.rstrip('\n')
            await bot.say(output)
            games_list.close()
        else:
            await bot.say("Uhhh... I don't know.")
    except IndexError:
        await bot.say(no_games_message)


bot.run(token)
