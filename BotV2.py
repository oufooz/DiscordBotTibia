import discord

import random

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='!', description=description)

players = []

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    
@bot.command()
async def hi():
        """ Says hi @user """
        await bot.say("Hello you")

                        
async def readHuntedList():
    try:
        with open("hunted.txt") as file_object:
            contents = file_object.read()
    except FileNotFoundError:
            msg = 'couldnt find the file'
            print(msg)
            return " "
    else:
        players = contents.split(',');
        
@bot.command()
async def add(name :str):
    players.append(name)
    await bot.say("Player added {} to hunted list".format(name))
    
@bot.command()
async def huntedlist():
    await bot.say("Current hunted list \n")
    await bot.say(players)

bot.run('MzA3MTI4MzIwMzQzMDE1NDQ0.C_UxCQ.jKf4B66x9bV-XvD4ALL6A7AMM0o')
