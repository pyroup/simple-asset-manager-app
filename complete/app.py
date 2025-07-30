from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from config import config
from database import repository
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app)
    from database import init_db
    init_db()

    @app.route('/')
    def index():
        return render_template('index.html')

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
            if not data.get('name') or not data.get('amount') or not data.get('category'):
                return jsonify({'error': '必須項目が不足しています'}), 400
            asset = repository.create(data)
            return jsonify(asset), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/assets/<int:asset_id>', methods=['PUT'])
    def update_asset(asset_id):
        try:
            data = request.get_json()
            asset = repository.update(asset_id, data)
            if not asset:
                return jsonify({'error': '資産が見つかりません'}), 404
            return jsonify(asset), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/assets/<int:asset_id>', methods=['DELETE'])
    def delete_asset(asset_id):
        try:
            deleted = repository.delete(asset_id)
            if not deleted:
                return jsonify({'error': '資産が見つかりません'}), 404
            return jsonify({'message': '資産を削除しました'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/assets/summary', methods=['GET'])
    def get_summary():
        try:
            summary = repository.get_summary()
            return jsonify(summary), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=config.DEBUG) 