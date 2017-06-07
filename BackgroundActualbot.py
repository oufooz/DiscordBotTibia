import discord
import asyncio
import subprocess
import string
import re
import traceback
import copy
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

hunted_list = []
friend_list = []
                        
async def readSubProcessFile():
    try:
        with open("output.txt") as file_object:
            contents = file_object.read()
    except FileNotFoundError:
            msg = 'couldnt find the file'
            print(msg)
            return " "
    else:
        deleteChars = "Â\t"
        translator = str.maketrans('', '', deleteChars)
        contents = contents.translate(translator)
        contents = contents.replace("\xa0"," ")
        words = contents.split(',');
        return words
    
def split_to_vln(content):
    t = []
    for i in content:
          t.append(list(filter(None, re.split(r'(\d+)', i))))
    return t
            
def swap_voc_short(vocation):
    if( vocation == "Paladin"):
       return " P"
    if( vocation == "Sorcerer"):
       return " S"
    if( vocation == "Druid"):
       return " D"
    if( vocation == "Knight"):
       return " K"
    if( vocation == "Royal Paladin"):
       return "RP"
    if( vocation == "Elite Knight"):
       return "EK"
    if( vocation == "Master Sorcerer"):
       return "MS"
    if( vocation == "Elder Druid"):
       return "ED"
    # No Voc chosen
    return " N"

        
            
async def table(ctx):
    # Grabs the OnlineplayerList
    p = subprocess.Popen(["phantomjs.exe","github.js"])
    p.wait()
    # wait till the subprocess terminates
    print( "\n\n\n length of huntedlist = " + str(len(hunted_list))+"\n\n\n")
    if(len(hunted_list) <= 0):
        return
    content = await readSubProcessFile();
    content = split_to_vln(content);
    print(content)
    await clearNotCommand(ctx,99)
    temp = "List of Hunted Online players\n"
    startend = "```"
    for i in content:
            if(len(temp) > 1942):
                await bot.send_message(ctx,startend+temp+startend)
                temp = ""
            tName = i[0].strip()
            # check if "name" is in huntedlist
            if( any(s in tName for s in hunted_list)):
                tVoc = swap_voc_short(i[2].strip())
                tLevel = str(i[1]).strip()
                t= "| " + '{0: <3}'.format(tVoc) + "| " + '{0: <60}'.format(tName) + "| " +  '{0: <4}'.format(tLevel)+ "|\n"
                print(t)
                temp+= t
                

    if(len(temp) <= 1943):
            await bot.send_message(ctx,startend+temp+startend)
    if(len(friend_list) <= 0):
        return
    temp = "List of Friends Online \n``````"
    for i in content:
            if(len(temp) > 1942):
                await bot.send_message(ctx,startend+temp+startend)
                temp = ""
            tName = i[0].strip()
            # check if "name" is in huntedlist
            if( any(s in tName for s in friend_list)):
                tVoc = swap_voc_short(i[2].strip())
                tLevel = str(i[1]).strip()
                t= "| " + '{0: <3}'.format(tVoc) + "| " + '{0: <60}'.format(tName) + "| " +  '{0: <4}'.format(tLevel)+ "|\n"
                print(t)
                temp+= t
                

    if(len(temp) <= 1943):
            await bot.send_message(ctx,startend+temp+startend)
    
            
    
    

async def my_background_task():
    await loadlist(False)
    await loadlist(True)
    await bot.wait_until_ready()
    counter = 0
    channel = discord.Object(id='312008640137527296')
    while not bot.is_closed:
        counter += 1
        await table(channel)
        await asyncio.sleep(30) # task runs every 60 seconds
        
async def clearNotCommand(ctx, number = 99):
    mgs = [] #Empty list to put all the messages in the log
    number = int(number) #Converting the amount of messages to delete to an integer
    async for x in bot.logs_from(ctx, limit = number):
            mgs.append(x)
    if len(mgs) == 0:
        return
    if len(mgs) == 1:
        await bot.delete_message(mgs[0])
    else:
        await bot.delete_messages(mgs)

@bot.group(pass_context = True)
async def add(ctx):
    """ Add to friend or Hunted"""
    if (ctx.invoked_subcommand is None):
        await bot.say("Invalid Add command Passed ... ")
        return
    
@add.command(name="hunted")
async def add_hunted(name :str):
    name = name.title()
    if name in friend_list:
        await bot.say("Player {} in friendlist\n remove first".format(name))
        await friends()
        return
    if name in hunted_list:
        await bot.say("Player {} already in huntedlist".format(name))
        await hunted()
        return
    hunted_list.append(name)
    await bot.say("Player added {} to hunted list".format(name))
    await savelist(False)
    await hunted()

@add.command(name="friend")
async def add_friend(name :str):
    name = name.title()
    if name in hunted_list:
        await bot.say("Player {} in  huntedlist\n remove first".format(name))
        await hunted()
        return
    if name in friend_list:
        await bot.say("Player {} already in friends list".format(name))
        await friends()
        return
    friend_list.append(name)
    await bot.say("Player added {} to friends list".format(name))
    await savelist(True)
    await friends()
    
@bot.group(pass_context = True)
async def remove(ctx):
    """ remove to friend or Hunted"""
    if (ctx.invoked_subcommand is None):
        await bot.say("Invalid remove command Passed ... ")
        return

@remove.command(name="hunted")
async def remove_hunted(name:str):
    name = name.title()
    if name in hunted_list:
        hunted_list.remove(name)
        bot.say("updated huntedlist")
        await savelist(False)
        await hunted()
    else:
        await bot.say("Player {} was not in huntedlist".format(name))

@remove.command(name="friend")
async def remove_friend(name:str):
    name = name.title()
    if name in friend_list:
        friend_list.remove(name)
        bot.say("updated friendlist")
        await savelist(True)
        await friends()
    else:
        await bot.say("Player {} was not in friendlist".format(name))

@bot.group(pass_context = True)
async def display(ctx):
    if (ctx.invoked_subcommand is None):
        await bot.say("Invalid display command Passed ... ")
        return

@display.command(name="hunted")
async def display_hunted():
    await hunted()

async def hunted():
    await bot.say("Current hunted list \n")
    await bot.say(hunted_list)
    
@display.command(name="friend")
async def display_friend():
    await friends()

async def friends():
    await bot.say("Current friend list \n")
    await bot.say(friend_list)


async def loadlist(t :bool):
    filename = ""
    if(t == False):
        filename = "hunted.txt"
    else:
        filename = "friend.txt"
    try:
        with open(filename,"r") as file_object:
            contents = file_object.read()
    except FileNotFoundError:
            msg = 'couldnt find the file' + filename
            print(msg)
            return False
    else:
        contents = contents.split('\n')
        if(t == False):
            for i in contents:
                if(i == ""):
                    continue
                hunted_list.append(i)
            print(hunted_list)
        else:
            for i in contents:
                if(i == ""):
                    continue
                friend_list.append(i)
            print(friend_list)

        return True

''' 
    t == false for huntedlist
    t == true  for friendlist
'''
async def savelist(t : bool):
    filename = ""
    if(t == False):
        filename = "hunted.txt"
    else:
        filename = "friend.txt"
    try:
        file_object = open(filename,'w')
    except FileNotFoundError:
            msg = 'couldnt find the file' + filename
            print(msg)
            return False
    else:
        if(t == False):
            for i in hunted_list:
                if(i == ""):
                    continue
                print(i , file= file_object)
        if(t == True):
            for i in friend_list:
                if(i == ""):
                    continue
                print(i , file= file_object)
        return True

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
try:
    bot.loop.create_task(my_background_task())
    bot.run('MzA3MTI4MzIwMzQzMDE1NDQ0.C_UxCQ.jKf4B66x9bV-XvD4ALL6A7AMM0o')
except Exception as e:
     traceback.print_exc()
     raise e

