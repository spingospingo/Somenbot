"""
todo:
change all open(gamefile) to when statements, to avoid having to use games_list.close()
"""

from discord.ext import commands
from discord import errors
import time
import random

desc = "Somenbot. Provides little to no utilities."
token = 'token'  # replace with actual token
bot = commands.Bot(command_prefix='!', description=desc, pm_help=True)
gamefile = 'Games'

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
    time.sleep(2)  # might be worth changing to a separate thread
    async for message in bot.logs_from(ctx.message.channel):
        if message.author == bot.user:
            await bot.delete_message(message)


@bot.command(help="Returns a list of games.", no_pm=True)
async def games():
    try:
        games_list = open(gamefile)
        result = games_list.read()
        games_list.close()
        await bot.say(result)
    except errors.HTTPException:
        await bot.say(no_games_message)


@bot.command(help="Adds an item to a list of games to choose from.\n"
                  "For names longer than one word, put quotes around entry.", no_pm=True)
async def addgame(game):
    games_list = open(gamefile, 'a') 
    output = game + "\n"
    games_list.write(output)
    games_list.close()
    output = "Added " + game
    await bot.say(output)


@bot.command(help="Removes an item from the game list.\n"
                  "For names longer than one word, put quotes around entry.", no_pm=True, parent='games')
async def removegame(game):  # can only delete one game at a time as of now
    # copies all non-flagged listings to the top of the file, and deletes old entries
    games_list = open(gamefile, 'r+')
    lines = games_list.readlines()
    games_list.seek(0)  # direct pointer to beginning
    for item in lines:
        if item != (game+"\n"):  # flag item to be rewritten
            games_list.write(item)
        else:  # items that don't get flagged get deleted...
            output = "Deleting " + game
            await bot.say(output)
    games_list.truncate()  # ...here!
    games_list.close()


@bot.command(help="Picks an item from the gamelist at random.\n"
                  "In true Somen fashion, sometimes it won't make a choice.", no_pm=True)
async def choosegame():
    try:
        presult = random.random()
        if presult > 0.10:  # 90% chance
            games_list = open(gamefile)
            lines = games_list.readlines()
            result = random.choice(lines)
            output = result.rstrip('\n')  # temp file so that \n doesn't get stripped from actual entry
            await bot.say(output)
            games_list.close()
        else:  # 10% chance
            await bot.say("Uhhh... I don't know.")
    except IndexError:
        await bot.say(no_games_message)


bot.run(token)  # loops
