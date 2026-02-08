import logging
import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    token = os.getenv("DISCORD_TOKEN")
    if not token:
        logger.error("DISCORD_TOKEN が設定されていません。.env ファイルを確認してください。")
        raise SystemExit(1)

    # Intents: default + message_content + members（特権 Intent）
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def setup_hook() -> None:
        """cogs/ ディレクトリから Cog を自動読み込み"""
        cogs_dir = Path(__file__).parent / "cogs"
        for filepath in sorted(cogs_dir.glob("*.py")):
            if filepath.name == "__init__.py":
                continue
            extension = f"cogs.{filepath.stem}"
            try:
                await bot.load_extension(extension)
                logger.info("Cog 読み込み成功: %s", extension)
            except Exception:
                logger.exception("Cog 読み込み失敗: %s", extension)

    @bot.event
    async def on_ready() -> None:
        assert bot.user is not None
        logger.info("ログイン: %s (ID: %s)", bot.user, bot.user.id)

        synced = await bot.tree.sync()
        logger.info("スラッシュコマンド同期完了: %d 個", len(synced))

    bot.run(token)


if __name__ == "__main__":
    main()
