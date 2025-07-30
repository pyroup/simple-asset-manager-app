# 資産管理アプリ 設計書（Azure書籍用）

## 1. システム概要
Azureの書籍でPaaSアプリ構築を学習するためのシンプルな資産管理アプリケーション。
読者がコードを一部記述して体験できるよう、最小限の構成で設計。

## 2. 技術スタック（シンプル構成）
- **フロントエンド**: HTML + CSS + JavaScript（Vanilla JS）
- **バックエンド**: Python + Flask
- **データベース**: 
  - 開発環境: SQLite
  - 本番環境: Azure SQL Database
- **デプロイ**: Azure App Service

## 3. データベース設計

### テーブル: assets
```sql
CREATE TABLE assets (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(255) NOT NULL,           -- 資産の名前
  amount DECIMAL(15,2) NOT NULL,        -- 金額
  quantity INTEGER NOT NULL DEFAULT 1,  -- 個数
  description TEXT,                     -- 説明（追加フィールド）
  category VARCHAR(100),                -- カテゴリ（現金、不動産、株式など）
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 4. 画面設計

### 4.1 資産入力画面
- 資産名入力フィールド（必須）
- 金額入力フィールド（必須）
- 個数入力フィールド（デフォルト1）
- カテゴリ選択（ドロップダウン）
- 説明入力フィールド（オプション）
- 保存ボタン

### 4.2 資産一覧画面
- 資産一覧テーブル表示
- 各資産の編集・削除機能
- 合計金額表示
- カテゴリ別集計表示

## 5. API設計（Flask）

### 5.1 資産関連API
- `GET /api/assets` - 資産一覧取得
- `POST /api/assets` - 資産登録
- `PUT /api/assets/<id>` - 資産更新
- `DELETE /api/assets/<id>` - 資産削除
- `GET /api/assets/summary` - 合計金額・カテゴリ別集計取得

## 6. プロジェクト構造
```
asset-manager-app-simple/
├── app.py                 # Flaskアプリケーション（メインファイル）
├── database.py            # データベース操作
├── static/
│   ├── css/
│   │   └── style.css      # スタイルシート
│   └── js/
│       └── app.js         # フロントエンドJavaScript
├── templates/
│   ├── index.html         # メインページ
│   └── base.html          # ベーステンプレート
├── requirements.txt       # Python依存関係
├── config.py              # 設定ファイル
└── README.md
```

## 7. 読者体験設計

### 7.1 読者が記述する部分
1. **データベース接続設定** (`config.py`)
   - SQLite接続文字列の設定
   - Azure SQL Database接続文字列の設定

2. **APIエンドポイント実装** (`app.py`)
   - 資産一覧取得API
   - 資産登録API
   - 資産更新API
   - 資産削除API

3. **フロントエンド機能** (`static/js/app.js`)
   - 資産一覧表示
   - 資産登録フォーム送信
   - 資産編集・削除機能

4. **データベース操作** (`database.py`)
   - テーブル作成
   - CRUD操作の実装

### 7.2 事前準備済み部分
- HTMLテンプレート
- CSSスタイル
- 基本的なFlaskアプリ構造
- エラーハンドリング

## 8. 学習ポイント
- Flaskアプリケーションの基本構造
- SQLiteとAzure SQL Databaseの使い分け
- RESTful APIの設計と実装
- フロントエンドとバックエンドの連携
- Azure App Serviceへのデプロイ

## 9. 開発手順
1. プロジェクト構造の作成
2. Flaskアプリケーションの基本設定
3. データベーススキーマの実装
4. APIエンドポイントの実装
5. フロントエンドの実装
6. スタイリングの適用
7. Azure App Serviceへのデプロイ 