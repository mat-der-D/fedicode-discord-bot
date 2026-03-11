import discord
from discord import app_commands
from discord.ext import commands


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="chat")
    async def chat(self, interaction: discord.Interaction, message: str):
        await interaction.response.defer()

        service = self.bot.gemini_service

        text = await service.chat_from_channel(
            interaction.channel,
            user_message=message,
            user_name=interaction.user.display_name,
        )
        if text.startswith("[Bot]"):
            text = text[len("[Bot]") :]

        response = (
            f"(**ユーザー:** {message})"  #
            "\n"  #
            "\n"  #
            f"{text}"  #
        )

        await interaction.followup.send(response)


async def setup(bot):
    await bot.add_cog(Chat(bot))
