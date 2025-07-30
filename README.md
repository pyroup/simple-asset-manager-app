# 資産管理アプリ（Azure書籍用）

Azureの書籍でPaaSアプリ構築を学習するためのシンプルな資産管理アプリケーションです。

## 技術スタック

- **フロントエンド**: HTML + CSS + JavaScript（Vanilla JS）
- **バックエンド**: Python + Flask
- **データベース**: 
  - 開発環境: SQLite
  - 本番環境: Azure SQL Database
- **デプロイ**: Azure App Service

## 機能

- 資産の登録・編集・削除
- 資産一覧表示
- 合計金額表示
- カテゴリ別集計表示

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

開発環境用の`.env`ファイルを作成：

```env
FLASK_ENV=development
DATABASE_URL=sqlite:///assets.db
SECRET_KEY=your-secret-key
```

### 3. データベーススキーマの実装

`database.py`ファイル内のTODOコメントを参考に、以下の機能を実装してください：

- **テーブル作成**: `init_table()`メソッド
- **CRUD操作**: `get_all()`, `get_by_id()`, `create()`, `update()`, `delete()`メソッド
- **集計機能**: `get_summary()`メソッド
- **サンプルデータ**: `insert_sample_data()`メソッド

### 4. データベースのテスト

実装後、以下のコマンドでデータベースの動作を確認できます：

```bash
python test_database.py
```

### 5. APIエンドポイントの実装

`app.py`ファイル内のTODOコメントを参考に、以下のAPIを実装してください：

- **GET /api/assets**: 資産一覧取得
- **POST /api/assets**: 資産作成
- **PUT /api/assets/<id>**: 資産更新
- **DELETE /api/assets/<id>**: 資産削除
- **GET /api/assets/summary**: 集計情報取得

### 6. APIのテスト

実装後、以下のコマンドでAPIの動作を確認できます：

```bash
python test_api.py
```

### 7. フロントエンドの実装

`static/js/app.js`ファイル内のTODOコメントを参考に、以下の機能を実装してください：

- **API通信**: `fetchAssets()`, `createAsset()`, `updateAsset()`, `deleteAsset()`, `fetchSummary()`
- **UI更新**: `renderAssets()`, `renderSummary()`, `populateEditForm()`, `clearEditForm()`
- **イベント処理**: `handleAssetSubmit()`, `handleEditSubmit()`, `handleDeleteAsset()`, `handleRefresh()`
- **ユーティリティ**: `showMessage()`, `showLoading()`, `hideLoading()`

### 8. アプリケーションの起動

```bash
python app.py
```

アプリケーションは `http://localhost:5000` で起動します。

## プロジェクト構造

```
asset-manager-app-simple/
├── app.py                 # Flaskアプリケーション（メインファイル）
├── database.py            # データベース操作（リポジトリパターン）
├── config.py              # 設定ファイル
├── requirements.txt       # Python依存関係
├── test_database.py       # データベーステストスクリプト
├── test_api.py            # APIテストスクリプト
├── static/
│   ├── css/
│   │   └── style.css      # スタイルシート
│   └── js/
│       └── app.js         # フロントエンドJavaScript
├── templates/
│   ├── index.html         # メインページ
│   └── base.html          # ベーステンプレート
└── README.md
```

## データベース設計

### assetsテーブル

| カラム名 | 型 | 説明 |
|---------|----|----|
| id | INTEGER PRIMARY KEY | 主キー（自動採番） |
| name | VARCHAR(255) | 資産名（必須） |
| amount | DECIMAL(15,2) | 金額（必須） |
| quantity | INTEGER | 個数（デフォルト: 1） |
| description | TEXT | 説明（オプション） |
| category | VARCHAR(100) | カテゴリ |
| created_at | TIMESTAMP | 作成日時（自動設定） |

## API仕様

### 資産一覧取得
```
GET /api/assets
```

**レスポンス例:**
```json
[
  {
    "id": 1,
    "name": "現金",
    "amount": 500000,
    "quantity": 1,
    "description": "手元現金",
    "category": "現金",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

### 資産作成
```
POST /api/assets
```

**リクエスト例:**
```json
{
  "name": "株式",
  "amount": 1000000,
  "quantity": 100,
  "description": "A社の株式",
  "category": "株式"
}
```

**レスポンス例:**
```json
{
  "id": 2,
  "name": "株式",
  "amount": 1000000,
  "quantity": 100,
  "description": "A社の株式",
  "category": "株式",
  "created_at": "2024-01-01T00:00:00"
}
```

### 資産更新
```
PUT /api/assets/{id}
```

**リクエスト例:**
```json
{
  "amount": 1200000,
  "description": "更新された説明"
}
```

### 資産削除
```
DELETE /api/assets/{id}
```

**レスポンス例:**
```json
{
  "message": "資産を削除しました"
}
```

### 集計情報取得
```
GET /api/assets/summary
```

**レスポンス例:**
```json
{
  "total_amount": 33500000,
  "category_summary": [
    {
      "category": "現金",
      "total": 500000,
      "count": 1
    },
    {
      "category": "株式",
      "total": 100000000,
      "count": 1
    }
  ]
}
```

## UI機能

### 資産入力フォーム
- 資産名、金額、個数、カテゴリ、説明の入力
- バリデーション（必須項目チェック）
- リアルタイムフォーム検証

### 資産一覧表示
- テーブル形式での資産表示
- 金額の通貨フォーマット
- カテゴリ別カラーバッジ
- 編集・削除ボタン

### 編集モーダル
- 資産情報の編集機能
- モーダルウィンドウでの表示
- フォームの事前入力

### 集計情報
- 合計金額の表示
- カテゴリ別集計
- リアルタイム更新

## 読者向け実装箇所

以下のファイルにはTODOコメントがあり、読者が実装する部分です：

1. **`database.py`** - データベース操作の実装
   - SQLite用とAzure SQL Database用の両方を実装
   - リポジトリパターンによる抽象化
2. **`app.py`** - APIエンドポイントの実装
   - RESTful APIの設計と実装
   - バリデーションとエラーハンドリング
3. **`static/js/app.js`** - フロントエンド機能の実装
   - API通信とUI操作
   - イベントハンドリング
   - ユーティリティ関数

## 実装のヒント

### SQLiteの実装例

```python
def init_table(self):
    with self.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL,
                amount DECIMAL(15,2) NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 1,
                description TEXT,
                category VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
```

### Azure SQL Databaseの実装例

```python
def init_table(self):
    with self.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='assets' AND xtype='U')
            CREATE TABLE assets (
                id INT IDENTITY(1,1) PRIMARY KEY,
                name NVARCHAR(255) NOT NULL,
                amount DECIMAL(15,2) NOT NULL,
                quantity INT NOT NULL DEFAULT 1,
                description NVARCHAR(MAX),
                category NVARCHAR(100),
                created_at DATETIME2 DEFAULT GETDATE()
            )
        ''')
        conn.commit()
```

### APIエンドポイントの実装例

```python
@app.route('/api/assets', methods=['GET'])
def get_assets():
    try:
        assets = repository.get_all()
        return jsonify(assets), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/assets', methods=['POST'])
def create_asset():
    try:
        data = request.get_json()
        
        # バリデーション
        if not data.get('name') or not data.get('amount') or not data.get('category'):
            return jsonify({'error': '必須項目が不足しています'}), 400
        
        asset = repository.create(data)
        return jsonify(asset), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### フロントエンドの実装例

```javascript
// API通信の例
async function fetchAssets() {
    try {
        const response = await fetch(`${API_BASE_URL}/assets`);
        if (!response.ok) {
            throw new Error('資産の取得に失敗しました');
        }
        assets = await response.json();
        renderAssets();
    } catch (error) {
        showMessage(error.message, 'error');
    }
}

// UI更新の例
function renderAssets() {
    const tbody = document.getElementById('assets-tbody');
    tbody.innerHTML = '';
    
    assets.forEach(asset => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="px-4 py-2">${asset.name}</td>
            <td class="px-4 py-2 amount">${formatCurrency(asset.amount)}</td>
            <td class="px-4 py-2">${asset.quantity}</td>
            <td class="px-4 py-2">
                <span class="category-badge ${getCategoryBadgeClass(asset.category)}">
                    ${asset.category}
                </span>
            </td>
            <td class="px-4 py-2">
                <button onclick="handleEditAsset(${JSON.stringify(asset)})" 
                        class="bg-blue-500 text-white px-2 py-1 rounded text-sm mr-2">
                    編集
                </button>
                <button onclick="handleDeleteAsset(${asset.id})" 
                        class="bg-red-500 text-white px-2 py-1 rounded text-sm">
                    削除
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}
```

## テスト方法

### データベーステスト
```bash
python test_database.py
```

### APIテスト
```bash
# 別のターミナルでFlaskアプリを起動
python app.py

# 別のターミナルでAPIテストを実行
python test_api.py
```

### フロントエンドテスト
1. Flaskアプリを起動: `python app.py`
2. ブラウザで `http://localhost:5000` にアクセス
3. 資産の入力・編集・削除をテスト
4. 集計情報の表示を確認

## Azure App Serviceへのデプロイ

1. Azure CLIでログイン
2. App Serviceプランの作成
3. Webアプリの作成
4. アプリケーションのデプロイ
5. Azure SQL Databaseの設定
6. 環境変数の設定

詳細な手順は書籍内で説明します。 