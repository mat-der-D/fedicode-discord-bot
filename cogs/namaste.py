from discord import Message
from discord.ext import commands, tasks
from datetime import time, timezone, timedelta

class Namaste(commands.Cog):
    """ﾅﾏｽﾃ に ﾅﾏｽﾃ と返すbot"""
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.namaste_said_today = False
        self.target_channel_id = 1234567890  # 投稿先のチャンネルID
        self.check_namaste.start()
    
    def cog_unload(self) -> None:
        self.check_namaste.cancel()
    
    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        if message.author == self.bot.user:
            return
        
        if 'ﾅﾏｽﾃ' in message.content:
            self.namaste_said_today = True
            await message.reply('ﾅﾏｽﾃ')  # 返信に変更
    
    @tasks.loop(time=time(hour=9, minute=30, tzinfo=timezone(timedelta(hours=9))))
    async def check_namaste(self) -> None:
        if not self.namaste_said_today:
            channel = self.bot.get_channel(self.target_channel_id)
            if channel:
                await channel.send('ﾅﾏｽﾃ')  # こっちは返信先がないので普通の投稿
        
        self.namaste_said_today = False
    
    @check_namaste.before_loop
    async def before_check_namaste(self) -> None:
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Namaste(bot))