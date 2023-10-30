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

    @commands.command(brief="Создает временный войс чат: <название> <упоминания участников>")
    # change function so, that it takes a name for a channel and then takes a list of mentions of users
    async def tempchannel(self, ctx, channel_name: str, *users: discord.Member):
        """
            Создает временный голосовой канал на сервере Discord.
            Параметры:
                - `channel_name`: Название временного канала.
                - `users`: Упомянутые участники, которые имеют доступ к каналу.
            Пример использования:
              !create_temp_channel TemporaryChannel @user1 @user2
            """
        if channel_name.startswith("<@"):
            channel_name = "Посиделки🍿📺😏"
        guild = ctx.guild

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=True, connect=False),
            guild.me: discord.PermissionOverwrite(read_messages=True, connect=True)
        }
        usernames = [user.name for user in users]
        for user in users:
            overwrites[user] = discord.PermissionOverwrite(read_messages=True, connect=True)

        mention_users = ', '.join(user.mention for user in users)
        await ctx.send(f"Канал '{channel_name}' был создан {ctx.author.name}. Заходите {mention_users}!")
        time.sleep(5)
        channel = await guild.create_voice_channel(f"{channel_name}", overwrites=overwrites)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Канал создан {ctx.author.name}"))
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
            print(f"Канал '{channel.name}' был удален.")
            # Отправка сообщения в текстовый канал
            text_channel = self.bot.get_channel(1163053302171324458)
            if text_channel:
                await text_channel.send(f"Канал {channel.name} был удален.")


async def setup(bot):
    await bot.add_cog(VoiceChannels(bot))
