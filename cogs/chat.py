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

        user_message = message.content
        for mention in message.mentions:
            user_message = user_message.replace(f"<@{mention.id}>", "").strip()

        images = [
            (await attachment.read(), attachment.content_type)
            for attachment in message.attachments
            if attachment.content_type and attachment.content_type.startswith("image/")
        ]

        if not user_message and not images:
            return

        text = self.bot.gemini_service.reply(user_message, images=images or None)
        await message.reply(text)


async def setup(bot):
    await bot.add_cog(Chat(bot))
