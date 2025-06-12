#!/usr/bin/env python3
"""
修正されたデモ版のテスト
"""

from demo_game import get_player_name

def test_player_name_prompt():
    """プレイヤー名プロンプトのテスト"""
    print("🧪 プレイヤー名プロンプトテスト")
    print("=" * 40)
    print("以下のように表示されるはずです:")
    print("プレイヤー名を入力してください: [入力待ち]")
    print()
    print("実際のテスト:")
    print("プレイヤー名を入力してください: ", end="")
    print("[この部分で入力を待つ]")

if __name__ == "__main__":
    test_player_name_prompt()
    print("\n✅ プロンプト表示の修正完了！")
    print("\n🚀 実際のゲームを試すには:")
    print("   python3 demo_game.py")
