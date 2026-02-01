import os
import discord
import requests
from dotenv import load_dotenv
import asyncio
import aiohttp
from typing import List, Set

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

class FilterBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._disallow_list: Set[str] = set()
        self._disallow_list_lock = asyncio.Lock()
        self._last_update = 0
        self._update_interval = 3600

    async def _fetch_disallow_list(self) -> List[str]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("FILTER URL HERE") as response:
                    if response.status == 200:
                        text = await response.text()
                        return [line.strip() for line in text.splitlines() if line.strip()]
        except Exception as e:
            print(f"disallow list fetch error: {e}")
        return []

    async def _update_disallow_list(self):
        current_time = asyncio.get_event_loop().time()
        if current_time - self._last_update < self._update_interval:
            return

        async with self._disallow_list_lock:
            disallow_list = await self._fetch_disallow_list()
            self._disallow_list = set(disallow_list)
            self._last_update = current_time

    def _is_disallow_url(self, url: str) -> bool:
        return any(bad_url in url for bad_url in self._disallow_list)

    async def on_ready(self):
        await self._update_disallow_list()
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        await self._update_disallow_list()

        urls = [word for word in message.content.split()]
        
        for url in urls:
            if self._is_disallow_url(url):
                try:
                    if message.channel.permissions_for(message.guild.me).manage_messages:
                        await message.delete()
                        await message.channel.send(f"{message.author.mention} ❌ DisAllowed Word Detected!")
                    else:
                        await message.channel.send(f"{message.author.mention} ⚠️ Potential disallowed word detected. Admins have been notified.")
                except discord.errors.Forbidden:
                    print("Cannot delete disallowed word included message. Check permissions.")
                except Exception as e:
                    print(f"Unexpected error handling disallowed word: {e}")

def main():
    bot = FilterBot(intents=intents)
    bot.run(os.getenv('DISCORD_BOT_TOKEN'))

if __name__ == "__main__":
    main()


