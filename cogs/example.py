from discord import Interaction, app_commands
from discord.ext import commands


class Example(commands.Cog):
    """サンプル Cog（実装の参考用）"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ping", description="Pong! と返します")
    async def ping(self, interaction: Interaction) -> None:
        await interaction.response.send_message("Pong!")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Example(bot))
