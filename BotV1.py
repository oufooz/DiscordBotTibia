import discord
from discord.ext import commands
import random

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='!', description=description)
voc = ['MS' , 'EK', 'ED', 'RP',' S',' K',' D',' P']
levels = [x for x in range(0,1)]
name = [ 'a','b','c','d','e','f','g' ]
count = 1
Dictb = []
for name in name:
        for vo in voc:
                for l in levels:
                        b = {'vocation':vo,'name':name,'level':l}
                        Dictb.append(b)
                
print(Dictb)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def add(left : int, right : int):
        """Adds two numbers together."""
        try:
                t = left+right
                await bot.say(left + right)
        except Exception:
                await bot.say("Missing Argument")
                

@bot.command(pass_context = True)
async def table(ctx):
        temp = "List of Online players\n``````"
        global count
        count += 1
        startend = "```"
        for i in Dictb:
                if(len(temp) > 1942):
                    await bot.say(startend+temp+startend)
                    temp = ""
                tVoc = i['vocation']
                tName = i['name'] 
                tLevel = str(i['level']+ count)
                t= "| " + '{0: <3}'.format(tVoc) + "| " + '{0: <60}'.format(tName) + "| " +  '{0: <4}'.format(tLevel)+ "|\n"
                #print(t)
                temp+= t
        if(len(temp) <= 1943):
                await bot.say(startend+temp+startend)

@bot.command(pass_context = True)
async def hi(ctx):
        """ Says hi @user """
        await clearNotCommand(ctx,99)
        await bot.say("Hello you")

@bot.command(pass_context = True)
async def clear(ctx,number = 100):
        await clearNotCommand(ctx,number)
        
async def clearNotCommand(ctx, number = 99):
        mgs = [] #Empty list to put all the messages in the log
        number = int(number) #Converting the amount of messages to delete to an integer
        async for x in bot.logs_from(ctx.message.channel, limit = number):
                mgs.append(x)
        if len(mgs) == 0:
                return
        if len(mgs) == 1:
                await bot.delete_message(mgs[0])
        else:
                await bot.delete_messages(mgs)

@bot.command()
async def roll(dice : str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(*choices : str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))

@bot.command()
async def repeat(times : int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await bot.say(content)

@bot.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))

@bot.group(pass_context=True)
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))

@cool.command(name='bot')
async def _bot():
    """Is the bot cool?"""
    await bot.say('Yes, the bot is cool.')

bot.run('MzA3MTI4MzIwMzQzMDE1NDQ0.C_UxCQ.jKf4B66x9bV-XvD4ALL6A7AMM0o')
