import urllib.request
import urllib.error
import random
from discord import Interaction, app_commands
from discord.ext import commands

MIN_INDEX = 1
MAX_INDEX = 177561


def make_url(index: int):
    return f"https://dajare.jp/works/{index}/"


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def is_available(url: str) -> bool:
    opener = urllib.request.build_opener(_NoRedirectHandler())
    try:
        with opener.open(url, timeout=5) as response:
            return response.status == 200
    except urllib.error.URLError:
        return False


def get_random_available_url() -> str:
    while True:
        index = random.randint(MIN_INDEX, MAX_INDEX)
        url = make_url(index)
        if is_available(url):
            return url


class RandomDajare(commands.Cog):
    """ダジャレ・ステーションからランダムに記事のURLを返す"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="dajare", description="ランダムにダジャレをお届け")
    async def dajare(self, interaction: Interaction) -> None:
        url = get_random_available_url()
        await interaction.response.send_message(url)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RandomDajare(bot))
