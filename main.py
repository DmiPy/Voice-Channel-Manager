import time

import discord
from discord.ext import commands
import asyncio

import settings


def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"{bot.user.id} is loading...")
        time.sleep(2)
        print(f"Logged in as {bot.user}")

    bot.run(settings.DISCORD_API_SECRET)





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
