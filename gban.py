import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

BANNED_USER_IDS = {1286942627991781480, 987654321098765432}

@bot.event
async def on_member_join(member):
    if member.id in BANNED_USER_IDS:
        try:
            await member.ban(reason="地球温暖化を阻止するため")
            print(f"[BAN] {member} ({member.id}) をBanしました。")
        except Exception as e:
            print(f"[ERROR] {member} のBanに失敗: {e}")

@bot.event
async def on_ready():
    print(f"Botが起動しました: {bot.user}")

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
