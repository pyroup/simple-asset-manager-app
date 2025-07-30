#!/usr/bin/env python3
"""
APIエンドポイントの動作確認用テストスクリプト
読者が実装したAPIをテストできます
"""

import requests
import json
import time

# APIのベースURL
BASE_URL = "http://localhost:5000/api"

def test_api():
    """APIエンドポイントの動作確認"""
    print("=== APIエンドポイント動作確認 ===")
    
    try:
        # 1. 資産一覧取得API
        print("\n1. 資産一覧取得APIをテスト中...")
        response = requests.get(f"{BASE_URL}/assets")
        if response.status_code == 200:
            assets = response.json()
            print(f"✓ 取得成功: {len(assets)}件の資産")
            for asset in assets:
                print(f"  - {asset['name']}: {asset['amount']}円")
        else:
            print(f"✗ 取得失敗: {response.status_code}")
            return
        
        # 2. 新しい資産作成API
        print("\n2. 資産作成APIをテスト中...")
        new_asset = {
            "name": "テスト資産",
            "amount": 100000,
            "quantity": 1,
            "description": "APIテスト用の資産です",
            "category": "その他"
        }
        response = requests.post(f"{BASE_URL}/assets", json=new_asset)
        if response.status_code == 201:
            created_asset = response.json()
            print(f"✓ 作成成功: ID {created_asset['id']}")
            asset_id = created_asset['id']
        else:
            print(f"✗ 作成失敗: {response.status_code}")
            print(f"  エラー: {response.text}")
            return
        
        # 3. 特定の資産取得API
        print(f"\n3. 資産取得API（ID: {asset_id}）をテスト中...")
        response = requests.get(f"{BASE_URL}/assets/{asset_id}")
        if response.status_code == 200:
            asset = response.json()
            print(f"✓ 取得成功: {asset['name']}")
        else:
            print(f"✗ 取得失敗: {response.status_code}")
        
        # 4. 資産更新API
        print(f"\n4. 資産更新API（ID: {asset_id}）をテスト中...")
        update_data = {
            "amount": 150000,
            "description": "更新されたテスト資産です"
        }
        response = requests.put(f"{BASE_URL}/assets/{asset_id}", json=update_data)
        if response.status_code == 200:
            updated_asset = response.json()
            print(f"✓ 更新成功: 金額 {updated_asset['amount']}円")
        else:
            print(f"✗ 更新失敗: {response.status_code}")
            print(f"  エラー: {response.text}")
        
        # 5. 集計情報取得API
        print("\n5. 集計情報取得APIをテスト中...")
        response = requests.get(f"{BASE_URL}/assets/summary")
        if response.status_code == 200:
            summary = response.json()
            print(f"✓ 取得成功: 合計金額 {summary['total_amount']}円")
            print("  カテゴリ別集計:")
            for category in summary['category_summary']:
                print(f"    - {category['category']}: {category['total']}円 ({category['count']}件)")
        else:
            print(f"✗ 取得失敗: {response.status_code}")
        
        # 6. 資産削除API
        print(f"\n6. 資産削除API（ID: {asset_id}）をテスト中...")
        response = requests.delete(f"{BASE_URL}/assets/{asset_id}")
        if response.status_code == 200:
            print("✓ 削除成功")
        else:
            print(f"✗ 削除失敗: {response.status_code}")
            print(f"  エラー: {response.text}")
        
        # 7. 削除後の確認
        print(f"\n7. 削除後の確認（ID: {asset_id}）...")
        response = requests.get(f"{BASE_URL}/assets/{asset_id}")
        if response.status_code == 404:
            print("✓ 削除確認成功（404エラー）")
        else:
            print(f"✗ 削除確認失敗: {response.status_code}")
        
        print("\n=== すべてのAPIテストが完了しました ===")
        
    except requests.exceptions.ConnectionError:
        print("\n✗ Flaskアプリケーションが起動していません。")
        print("python app.py でアプリケーションを起動してから再実行してください。")
    except Exception as e:
        print(f"\n✗ エラーが発生しました: {e}")

def test_validation():
    """バリデーションテスト"""
    print("\n=== バリデーションテスト ===")
    
    # 必須項目が不足している場合のテスト
    print("\n1. 必須項目不足のテスト...")
    invalid_asset = {
        "amount": 100000,
        "quantity": 1
        # nameとcategoryが不足
    }
    response = requests.post(f"{BASE_URL}/assets", json=invalid_asset)
    if response.status_code == 400:
        print("✓ バリデーション成功（400エラー）")
    else:
        print(f"✗ バリデーション失敗: {response.status_code}")
    
    # 存在しないIDでの更新テスト
    print("\n2. 存在しないIDでの更新テスト...")
    response = requests.put(f"{BASE_URL}/assets/99999", json={"name": "テスト"})
    if response.status_code == 404:
        print("✓ 404エラーハンドリング成功")
    else:
        print(f"✗ 404エラーハンドリング失敗: {response.status_code}")

if __name__ == "__main__":
    print("Flaskアプリケーションが起動していることを確認してください。")
    print("起動していない場合は、別のターミナルで 'python app.py' を実行してください。")
    print("5秒後にテストを開始します...")
    time.sleep(5)
    
    test_api()
    test_validation() 