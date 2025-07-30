# 資産管理アプリ（試用版・読者実装用）

このディレクトリは、読者が実装する部分（TODOコメント）が残された試用版です。
**最低限の機能（データ登録・一覧表示のみ）**に絞って設計されています。

## セットアップ

1. 依存関係をインストール
```bash
pip install -r requirements.txt
```

2. 環境変数を設定
```bash
# env.exampleをコピーして.envファイルを作成
cp env.example .env
# .envファイルを編集して必要な値を設定
```

3. アプリケーションを実行
```bash
python app.py
```

## 学習の流れ

### 1. フロントエンド実装
`static/js/app.js`のTODOコメントを実装してください：
- API通信関数（`fetchAssets()`, `createAsset()`）
- イベントハンドラー（`handleAssetSubmit()`）

### 2. バックエンドAPI実装
`app.py`のTODOコメントを実装してください：
- 資産一覧取得API（`GET /api/assets`）
- 資産作成API（`POST /api/assets`）

### 3. データベース実装
`database.py`のTODOコメントを実装してください：
- テーブル作成（`init_table()`）
- データ取得（`get_all()`）
- データ作成（`create()`）

## 実装する機能

### 必須機能
- ✅ 資産の登録（名前、金額のみ）
- ✅ 資産の一覧表示

### 削除された機能（学習負荷軽減のため）
- ❌ 資産の編集
- ❌ 資産の削除
- ❌ 集計情報の表示
- ❌ 手動更新ボタン
- ❌ サンプルデータの自動挿入

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
3. 資産登録と一覧表示をテスト

## 実装のヒント

### JavaScriptの実装例
```javascript
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

async function createAsset(assetData) {
    try {
        const response = await fetch(`${API_BASE_URL}/assets`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(assetData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || '資産の作成に失敗しました');
        }

        return await response.json();
    } catch (error) {
        throw error;
    }
}
```

### APIエンドポイントの実装例
```python
@app.route('/api/assets', methods=['GET'])
def get_assets():
    """資産一覧取得API"""
    assets = repository.get_all()
    return jsonify(assets), 200

@app.route('/api/assets', methods=['POST'])
def create_asset():
    """資産作成API"""
    data = request.get_json()
    repository.create(data)
    return jsonify({'message': '資産が作成されました'}), 201
```

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

def get_all(self) -> List[Dict]:
    with self.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM assets ORDER BY created_at DESC')
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def create(self, asset_data: Dict) -> None:
    with self.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO assets (name, amount, quantity, description, category)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            asset_data.get('name'),
            asset_data.get('amount'),
            asset_data.get('quantity', 1),
            asset_data.get('description', ''),
            asset_data.get('category', '')
        ))
        conn.commit()
```

## 完成版との違い

- **試用版**: TODOコメントが残されており、読者が実装する必要があります
- **完成版**: すべての機能が実装済みで、すぐに動作します
- **機能範囲**: 試用版は最低限の機能のみ、完成版は全機能対応

## 注意事項

- 実装に困った場合は、`complete/`ディレクトリの完成版を参考にしてください
- エラーが発生した場合は、エラーメッセージを確認してデバッグしてください
- 段階的に実装し、各段階でテストを実行することをお勧めします
- 編集・削除機能は意図的に削除されているため、実装する必要はありません 