import random
from discord import Interaction, app_commands
from discord.ext import commands

MIN_INDEX = 1
MAX_INDEX = 177561


class RandomDajare(commands.Cog):
    """ダジャレ・ステーションからランダムに記事のURLを返す"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="dajare", description="ランダムにダジャレをお届け")
    async def dajare(self, interaction: Interaction) -> None:
        index = random.randint(MIN_INDEX, MAX_INDEX)
        url = f"https://dajare.jp/works/{index}/"
        await interaction.response.send_message(url)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RandomDajare(bot))
