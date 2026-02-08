# Cog ガイド

Discord Bot に機能を追加するための Cog（コグ）の書き方を説明します。
Python の経験が少なくても読めるよう、各コードの意味も丁寧に解説しています。

---

## Cog とは

**Cog（コグ）** は、Bot の機能を「ファイル単位で分割する」仕組みです。

たとえば「サイコロを振る機能」と「挨拶する機能」をそれぞれ別ファイルに書けます。
`cogs/` ディレクトリに `.py` ファイルを置くだけで、Bot 起動時に自動で読み込まれます。

```
cogs/
├── dice.py      ← サイコロ機能
├── greeting.py  ← 挨拶機能
└── example.py   ← サンプル（参考用）
```

---

## 最小テンプレート

新しい Cog を作るときは、このテンプレートをコピーして使ってください。

```python
# cogs/my_feature.py  ← ファイル名は機能に合わせて変更する

from discord import Interaction, app_commands
from discord.ext import commands


class MyFeature(commands.Cog):  # ← クラス名も機能に合わせて変更する
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # ここにコマンドやイベントを書く


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MyFeature(bot))  # ← クラス名を合わせること
```

> **ポイント:** ファイル名・クラス名・`add_cog(...)` の中の名前を揃えてください。

---

## 各部の解説

Python に不慣れな方向けに、コードの各行が何を意味するか説明します。

### `from discord import ...` / `from discord.ext import commands`

discord.py ライブラリから必要な部品を読み込む宣言です。
スラッシュコマンドを書くなら `Interaction` と `app_commands` が必要です。

### `class MyFeature(commands.Cog):`

Cog の本体となる「クラス（設計図）」を定義します。
`(commands.Cog)` は「Cog の機能を引き継ぐ」という意味です。

### `def __init__(self, bot: commands.Bot) -> None:`

クラスが作られるときに一度だけ呼ばれる初期化処理です。
`self.bot = bot` で Bot 本体を保存しておくと、後でコマンドから使えます。

- **`self`** — クラス自身を指す特別な引数です。Python のクラスでは常に第一引数に書きます。

### `async def` / `await`

Discord との通信は「非同期処理」で行います。
- `async def` — 非同期関数（待ち時間がある処理）を定義するときに付けます。
- `await` — 処理が完了するまで待つ、という意味です。`async def` の中でのみ使えます。

### `async def setup(bot: commands.Bot) -> None:`

Bot がこのファイルを読み込むときに呼ばれる関数です。
**この関数がないと Cog が読み込まれません。** 必ず書いてください。

---

## スラッシュコマンドの書き方

### 引数なしのコマンド

```python
@app_commands.command(name="ping", description="Pong! と返します")
async def ping(self, interaction: Interaction) -> None:
    await interaction.response.send_message("Pong!")
```

- `@app_commands.command(...)` — この関数をスラッシュコマンドとして登録します。
- `name` — Discord 上で表示されるコマンド名（例: `/ping`）。
- `description` — コマンドの説明文。Discord の UI に表示されます。
- `interaction.response.send_message(...)` — コマンドへの返信を送ります。

### 文字列引数付きのコマンド

```python
@app_commands.command(name="hello", description="指定した名前に挨拶します")
async def hello(self, interaction: Interaction, name: str) -> None:
    await interaction.response.send_message(f"こんにちは、{name} さん！")
```

- 関数の引数に `name: str` を追加するだけで、Discord 側に入力欄が自動で現れます。
- `str`（文字列）のほか、`int`（整数）なども使えます。

### 本人のみ見えるエフェメラル応答

```python
@app_commands.command(name="secret", description="自分だけに見えるメッセージを送ります")
async def secret(self, interaction: Interaction) -> None:
    await interaction.response.send_message("これはあなただけに見えます", ephemeral=True)
```

- `ephemeral=True` を付けると、コマンドを実行した本人にしか見えないメッセージになります。

---

## イベントリスナーの書き方

コマンド以外にも、Discord 上の出来事（イベント）に反応できます。

### メッセージに反応する（`on_message`）

```python
@commands.Cog.listener()
async def on_message(self, message: discord.Message) -> None:
    # Bot 自身のメッセージには反応しない
    if message.author.bot:
        return

    if "おはよう" in message.content:
        await message.channel.send("おはようございます！")
```

- `@commands.Cog.listener()` — イベントリスナーであることを示すデコレーターです。
- `on_message` は誰かがメッセージを送ったときに呼ばれます。
- `message.author.bot` が `True` のときは Bot のメッセージなので無視します（無限ループ防止）。

> **注意:** `on_message` を使うには Bot の Intents で `message_content` が有効になっている必要があります。このリポジトリでは `main.py` で有効化済みです。

---

## よくある間違いと対処法

### `setup` 関数がない

```python
# ❌ 間違い: setup がないと Cog が読み込まれない
class MyFeature(commands.Cog):
    ...
```

```python
# ✅ 正しい: ファイルの末尾に必ず書く
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MyFeature(bot))
```

### `async`/`await` を忘れた

```python
# ❌ 間違い: Discord の処理は非同期なので async が必要
def ping(self, interaction: Interaction) -> None:
    interaction.response.send_message("Pong!")  # await も忘れずに
```

```python
# ✅ 正しい
async def ping(self, interaction: Interaction) -> None:
    await interaction.response.send_message("Pong!")
```

### スラッシュコマンドに `@app_commands.command` を付けていない

```python
# ❌ 間違い: ただのメソッドになってしまう
async def ping(self, interaction: Interaction) -> None:
    await interaction.response.send_message("Pong!")
```

```python
# ✅ 正しい: デコレーターが必要
@app_commands.command(name="ping", description="Pong! と返します")
async def ping(self, interaction: Interaction) -> None:
    await interaction.response.send_message("Pong!")
```

### `interaction.response` で応答しなかった

スラッシュコマンドは必ず `interaction.response.send_message(...)` などで応答する必要があります。
応答しないと Discord 側で「応答しませんでした」というエラーが表示されます。

---

## 参考リンク

- [discord.py 公式ドキュメント（英語）](https://discordpy.readthedocs.io/en/stable/)
- [discord.py Cog の説明](https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html)
- [app_commands の説明](https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.app_commands.Command)
- このリポジトリの [`cogs/example.py`](../cogs/example.py) — 動く最小サンプル
