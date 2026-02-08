# fedicode-discord-bot 仕様書

## 概要

Fedicode Discord サーバー向けの Bot 実装リポジトリ。
コミュニティメンバー全員が機能を自由に提案・実装できる共同開発モデルを採用する。

---

## 技術スタック

| 項目 | 内容 |
|------|------|
| 言語 | Python 3.12 以上 |
| フレームワーク | discord.py 2.x |
| コマンドスタイル | スラッシュコマンド（`discord.app_commands`）ベース |
| 依存関係管理 | uv |
| 依存関係管理 | uv |
| シークレット管理 | `.env` ファイル（リポジトリには含めない） |
| Discord Intents | `default` + `message_content` + `members`（特権 Intent） |

---

## アーキテクチャ

### Cog 分割

discord.py の [Cog](https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html) 機能を用いて、機能単位でファイルを分割する。
各 Cog は独立したモジュールとして `cogs/` ディレクトリに配置し、エントリーポイント (`main.py`) が起動時にすべての Cog を読み込む。

### ディレクトリ構成

```
fedicode-discord-bot/
├── .env.example          # 必要な環境変数のテンプレート
├── .gitignore
├── README.md
├── pyproject.toml        # uv プロジェクト設定・依存関係
├── docs/
│   ├── SPECIFICATION.md  # 本仕様書
│   ├── CONTRIBUTING.md   # 貢献ガイド
│   └── cog-guide.md      # Cog の書き方ガイド
├── main.py               # エントリーポイント（Cog の読み込み・Bot 起動）
└── cogs/
    ├── __init__.py
    └── example.py        # サンプル Cog（実装の参考）
```

---

## Cog 実装ルール

**すべての Cog モジュールは以下のルールに従うこと。これが唯一の必須ルールである。**

### 必須: `setup` 関数の実装

各 Cog ファイルには、discord.py が Cog を読み込むための非同期 `setup` 関数を実装すること。

```python
# cogs/my_feature.py

from discord.ext import commands


class MyFeature(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # ... コマンドやイベントハンドラの実装 ...


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MyFeature(bot))
```

この `setup` 関数が存在しない場合、`main.py` による Cog の自動読み込みが失敗する。

---

## リポジトリ運用ルール

### ブランチ命名規則

| ブランチ | 用途 |
|----------|------|
| `main` | 本番ブランチ |
| `(user-name)/(feature-name)` | 各参加者が自由に管理するブランチ |

### ブランチ保護

- `main` ブランチへの直接 push は禁止する。
- すべての変更は Pull Request 経由でマージする。

### Pull Request

- PR の承認・マージはモデレーター（リポジトリオーナー）のみが行う。
- PR には変更の目的を簡潔に記載すること。

### 貢献の流れ

1. リポジトリを fork する（または feature ブランチを作成する）。
2. `cogs/` 以下に新しい Cog ファイルを追加する（または既存ファイルを修正する）。
3. Pull Request を作成し、変更内容を説明する。
4. モデレーターがレビュー・マージを行う。

---

## 環境変数

`.env.example` を `.env` にコピーして必要な値を設定する。

| 変数名 | 説明 |
|--------|------|
| `DISCORD_TOKEN` | Discord Bot Token |

`.env` はリポジトリに含めない（`.gitignore` で除外済み）。

---

## セットアップ手順

```bash
# リポジトリをクローン
git clone <repository-url>
cd fedicode-discord-bot

# 環境変数を設定
cp .env.example .env
# .env を編集して DISCORD_TOKEN を設定する

# 依存関係のインストール
uv sync

# Bot を起動
uv run python main.py
```

---

## 未決定事項

以下の項目は今後コミュニティで決定する。

- CI（自動テスト・lint）の導入有無
- Bot に実装する具体的な機能
