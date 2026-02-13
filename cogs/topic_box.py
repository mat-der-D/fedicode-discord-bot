from discord import Interaction, app_commands, TextChannel, Message
from discord.ext import commands
import random

CATEGORY_TO_EMOJI = {
    'tech': '💻',
    'daily': '📝',
}

async def gather_messages(channel: TextChannel, category: str | None) -> list[Message]:
    return [
        message
        async for message in channel.history(limit=100)
        if is_target_message(message, category)
    ]


def is_target_message(message: Message, category: str | None) -> bool:
    # ✅がついたメッセージは除外
    if any(reaction.emoji == '✅' for reaction in message.reactions):
        return False

    # カテゴリ指定なしの場合は全て対象
    if not category:
        return True

    # カテゴリ指定がある場合はフィルタリング
    emoji = CATEGORY_TO_EMOJI.get(category)
    if not emoji:
        return False

    # 指定された絵文字がリアクションについているかチェック
    has_reaction = any(
        reaction.emoji == emoji
        for reaction in message.reactions
    )
    return has_reaction

class TopicBox(commands.Cog):
    """お題箱bot"""
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.topic_channel_id = 1471134377894215701  # お題箱チャンネルのIDに置き換えてください
    
    @app_commands.command(name="topic", description="お題箱からランダムにお題を選びます")
    @app_commands.describe(category="お題のカテゴリ（省略可）")
    @app_commands.choices(category=[
        app_commands.Choice(name='💻 技術ブログ', value='tech'),
        app_commands.Choice(name='📝 日常ブログ', value='daily'),
    ])
    async def random_topic(
        self, 
        interaction: Interaction,
        category: str | None = None
    ) -> None:
        channel = self.bot.get_channel(self.topic_channel_id)
        
        if not isinstance(channel, TextChannel):
            await interaction.response.send_message("お題箱チャンネルが見つかりません")
            return
        
        # チャンネルのメッセージを取得
        messages = await gather_messages(channel, category)
        
        if not messages:
            category_text = f"（{category}カテゴリ）" if category else ""
            await interaction.response.send_message(
                f"お題箱{category_text}にメッセージがありません"
            )
            return
        
        # ランダムに選択
        selected = random.choice(messages)
        
        # カテゴリを判定して表示
        categories = []
        for cat_name, emoji in CATEGORY_TO_EMOJI.items():
            if any(reaction.emoji == emoji for reaction in selected.reactions):
                categories.append(cat_name)
        
        category_display = f" [{', '.join(categories)}]" if categories else ""
        
        # 投稿者判別
        if selected.author.bot:
            message_text = f"今回のお題{category_display}: {selected.content}"
        else:
            message_text = f"今回のお題{category_display}: {selected.content}\n（提案者: {selected.author.mention}）"

        await interaction.response.send_message(message_text)

    # お題をチャンネルに投稿
    @app_commands.command(name="add_topic", description="お題箱にお題を追加します")
    @app_commands.describe(
        content="お題の内容",
        category="お題のカテゴリ"
    )
    @app_commands.choices(category=[
        app_commands.Choice(name='💻 技術ブログ', value='tech'),
        app_commands.Choice(name='📝 日常ブログ', value='daily'),
        app_commands.Choice(name='💻📝 両方', value='both'),
    ])
    async def add_topic(
        self,
        interaction: Interaction,
        content: str,
        category: str
    ) -> None:
        """お題をお題箱チャンネルに追加"""
        channel = self.bot.get_channel(self.topic_channel_id)
        
        if not isinstance(channel, TextChannel):
            await interaction.response.send_message("お題箱チャンネルが見つかりません", ephemeral=True)
            return
        
        # お題箱に投稿
        sent_message = await channel.send(
            f"{content}\n（提案者: {interaction.user.mention}）"
        )
        
        # カテゴリに応じてリアクションを追加
        if category in ('tech', 'both'):
            await sent_message.add_reaction('💻')
        if category in ('daily', 'both'):
            await sent_message.add_reaction('📝')
        
        # 完了通知（本人にだけ見える）
        await interaction.response.send_message(
            f"お題「{content}」を追加しました！", 
            ephemeral=True
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TopicBox(bot))