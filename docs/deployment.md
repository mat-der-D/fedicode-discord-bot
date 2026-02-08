# デプロイ手順

Ubuntu 24.04 サーバーで Bot を自動更新しながら稼働させるためのセットアップ手順です。

## 概要

- **systemd サービス**: Bot プロセスの管理（自動起動・クラッシュ時再起動）
- **更新スクリプト**: リモートリポジトリの差分チェック → pull → 再起動
- **systemd timer**: 更新スクリプトの定期実行（5分間隔）

## 事前準備

- `uv` がインストール済みであること（パスは `which uv` で確認）
- サーバー上にリポジトリをクローン済みであること
- GitHub への接続が可能であること（SSH 鍵または HTTPS）

---

## 1. systemd サービスの作成

`/etc/systemd/system/fedicode-bot.service` を作成します。

```ini
[Unit]
Description=Fedicode Discord Bot
After=network.target

[Service]
Type=simple
User=YOUR_USER
WorkingDirectory=/path/to/fedicode-discord-bot
ExecStart=/home/YOUR_USER/.local/bin/uv run python main.py
Restart=always
RestartSec=10
EnvironmentFile=/path/to/fedicode-discord-bot/.env

[Install]
WantedBy=multi-user.target
```

`YOUR_USER` と `/path/to/fedicode-discord-bot` は実際の値に置き換えてください。

---

## 2. 更新チェックスクリプトの作成

`/usr/local/bin/update-fedicode-bot.sh` を作成します。

```bash
#!/bin/bash
set -e
REPO_DIR="/path/to/fedicode-discord-bot"
cd "$REPO_DIR"

git fetch origin main
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" != "$REMOTE" ]; then
    echo "$(date): 差分検出 → pull & 再起動"
    git pull origin main
    uv sync
    systemctl restart fedicode-bot
else
    echo "$(date): 変更なし"
fi
```

実行権限を付与します。

```bash
chmod +x /usr/local/bin/update-fedicode-bot.sh
```

---

## 3. systemd timer の作成

### サービスユニット

`/etc/systemd/system/fedicode-bot-updater.service` を作成します。

```ini
[Unit]
Description=Check fedicode-bot updates

[Service]
Type=oneshot
User=root
ExecStart=/usr/local/bin/update-fedicode-bot.sh
StandardOutput=journal
```

### タイマーユニット

`/etc/systemd/system/fedicode-bot-updater.timer` を作成します。

```ini
[Unit]
Description=Periodically check fedicode-bot updates

[Timer]
OnBootSec=1min
OnUnitActiveSec=5min

[Install]
WantedBy=timers.target
```

---

## 4. 有効化

```bash
systemctl daemon-reload
systemctl enable --now fedicode-bot.service
systemctl enable --now fedicode-bot-updater.timer
```

---

## 動作確認

```bash
# Bot の状態確認
systemctl status fedicode-bot

# Timer の確認
systemctl list-timers fedicode-bot-updater

# 更新ログ確認
journalctl -u fedicode-bot-updater -f

# Bot のログ確認
journalctl -u fedicode-bot -f
```

---

## 注意事項

- `git pull` が SSH 認証を使う場合、サービス実行ユーザーの `~/.ssh` に鍵を配置してください
- `uv` のパスは `which uv` で確認し、`ExecStart` に正確なパスを指定してください
- `.env` には機密情報が含まれるため、ファイルのパーミッションを適切に設定してください（`chmod 600 .env`）
