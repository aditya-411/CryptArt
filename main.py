import discord
from discord.ext import commands as cmd
from file_input import file_input


from dotenv import load_dotenv
import os

load_dotenv()
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
bot = cmd.Bot(intents=intents, command_prefix="!")

@bot.event
async def on_ready():
    print('bot is up')
    await bot.add_cog(file_input(bot))

bot.run(os.getenv("token"))
