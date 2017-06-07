import discord
from discord.ext import commands
import aiohttp
import asyncio
import bs4

"""


Settings = {
    'server' :
    'huntedlist' :
    'friendlist' :
}

def check_server():
    ALLOWED_SERVERS = []
"""

async def fetch(session, url):
    with aiohttp.Timeout(10, loop=session.loop):
        async with session.get(url) as response:
            return await response.text()

async def main(loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        html = await fetch(session, 'https://secure.tibia.com/community/?subtopic=worlds')
        print(html)
        soup = bs4.BeautifulSoup(html)
        a = soup.find_all("a")
        print(a)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
