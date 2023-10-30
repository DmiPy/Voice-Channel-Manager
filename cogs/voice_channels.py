import time

import discord
from discord.ext import commands, tasks

class TemporaryChannel:
    def __init__(self, channel_id, created_at):
        self.channel_id = channel_id
        self.created_at = created_at

temporary_channels = {}

class VoiceChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_temporary_channels.start()

    @commands.command()
    async def create_temp_channel(self, ctx):
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
        temporary_channels[channel.id] = TemporaryChannel(channel.id, time.time())

    @tasks.loop(minutes=1)
    async def check_temporary_channels(self):
        # delete voice channels that are older than 1 minute and have no users in them
        channels_to_delete = []

        for channel_id, temp_channel in temporary_channels.copy().items():
            if time.time() - temp_channel.created_at > 60:
                channel = self.bot.get_channel(channel_id)
                if channel and len(channel.members) == 0:
                    channels_to_delete.append(channel)

        for channel in channels_to_delete:
            await channel.delete()
            del temporary_channels[channel.id]
            print(f"Канал {channel.name} был удален.")



async def setup(bot):
    await bot.add_cog(VoiceChannels(bot))
