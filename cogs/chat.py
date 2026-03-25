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

        if not user_message:
            return

        text = self.bot.gemini_service.reply(user_message)
        await message.reply(text)


async def setup(bot):
    await bot.add_cog(Chat(bot))
