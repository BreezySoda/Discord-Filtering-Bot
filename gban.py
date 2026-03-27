import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

BANNED_USER_IDS = {1286942627991781480, 987654321098765432}

@bot.event
async def on_member_join(member):
    if member.id in BANNED_USER_IDS:
        try:
            await member.ban(reason="自動BAN（参加時）")
            print(f"[BAN] {member} ({member.id}) をBanしました。")
        except discord.Forbidden:
            print(f"[ERROR] 権限不足で {member} をBanできません")
        except discord.HTTPException as e:
            print(f"[ERROR] HTTPエラー: {e}")

@bot.event
async def on_ready():
    print(f"Botが起動しました: {bot.user}")

    for guild in bot.guilds:
        print(f"[CHECK] サーバー: {guild.name}")

        async for member in guild.fetch_members(limit=None):
            if member.id in BANNED_USER_IDS:
                try:
                    await member.ban(reason="自動BAN（既存メンバー）")
                    print(f"[BAN] {member} ({member.id}) をBanしました。")
                    await asyncio.sleep(1)
                except discord.Forbidden:
                    print(f"[ERROR] 権限不足で {member} をBanできません")
                except discord.HTTPException as e:
                    print(f"[ERROR] HTTPエラー: {e}")

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
