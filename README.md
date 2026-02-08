# fedicode-discord-bot

Fedicode Discord サーバー向けの Bot 実装リポジトリです。
コミュニティメンバー全員が機能を自由に提案・実装できる共同開発モデルを採用しています。

## セットアップ

### 前提条件

- Python 3.12 以上
- [uv](https://docs.astral.sh/uv/)
- Discord Bot Token（[Discord Developer Portal](https://discord.com/developers/applications) で取得）

### 手順

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

## 機能の追加方法

Bot の機能は discord.py の [Cog](https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html) として実装します。
`cogs/` ディレクトリに Python ファイルを追加するだけで、Bot が起動時に自動で読み込みます。

詳しくは [CONTRIBUTING.md](docs/CONTRIBUTING.md) を参照してください。

## ドキュメント

- [仕様書](docs/SPECIFICATION.md)
- [コントリビューションガイド](docs/CONTRIBUTING.md)
