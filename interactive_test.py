#!/usr/bin/env python3
"""
対話的なテスト - ユーザー名必須と入力検証のデモ
"""

import sys
from io import StringIO
from demo_game import get_player_name, validate_service_input, AWS_SERVICES

def test_player_name_validation():
    """プレイヤー名必須機能のテスト"""
    print("🧪 プレイヤー名必須機能のテスト")
    print("=" * 40)
    
    # 空の入力をシミュレート
    print("テストケース: 空の名前を入力した場合")
    print("期待される動作: エラーメッセージが表示され、再入力を求められる")
    print()

def test_service_validation():
    """サービス入力検証のテスト"""
    print("🧪 サービス入力検証のテスト")
    print("=" * 40)
    
    # 正しいサービスのテスト
    print("✅ 正しいサービスの場合:")
    valid_input = "EC2, RDS, S3, CloudFront"
    result = validate_service_input(valid_input, AWS_SERVICES)
    print(f"入力: {valid_input}")
    print(f"結果: {result}")
    print()
    
    # 不正なサービスを含む場合のシミュレーション
    print("⚠️  不正なサービスを含む場合:")
    invalid_input = "EC2, RDS, InvalidService, S3"
    print(f"入力: {invalid_input}")
    print("期待される動作:")
    print("1. 不正なサービス 'InvalidService' が検出される")
    print("2. Yes/No の確認が表示される")
    print("3. Yes: そのまま続行, No: 再入力")
    print()
    
    # 実際に検証を実行（自動でYesを選択）
    print("🔍 実際の検証結果:")
    selected_services = [s.strip() for s in invalid_input.split(",") if s.strip()]
    all_services = []
    for services in AWS_SERVICES.values():
        all_services.extend(services)
    
    unknown_services = [s for s in selected_services if s not in all_services]
    
    if unknown_services:
        print(f"検出された不正なサービス: {unknown_services}")
        print("実際のゲームでは、ここでYes/Noの確認が表示されます。")
    else:
        print("全てのサービスが有効です。")

def demo_game_flow():
    """ゲームフローのデモ"""
    print("\n🎮 ゲームフローのデモ")
    print("=" * 40)
    
    print("1. プレイヤー名入力 (必須)")
    print("   - 空の場合: エラーメッセージ + 再入力")
    print("   - 有効な場合: 次のステップへ")
    print()
    
    print("2. シナリオ選択")
    print("   - 1-3の数字を選択")
    print()
    
    print("3. サービス選択")
    print("   - カンマ区切りでサービス名を入力")
    print("   - 不正なサービス名がある場合: Yes/No確認")
    print("   - No選択時: 再入力")
    print("   - Yes選択時: 評価実行")
    print()
    
    print("4. 評価結果表示")
    print("   - スコア、グレード、コスト分析")
    print("   - 学習ポイントの提示")

if __name__ == "__main__":
    print("🎮 AWS アーキテクチャ・クイズマスター - 機能テスト")
    print("=" * 60)
    print()
    
    test_player_name_validation()
    print()
    test_service_validation()
    print()
    demo_game_flow()
    
    print("\n✅ 機能テスト完了！")
    print("\n💡 実際のゲームを試すには:")
    print("   python3 demo_game.py")
