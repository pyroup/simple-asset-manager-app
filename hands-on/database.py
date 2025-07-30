import sqlite3
import pyodbc
from config import config
from datetime import datetime
from typing import List, Dict, Optional

class AssetRepository:
    """資産リポジトリの抽象クラス"""
    
    def get_connection(self):
        """データベース接続を取得"""
        raise NotImplementedError
    
    def init_table(self):
        """テーブルを初期化"""
        raise NotImplementedError
    
    def get_all(self) -> List[Dict]:
        """全資産を取得"""
        raise NotImplementedError
    
    def create(self, asset_data: Dict) -> None:
        """資産を作成"""
        raise NotImplementedError

class SQLiteAssetRepository(AssetRepository):
    """SQLite用資産リポジトリ"""
    
    def __init__(self, db_path: str = 'assets.db'):
        self.db_path = db_path
        self.init_table()
    
    def get_connection(self):
        """データベース接続を取得"""
        return sqlite3.connect(self.db_path)
    
    # 必要なカラム: id, name, amount, quantity, description, category, created_at
    # CREATE TABLE IF NOT EXISTSを使用してください
    def init_table(self):
        """テーブルを初期化"""
        # TODO: assetsテーブルを作成するSQLを実装してください
    
    # SELECT文で全カラムを取得し、辞書のリストとして返してください
    def get_all(self) -> List[Dict]:
        """全資産を取得"""
        # TODO: 全資産を取得するSQLを実装してください

    # INSERT文でデータを挿入してください
    def create(self, asset_data: Dict) -> None:
        """資産を作成"""
        # TODO: 資産を作成するSQLを実装してください

class AzureSQLAssetRepository(AssetRepository):
    """Azure SQL Database用資産リポジトリ"""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.init_table()
    
    def get_connection(self):
        """データベース接続を取得"""
        return pyodbc.connect(self.connection_string)
    
    def init_table(self):
        """テーブルを初期化"""
        # TODO: 読者が実装する部分
        # Azure SQL Database用のassetsテーブルを作成するSQLを記述してください
        # SQLiteと同様のカラム構成にしてください
        pass
    
    def get_all(self) -> List[Dict]:
        """全資産を取得"""
        # TODO: 読者が実装する部分
        # Azure SQL Database用の全資産取得SQLを記述してください
        pass
    
    def create(self, asset_data: Dict) -> None:
        """資産を作成"""
        # TODO: 読者が実装する部分
        # Azure SQL Database用の資産作成SQLを記述してください
        pass

# リポジトリインスタンス
def get_repository() -> AssetRepository:
    """環境に応じたリポジトリを取得"""
    database_url = config.DATABASE_URL
    
    if database_url.startswith('sqlite:///'):
        # SQLiteの場合
        db_path = database_url.replace('sqlite:///', '')
        return SQLiteAssetRepository(db_path)
    else:
        # Azure SQL Databaseの場合
        return AzureSQLAssetRepository(database_url)

# グローバルリポジトリインスタンス
repository = get_repository()