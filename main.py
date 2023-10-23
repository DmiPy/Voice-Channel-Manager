import discord
from discord.ext import commands
import asyncio


token = "MTE2NjEwMzkyMjEzMDMwMTA1OQ.GbXgkJ.UL7cim566TWVYrq5SHWYL8TEGfEad-sw11JG6k"
prefix = "!"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=prefix, intents=intents)


@bot.event()
async def on_ready():
    print(f"Logged in as {bot.user}")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
