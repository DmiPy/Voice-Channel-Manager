import discord
from discord.ext import commands, tasks

temporary_channels = {}

class VoiceChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def create_time_channel(self, ctx):
        guild = ctx.guild
        users = ctx.message.mentions


        print(users)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False, connect=False),
            guild.me: discord.PermissionOverwrite(read_messages=True, connect=True)
        }

        for user in users:
            overwrites[user] = discord.PermissionOverwrite(read_messages=True, connect=True)

        channel = await guild.create_voice_channel("Временный", overwrites=overwrites)


async def setup(bot):
    await bot.add_cog(VoiceChannels(bot))
