import time
from cogs.voice_channels import VoiceChannels
import discord
from discord.ext import commands
import asyncio

import settings

logger = settings.logging.getLogger("bot")


def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        print(f"{bot.user.id} is loading...")
        time.sleep(2)
        print(f"Logged in as {bot.user}")
        await bot.load_extension("cogs.voice_channels")

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Тебе по ебалу дать? Такой команды нет...")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Хоть мои пальцы и разбросаны по всему миру, но даже я могу пересчитать их и понять, что ты забыл ввести аргументы, додик...")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("Ты думаешь, что я дурак? У тебя нет прав на это, щенок...")

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()

