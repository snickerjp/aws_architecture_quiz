#!/usr/bin/env python3
"""
プロンプト表示のテスト
"""

import sys

def test_prompt_display():
    """プロンプト表示のテスト"""
    print("🧪 プロンプト表示テスト")
    print("=" * 30)
    
    # 方法1: sys.stdout.write + flush
    print("\n方法1: sys.stdout.write + flush")
    sys.stdout.write("名前を入力してください (方法1): ")
    sys.stdout.flush()
    name1 = input()
    print(f"入力された名前: {name1}")
    
    # 方法2: print with end="" + flush
    print("\n方法2: print with end='' + flush")
    print("名前を入力してください (方法2): ", end="", flush=True)
    name2 = input()
    print(f"入力された名前: {name2}")
    
    # 方法3: 通常のinput()
    print("\n方法3: 通常のinput()")
    name3 = input("名前を入力してください (方法3): ")
    print(f"入力された名前: {name3}")

if __name__ == "__main__":
    test_prompt_display()
    print("\n✅ テスト完了")
