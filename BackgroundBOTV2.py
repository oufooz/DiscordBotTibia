import discord
import asyncio
import subprocess
import string
import re
import traceback
from discord.ext import commands

client = discord.Client()

hunted_list = ["Ailon\xa0Diek","Kimue\xa0Stora"]
                        
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
        contents = contents.translate(translator);
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
    if( vocation == "Royal\xa0Paladin"):
       return "RP"
    if( vocation == "Elite\xa0Knight"):
       return "EK"
    if( vocation == "Master\xa0Sorcerer"):
       return "MS"
    if( vocation == "Elder\xa0Druid"):
       return "ED"
    # No Voc chosen
    return " N"

        
            
async def table(ctx):
    # Grabs the OnlineplayerList
    p = subprocess.Popen(["phantomjs.exe","github.js"])
    p.wait()
    # wait till the subprocess terminates
    content = await readSubProcessFile();
    content = split_to_vln(content);
    print(content)
    await clearNotCommand(ctx,99)
    temp = "List of Hunted Online players\n``````"
    startend = "```"
    for i in content:
            if(len(temp) > 1942):
                await client.send_message(ctx,startend+temp+startend)
                temp = ""
            tName = i[0].strip()
            # check if "name" is in huntedlist
            #if( any(s in tName for s in hunted_list)):
            tVoc = swap_voc_short(i[2].strip())
            tLevel = str(i[1]).strip()
            t= "| " + '{0: <3}'.format(tVoc) + "| " + '{0: <60}'.format(tName) + "| " +  '{0: <4}'.format(tLevel)+ "|\n"
            print(t)
            temp+= t
            

    if(len(temp) <= 1943):
            await client.send_message(ctx,startend+temp+startend)

async def my_background_task():
    await client.wait_until_ready()
    counter = 0
    channel = discord.Object(id='312008640137527296')
    while not client.is_closed:
        counter += 1
        await table(channel)
        await asyncio.sleep(5) # task runs every 60 seconds
        
async def clearNotCommand(ctx, number = 99):
    mgs = [] #Empty list to put all the messages in the log
    number = int(number) #Converting the amount of messages to delete to an integer
    async for x in client.logs_from(ctx, limit = number):
            mgs.append(x)
    if len(mgs) == 0:
        return
    if len(mgs) == 1:
        await client.delete_message(mgs[0])
    else:
        await client.delete_messages(mgs)



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
try:
    client.loop.create_task(my_background_task())
    client.run('MzA3MTI4MzIwMzQzMDE1NDQ0.C_UxCQ.jKf4B66x9bV-XvD4ALL6A7AMM0o')
except Exception as e:
     traceback.print_exc()
     raise e

