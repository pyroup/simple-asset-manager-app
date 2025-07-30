import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """基本設定クラス"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    DEBUG = False

class DevelopmentConfig(Config):
    """開発環境設定"""
    DEBUG = True
    # SQLiteデータベース設定
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///assets.db'

class ProductionConfig(Config):
    """本番環境設定"""
    DEBUG = False
    # Azure SQL Database設定
    DATABASE_URL = os.environ.get('DATABASE_URL')

# 環境に応じた設定を選択
def get_config():
    """環境に応じた設定を取得"""
    env = os.environ.get('FLASK_ENV', 'development')
    
    if env == 'production':
        return ProductionConfig()
    else:
        return DevelopmentConfig()

# 現在の設定
config = get_config() 