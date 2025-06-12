#!/usr/bin/env python3
"""
入力検証機能のテスト
"""

from demo_game import validate_service_input, AWS_SERVICES

def test_validation():
    """入力検証のテスト"""
    print("🧪 入力検証機能のテスト")
    print("=" * 40)
    
    # テストケース1: 全て正しいサービス
    print("\n📋 テスト1: 全て正しいサービス")
    test_input = "EC2, RDS, S3"
    print(f"入力: {test_input}")
    result = validate_service_input(test_input, AWS_SERVICES)
    if result:
        print(f"結果: {result}")
    
    # テストケース2: 一部不正なサービス（シミュレーション）
    print("\n📋 テスト2: 不正なサービスを含む場合")
    test_input = "EC2, RDS, InvalidService, AnotherInvalid"
    print(f"入力: {test_input}")
    print("※ 実際の実行では Yes/No の確認が表示されます")
    
    # 利用可能なサービス一覧表示
    print("\n📋 利用可能なサービス一覧:")
    for category, services in AWS_SERVICES.items():
        print(f"{category}: {', '.join(services)}")

if __name__ == "__main__":
    test_validation()
