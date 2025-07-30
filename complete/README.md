# 資産管理アプリ（完成版）

このディレクトリは、読者が実装する部分をすべて埋めた完成版です。

## ファイル構成

### バックエンド
- **app.py** - 完全動作するFlaskアプリケーション
- **database.py** - 完全動作するデータベース操作（SQLite + Azure SQL Database対応）

### フロントエンド
- **static/css/style.css** - カスタムスタイルシート
- **static/js/app.js** - 完全動作するJavaScript（API通信・UI操作）
- **templates/base.html** - ベーステンプレート
- **templates/index.html** - メインページテンプレート

## 使い方

### 1. 必要なパッケージをインストール
```bash
pip install -r requirements.txt
```

### 2. データベース設定
#### SQLite（開発環境）
```bash
# デフォルトでSQLiteが使用されます
python app.py
```

#### Azure SQL Database（本番環境）
```bash
# 環境変数でAzure SQL Databaseの接続文字列を設定
set DATABASE_URL="Driver={ODBC Driver 17 for SQL Server};Server=your-server.database.windows.net;Database=your-database;UID=your-username;PWD=your-password"
python app.py
```

### 3. アプリケーションを起動
```bash
python app.py
```

### 4. ブラウザでアクセス
http://localhost:5000 にアクセス

## 機能

### 資産管理機能
- ✅ 資産の登録（名前、金額、個数、カテゴリ、説明）
- ✅ 資産の一覧表示
- ✅ 資産の編集（モーダルウィンドウ）
- ✅ 資産の削除（確認ダイアログ付き）
- ✅ 集計情報の表示（合計金額、カテゴリ別集計）

### UI/UX機能
- ✅ レスポンシブデザイン
- ✅ リアルタイム更新
- ✅ 成功・エラーメッセージ表示
- ✅ ローディング状態表示
- ✅ カテゴリ別カラーバッジ
- ✅ 金額の通貨フォーマット

### データベース機能
- ✅ SQLiteデータベース（開発環境）
- ✅ Azure SQL Database（本番環境）
- ✅ サンプルデータの自動挿入
- ✅ リポジトリパターンによる抽象化
- ✅ 自動テーブル作成

## データベース対応

### SQLite（開発環境）
- ファイルベースのデータベース
- 設定不要で即座に使用可能
- 開発・テストに最適

### Azure SQL Database（本番環境）
- クラウドベースのリレーショナルデータベース
- 高可用性とスケーラビリティ
- 本番環境での運用に最適

## 環境変数設定

### 開発環境（SQLite）
```bash
# デフォルト設定（変更不要）
DATABASE_URL=sqlite:///assets.db
```

### 本番環境（Azure SQL Database）
```bash
# Azure SQL Databaseの接続文字列
DATABASE_URL="Driver={ODBC Driver 17 for SQL Server};Server=your-server.database.windows.net;Database=your-database;UID=your-username;PWD=your-password"
```

## 注意事項

- **初回起動時**にサンプルデータが自動挿入されます
- **Azure SQL Database使用時**は、ODBC Driver 17 for SQL Serverのインストールが必要です
- **接続文字列**は適切に設定してください（セキュリティ上の理由で環境変数を使用）

## 動作確認

1. アプリケーション起動後、ブラウザで http://localhost:5000 にアクセス
2. サンプルデータ（現金、株式、不動産、預金）が表示されることを確認
3. 新しい資産を登録して動作を確認
4. 編集・削除機能をテスト
5. 集計情報の更新を確認

## 技術仕様

- **フロントエンド**: HTML5 + CSS3 + JavaScript (ES6+)
- **バックエンド**: Python 3.8+ + Flask 3.0.0
- **データベース**: SQLite / Azure SQL Database
- **UIフレームワーク**: Tailwind CSS
- **API**: RESTful API (JSON)
- **データベースドライバー**: pyodbc (Azure SQL Database用) 