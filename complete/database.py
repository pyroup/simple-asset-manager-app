import sqlite3
import pyodbc
from config import config
from datetime import datetime
from typing import List, Dict, Optional

class AssetRepository:
    def get_all(self) -> List[Dict]:
        raise NotImplementedError
    def get_by_id(self, asset_id: int) -> Optional[Dict]:
        raise NotImplementedError
    def create(self, asset_data: Dict) -> Dict:
        raise NotImplementedError
    def update(self, asset_id: int, asset_data: Dict) -> Optional[Dict]:
        raise NotImplementedError
    def delete(self, asset_id: int) -> bool:
        raise NotImplementedError
    def get_summary(self) -> Dict:
        raise NotImplementedError
    def insert_sample_data(self):
        raise NotImplementedError

class SQLiteAssetRepository(AssetRepository):
    def __init__(self, db_path: str = 'assets.db'):
        self.db_path = db_path
        self.init_table()
    def get_connection(self):
        return sqlite3.connect(self.db_path)
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
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM assets ORDER BY created_at DESC')
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    def get_by_id(self, asset_id: int) -> Optional[Dict]:
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM assets WHERE id = ?', (asset_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    def create(self, asset_data: Dict) -> Dict:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO assets (name, amount, quantity, description, category)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                asset_data.get('name'),
                asset_data.get('amount'),
                asset_data.get('quantity', 1),
                asset_data.get('description'),
                asset_data.get('category')
            ))
            conn.commit()
            asset_id = cursor.lastrowid
            return self.get_by_id(asset_id)
    def update(self, asset_id: int, asset_data: Dict) -> Optional[Dict]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            fields = []
            values = []
            for key in ['name', 'amount', 'quantity', 'description', 'category']:
                if key in asset_data:
                    fields.append(f"{key} = ?")
                    values.append(asset_data[key])
            if not fields:
                return self.get_by_id(asset_id)
            values.append(asset_id)
            cursor.execute(f"UPDATE assets SET {', '.join(fields)} WHERE id = ?", values)
            conn.commit()
            return self.get_by_id(asset_id)
    def delete(self, asset_id: int) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM assets WHERE id = ?', (asset_id,))
            conn.commit()
            return cursor.rowcount > 0
    def get_summary(self) -> Dict:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT SUM(amount * quantity) FROM assets')
            total_amount = cursor.fetchone()[0] or 0
            cursor.execute('SELECT category, SUM(amount * quantity) as total, COUNT(*) as count FROM assets GROUP BY category')
            category_summary = [
                {'category': row[0], 'total': row[1], 'count': row[2]}
                for row in cursor.fetchall()
            ]
            return {'total_amount': total_amount, 'category_summary': category_summary}
    def insert_sample_data(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM assets')
            cursor.executemany('''
                INSERT INTO assets (name, amount, quantity, description, category)
                VALUES (?, ?, ?, ?, ?)
            ''', [
                ('現金', 500000, 1, '手元現金', '現金'),
                ('株式', 1000000, 100, 'A社の株式', '株式'),
                ('不動産', 30000000, 1, '自宅', '不動産'),
                ('預金', 2000000, 1, '銀行預金', '預金')
            ])
            conn.commit()

class AzureSQLAssetRepository(AssetRepository):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.init_table()
    
    def get_connection(self):
        return pyodbc.connect(self.connection_string)
    
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
    
    def get_all(self) -> List[Dict]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM assets ORDER BY created_at DESC')
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]
    
    def get_by_id(self, asset_id: int) -> Optional[Dict]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM assets WHERE id = ?', (asset_id,))
            columns = [column[0] for column in cursor.description]
            row = cursor.fetchone()
            return dict(zip(columns, row)) if row else None
    
    def create(self, asset_data: Dict) -> Dict:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO assets (name, amount, quantity, description, category)
                OUTPUT INSERTED.*
                VALUES (?, ?, ?, ?, ?)
            ''', (
                asset_data.get('name'),
                asset_data.get('amount'),
                asset_data.get('quantity', 1),
                asset_data.get('description'),
                asset_data.get('category')
            ))
            columns = [column[0] for column in cursor.description]
            row = cursor.fetchone()
            conn.commit()
            return dict(zip(columns, row)) if row else None
    
    def update(self, asset_id: int, asset_data: Dict) -> Optional[Dict]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            fields = []
            values = []
            for key in ['name', 'amount', 'quantity', 'description', 'category']:
                if key in asset_data:
                    fields.append(f"{key} = ?")
                    values.append(asset_data[key])
            if not fields:
                return self.get_by_id(asset_id)
            values.append(asset_id)
            cursor.execute(f"UPDATE assets SET {', '.join(fields)} WHERE id = ?", values)
            conn.commit()
            return self.get_by_id(asset_id)
    
    def delete(self, asset_id: int) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM assets WHERE id = ?', (asset_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def get_summary(self) -> Dict:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT SUM(amount * quantity) FROM assets')
            total_amount = cursor.fetchone()[0] or 0
            cursor.execute('SELECT category, SUM(amount * quantity) as total, COUNT(*) as count FROM assets GROUP BY category')
            category_summary = [
                {'category': row[0], 'total': row[1], 'count': row[2]}
                for row in cursor.fetchall()
            ]
            return {'total_amount': total_amount, 'category_summary': category_summary}
    
    def insert_sample_data(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM assets')
            cursor.executemany('''
                INSERT INTO assets (name, amount, quantity, description, category)
                VALUES (?, ?, ?, ?, ?)
            ''', [
                ('現金', 500000, 1, '手元現金', '現金'),
                ('株式', 1000000, 100, 'A社の株式', '株式'),
                ('不動産', 30000000, 1, '自宅', '不動産'),
                ('預金', 2000000, 1, '銀行預金', '預金')
            ])
            conn.commit()

def get_repository() -> AssetRepository:
    database_url = config.DATABASE_URL
    if database_url.startswith('sqlite:///'):
        db_path = database_url.replace('sqlite:///', '')
        return SQLiteAssetRepository(db_path)
    else:
        return AzureSQLAssetRepository(database_url)

repository = get_repository()

def init_db():
    repository.init_table()
    # サンプルデータが存在しない場合のみ挿入
    try:
        assets = repository.get_all()
        if not assets:
            repository.insert_sample_data()
    except Exception as e:
        print(f"サンプルデータ挿入エラー: {e}")
        # エラーが発生してもアプリは起動する 