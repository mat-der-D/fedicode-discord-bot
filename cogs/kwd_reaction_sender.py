from discord import Message
from discord.ext import commands


PUDDING = "🍮"
HONSHITSU = "<:honshitsu:1268731663052177458>"


class KwdReactionSender(commands.Cog):
    """キーワードに対してリアクションを送る"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.kwd_to_emoji = self.create_kwd_to_emoji()
    
    @staticmethod
    def create_kwd_to_emoji() -> dict[str, str]:
        kwds_to_emoji = {
            ("ぷりん", "プリン"): PUDDING,
            ("あほなこと", "アホなこと"): HONSHITSU,
        }

        k2e = {}
        for kwds, emoji in kwds_to_emoji.items():
            for kwd in kwds:
                k2e[kwd] = emoji
        return k2e

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        # Bot 自身のメッセージには反応しない
        if message.author.bot:
            return
        
        for kwd, emoji in self.kwd_to_emoji.items():
            if kwd not in message.content:
                continue
            await message.add_reaction(emoji)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(KwdReactionSender(bot))
