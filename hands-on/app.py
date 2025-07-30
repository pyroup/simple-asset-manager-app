from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from config import config
from database import repository
import os

def create_app():
    """Flaskアプリケーションを作成"""
    app = Flask(__name__)
    app.config.from_object(config)
    
    # CORS設定
    CORS(app)
    
    @app.route('/')
    def index():
        """メインページ"""
        return render_template('index.html')
    
    # APIルート
    # repository.get_all()を使用してデータを取得し、jsonify()でJSONレスポンスを作成してください
    @app.route('/api/assets', methods=['GET'])
    def get_assets():
        """資産一覧取得API"""
        # TODO: 資産一覧取得APIを実装してください
    
    # request.get_json()でリクエストデータを取得し、repository.create()でデータを作成してください
    @app.route('/api/assets', methods=['POST'])
    def create_asset():
        """資産作成API"""
        # TODO: 資産作成APIを実装してください
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=config.DEBUG) 