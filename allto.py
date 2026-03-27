import discord
from discord.ext import commands
import asyncio
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

    timeout_duration = timedelta(days=7)

    success = 0
    fail = 0

    print("処理を開始します…")

for guild in bot.guilds:
    for member in guild.members:
        
        if member.bot:
            continue

        if member.top_role >= guild.me.top_role:
            continue

        try:
            
            if not member.is_timed_out():
                await member.timeout(timeout_duration, reason="地球温暖化を阻止するため")
                success += 1
        except discord.Forbidden:
            fail += 1
        except discord.HTTPException:
            fail += 1

        await asyncio.sleep(1)

    print(f"完了: {success}人成功 / {fail}人失敗")

bot.run(os.getenv("DISCORD_BOT_TOKEN"))