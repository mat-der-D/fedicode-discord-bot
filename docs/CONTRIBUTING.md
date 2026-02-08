# コントリビューションガイド

fedicode-discord-bot への貢献ありがとうございます。
このドキュメントでは、プロジェクトへの貢献方法を説明します。

## 貢献の流れ

1. リポジトリを fork する（またはフィーチャーブランチを作成する）。
2. `cogs/` ディレクトリに新しい Cog ファイルを追加する（または既存ファイルを修正する）。
3. Pull Request を作成し、変更内容を説明する。
4. モデレーターがレビュー・マージを行う。

## ブランチ命名規則

| ブランチ | 用途 |
|----------|------|
| `main` | 本番ブランチ（直接 push 禁止） |
| `(user-name)/(feature-name)` | 各参加者が自由に管理するブランチ |

**例:** `taro/add-dice-command`, `hanako/fix-greeting`

## ブランチ保護ルール

- `main` ブランチへの直接 push は禁止です。
- すべての変更は Pull Request 経由でマージしてください。
- PR の承認・マージはモデレーター（リポジトリオーナー）が行います。

## Cog の追加方法

Bot の機能は discord.py の Cog として実装します。
新しい機能を追加するには、`cogs/` ディレクトリに Python ファイルを作成してください。

### 必須: `setup` 関数

各 Cog ファイルには、以下の形式で `setup` 関数を実装してください。
この関数がないと Bot が Cog を読み込めません。

```python
# cogs/my_feature.py

from discord.ext import commands


class MyFeature(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # コマンドやイベントハンドラをここに実装


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MyFeature(bot))
```

### 参考

- `cogs/example.py` にサンプル実装があります。
- [discord.py Cog ドキュメント](https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html)

## 開発環境のセットアップ

```bash
git clone <your-fork-url>
cd fedicode-discord-bot
cp .env.example .env
# .env を編集して DISCORD_TOKEN を設定
uv sync
uv run python main.py
```

> **初めて Discord Bot を開発する方へ**: Bot の作成・トークン取得・テスト用サーバーへの招待など、ローカルで動かすまでの詳しい手順は [ローカルテストガイド](local-testing.md) を参照してください。
