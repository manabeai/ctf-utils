# Request Logger

CTF用のFlaskベースリクエストロガー。全ての受信リクエストの詳細情報をログに記録します。

## セットアップ

```bash
# uvをインストール（未インストールの場合）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 依存関係をインストール
uv sync
```

## 使用方法

```bash
# サーバー起動
uv run python request_logger.py
```

デフォルトでポート5000で起動します。

## ログ内容

以下の情報が`requests.log`とコンソールに記録されます：

- タイムスタンプ
- HTTPメソッド、URL、パス
- リモートアドレス
- 全てのヘッダー
- クエリパラメータ
- フォームデータ
- JSONペイロード
- 生のリクエストボディ
- Cookie
- User-Agent
- リファラー
- その他のメタデータ（スキーム、ホスト、Content-Type等）

## 例

```bash
# GET リクエスト
curl http://localhost:5000/test?param=value

# POST リクエスト（JSON）
curl -X POST http://localhost:5000/api/data \
  -H "Content-Type: application/json" \
  -d '{"key":"value"}'

# POST リクエスト（フォーム）
curl -X POST http://localhost:5000/form \
  -d "username=admin&password=secret"
```