import urllib.request
import urllib.error
import random
from html.parser import HTMLParser
from discord import Interaction, app_commands
from discord.ext import commands

MIN_INDEX = 1
MAX_INDEX = 177561


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class _TitleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._in_title = False
        self.title: str | None = None

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self._in_title = True

    def handle_data(self, data):
        if self._in_title:
            self.title = data

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False


def fetch_title(url: str) -> str | None:
    opener = urllib.request.build_opener(_NoRedirectHandler())
    try:
        with opener.open(url, timeout=5) as response:
            if response.status != 200:
                return None
            html = response.read().decode()
            parser = _TitleParser()
            parser.feed(html)
            return parser.title
    except urllib.error.URLError:
        return None


def make_url(index: int):
    return f"https://dajare.jp/works/{index}/"


def get_random_dajare() -> tuple[str, int]:
    while True:
        index = random.randint(MIN_INDEX, MAX_INDEX)
        url = make_url(index)
        if (title := fetch_title(url)) is not None:
            return trim_footer(title), index


def trim_footer(title: str) -> str:
    footer = " / ダジャレ・ステーション | 面白いダジャレが満載！"
    return title.replace(footer, "").strip()


class RandomDajare(commands.Cog):
    """ダジャレ・ステーションからランダムにダジャレを取得して返す"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="dajare", description="ランダムにダジャレをお届け")
    async def dajare(self, interaction: Interaction) -> None:
        dajare, index = get_random_dajare()
        message = f"{dajare} ({index}番)"
        await interaction.response.send_message(message)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RandomDajare(bot))
