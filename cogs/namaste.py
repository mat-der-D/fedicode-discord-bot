from discord import Message
from discord.ext import commands, tasks
from datetime import time, timezone, timedelta
import random

TZ_TOKYO = timezone(timedelta(hours=9))

class Namaste(commands.Cog):
    """ﾅﾏｽﾃ に ﾅﾏｽﾃ と返すbot"""
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.namaste_said_today = False
        self.target_channel_id = 1134728733308227664  # 投稿先のチャンネルID
        self.reset_flag.start() 
        self.check_namaste.start()

        # ﾅﾏｽﾃのバリエーション
        self.namaste_variations = [
            'ﾅﾏｽﾃ',
            'ﾅﾏｽﾃ〜',
            'ﾅﾏｽﾃ!',
            'ﾅﾏｽﾃ〜!',
            'ﾅ・ﾏ・ｽ・ﾃ',
            'ﾅﾏｽﾃ☆',
            'ﾅ   ﾏ   ｽ   ﾃ',
            'ﾅﾏｽﾃ……',
            'ﾅﾏｽﾃｰｯ',
            'ﾅﾏｽﾃｯ',
            'ﾅﾏｽt……',
            'namaste',
            'なますて！',
            'なま☆すて'
        ]
    
    def cog_unload(self) -> None:
        self.check_namaste.cancel()
    
    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        if message.author == self.bot.user:
            return
        
        if 'ﾅﾏｽﾃ' in message.content:
            self.namaste_said_today = True
            # ランダムにバリエーションを選択
            response = random.choice(self.namaste_variations)
            await message.reply(response)

    @tasks.loop(time=time(hour=0, minute=0, tzinfo=TZ_TOKYO))  # 毎日0:00にリセット
    async def reset_flag(self) -> None:
        self.namaste_said_today = False

    
    @tasks.loop(time=time(hour=9, minute=30, tzinfo=TZ_TOKYO))
    async def check_namaste(self) -> None:
        if not self.namaste_said_today:
            channel = self.bot.get_channel(self.target_channel_id)
            if channel:
                await channel.send(random.choice(self.namaste_variations))  # こっちは返信先がないので普通の投稿
        
    @reset_flag.before_loop
    async def before_reset_flag(self) -> None:
        await self.bot.wait_until_ready()
    
    @check_namaste.before_loop
    async def before_check_namaste(self) -> None:
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Namaste(bot))