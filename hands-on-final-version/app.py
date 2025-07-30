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
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=config.DEBUG) 