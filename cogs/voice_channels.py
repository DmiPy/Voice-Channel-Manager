import time

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
            guild.default_role: discord.PermissionOverwrite(read_messages=True, connect=False),
            guild.me: discord.PermissionOverwrite(read_messages=True, connect=True)
        }

        for user in users:
            overwrites[user] = discord.PermissionOverwrite(read_messages=True, connect=True)

        channel = await guild.create_voice_channel("Временный", overwrites=overwrites)
        temporary_channels[channel.id] = time.time()

    @tasks.loop(seconds=5)
    async def check_temporary_channels(self):
        # write a function that deletes temporary channels if they are empty and older than 5 minutes and 10 seconds have passed since all members left
        for channel_id, time_created in temporary_channels.items():
            if time.time() - time_created > 5 * 60 + 10:
                channel = self.bot.get_channel(channel_id)
                if channel is not None:
                    if len(channel.members) == 0:
                        await channel.delete()
                        temporary_channels.pop(channel_id)


async def setup(bot):
    await bot.add_cog(VoiceChannels(bot))
