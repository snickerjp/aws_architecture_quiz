#!/usr/bin/env python3
"""
クイックデモ - 新機能の動作確認
"""

from demo_game import get_player_name, validate_service_input, AWS_SERVICES

def demo_player_name():
    """プレイヤー名入力のデモ"""
    print("🎮 プレイヤー名入力デモ")
    print("=" * 30)
    print("空の名前を入力した場合の動作を確認:")
    print()
    
    # シミュレーション
    print("プレイヤー名を入力してください: [空入力]")
    print("❌ プレイヤー名は必須です。名前を入力してください。")
    print("プレイヤー名を入力してください: 田中太郎")
    print("✅ 名前が受け入れられました")
    print()

def demo_service_validation():
    """サービス検証のデモ"""
    print("🔍 サービス入力検証デモ")
    print("=" * 30)
    
    # 正常なケース
    print("✅ 正常なサービス入力:")
    valid_services = validate_service_input("EC2, RDS, S3", AWS_SERVICES)
    print(f"入力: EC2, RDS, S3")
    print(f"結果: {valid_services}")
    print()
    
    # 不正なサービスを含むケース（シミュレーション）
    print("⚠️  不正なサービスを含む場合:")
    print("入力: EC2, RDS, InvalidService")
    print("⚠️  以下のサービスは提案リストにありません:")
    print("  • InvalidService")
    print("これらのサービスを含めて続行しますか？ (Yes/No): [ユーザー入力待ち]")
    print("- Yes選択時: そのまま続行")
    print("- No選択時: 再入力を求める")
    print()

def show_available_services():
    """利用可能なサービス一覧"""
    print("📋 利用可能なAWSサービス一覧:")
    print("=" * 40)
    for category, services in AWS_SERVICES.items():
        print(f"\n🔹 {category}:")
        print(f"   {', '.join(services)}")

if __name__ == "__main__":
    print("🎮 AWS アーキテクチャ・クイズマスター - 新機能デモ")
    print("=" * 60)
    print()
    
    demo_player_name()
    demo_service_validation()
    show_available_services()
    
    print("\n" + "=" * 60)
    print("✅ 新機能の実装完了！")
    print()
    print("🚀 実際のゲームを試すには:")
    print("   python3 demo_game.py")
    print()
    print("📝 主な改善点:")
    print("   • プレイヤー名が必須入力になりました")
    print("   • 提案外サービス入力時にYes/No確認が表示されます")
    print("   • より安全で使いやすいユーザーインターフェース")
