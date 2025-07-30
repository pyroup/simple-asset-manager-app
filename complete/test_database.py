#!/usr/bin/env python3
"""
データベースの動作確認用テストスクリプト
読者が実装したデータベース操作をテストできます
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import repository, insert_sample_data

def test_database():
    """データベースの動作確認"""
    print("=== データベース動作確認 ===")
    
    try:
        # 1. サンプルデータの挿入
        print("\n1. サンプルデータを挿入中...")
        insert_sample_data()
        print("✓ サンプルデータの挿入完了")
        
        # 2. 全資産の取得
        print("\n2. 全資産を取得中...")
        assets = repository.get_all()
        print(f"✓ 取得件数: {len(assets)}件")
        for asset in assets:
            print(f"  - {asset['name']}: {asset['amount']}円 (カテゴリ: {asset['category']})")
        
        # 3. 特定の資産を取得
        if assets:
            print(f"\n3. ID {assets[0]['id']} の資産を取得中...")
            asset = repository.get_by_id(assets[0]['id'])
            if asset:
                print(f"✓ 取得成功: {asset['name']}")
            else:
                print("✗ 取得失敗")
        
        # 4. 新しい資産を作成
        print("\n4. 新しい資産を作成中...")
        new_asset_data = {
            'name': 'テスト資産',
            'amount': 100000,
            'quantity': 1,
            'description': 'テスト用の資産です',
            'category': 'その他'
        }
        created_asset = repository.create(new_asset_data)
        if created_asset:
            print(f"✓ 作成成功: ID {created_asset['id']}")
            
            # 5. 資産を更新
            print(f"\n5. ID {created_asset['id']} の資産を更新中...")
            update_data = {'amount': 150000, 'description': '更新されたテスト資産です'}
            updated_asset = repository.update(created_asset['id'], update_data)
            if updated_asset:
                print(f"✓ 更新成功: 金額 {updated_asset['amount']}円")
            else:
                print("✗ 更新失敗")
            
            # 6. 資産を削除
            print(f"\n6. ID {created_asset['id']} の資産を削除中...")
            if repository.delete(created_asset['id']):
                print("✓ 削除成功")
            else:
                print("✗ 削除失敗")
        else:
            print("✗ 作成失敗")
        
        # 7. 集計情報を取得
        print("\n7. 集計情報を取得中...")
        summary = repository.get_summary()
        print(f"✓ 合計金額: {summary['total_amount']}円")
        print("✓ カテゴリ別集計:")
        for category in summary['category_summary']:
            print(f"  - {category['category']}: {category['total']}円 ({category['count']}件)")
        
        print("\n=== すべてのテストが完了しました ===")
        
    except Exception as e:
        print(f"\n✗ エラーが発生しました: {e}")
        print("データベースの実装を確認してください。")

if __name__ == "__main__":
    test_database() 