import discord
from discord.ext import commands


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if self.bot.user not in message.mentions:
            return

        service = self.bot.gemini_service

        user_message = message.content
        for mention in message.mentions:
            user_message = user_message.replace(f"<@{mention.id}>", "").strip()

        if not user_message:
            return

        text = await service.chat_from_channel(
            message.channel,
            user_message=user_message,
            user_name=message.author.display_name,
        )
        if text.startswith("[Bot] "):
            text = text[len("[Bot] ") :]

        await message.reply(text)


async def setup(bot):
    await bot.add_cog(Chat(bot))
