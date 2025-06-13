#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for multilingual functionality
多言語機能のテストスクリプト
"""

from languages import get_supported_languages, get_language_config, get_message, get_scenarios

def test_language_support():
    """Test basic language support functionality"""
    print("Testing language support...")
    
    # Test supported languages
    languages = get_supported_languages()
    print(f"Supported languages: {languages}")
    assert len(languages) == 2, "Should support 2 languages"
    assert ("ja", "日本語") in languages, "Should support Japanese"
    assert ("en", "English") in languages, "Should support English"
    
    # Test language configurations
    ja_config = get_language_config("ja")
    en_config = get_language_config("en")
    
    assert ja_config["code"] == "ja", "Japanese config should have correct code"
    assert en_config["code"] == "en", "English config should have correct code"
    
    print("✅ Language support test passed!")

def test_messages():
    """Test message localization"""
    print("\nTesting message localization...")
    
    # Test Japanese messages
    ja_welcome = get_message("ja", "welcome_message", player_name="田中太郎")
    en_welcome = get_message("en", "welcome_message", player_name="John Smith")
    
    print(f"Japanese welcome: {ja_welcome}")
    print(f"English welcome: {en_welcome}")
    
    assert "田中太郎" in ja_welcome, "Japanese message should contain player name"
    assert "John Smith" in en_welcome, "English message should contain player name"
    assert "ようこそ" in ja_welcome, "Japanese message should be in Japanese"
    assert "Welcome" in en_welcome, "English message should be in English"
    
    print("✅ Message localization test passed!")

def test_scenarios():
    """Test scenario localization"""
    print("\nTesting scenario localization...")
    
    ja_scenarios = get_scenarios("ja")
    en_scenarios = get_scenarios("en")
    
    assert len(ja_scenarios) == 3, "Should have 3 Japanese scenarios"
    assert len(en_scenarios) == 3, "Should have 3 English scenarios"
    
    # Test first scenario
    ja_scenario = ja_scenarios[0]
    en_scenario = en_scenarios[0]
    
    print(f"Japanese scenario 1: {ja_scenario['title']}")
    print(f"English scenario 1: {en_scenario['title']}")
    
    assert ja_scenario["id"] == en_scenario["id"], "Scenario IDs should match"
    assert "スタートアップ" in ja_scenario["title"], "Japanese scenario should be in Japanese"
    assert "Startup" in en_scenario["title"], "English scenario should be in English"
    
    # Test requirements
    assert len(ja_scenario["requirements"]) == len(en_scenario["requirements"]), "Requirements count should match"
    
    print("✅ Scenario localization test passed!")

def test_difficulty_levels():
    """Test difficulty level translations"""
    print("\nTesting difficulty level translations...")
    
    ja_scenarios = get_scenarios("ja")
    en_scenarios = get_scenarios("en")
    
    # Check difficulty mappings
    difficulty_mapping = {
        "初級": "Beginner",
        "中級": "Intermediate", 
        "上級": "Advanced"
    }
    
    for ja_scenario, en_scenario in zip(ja_scenarios, en_scenarios):
        ja_difficulty = ja_scenario["difficulty"]
        en_difficulty = en_scenario["difficulty"]
        
        expected_en_difficulty = difficulty_mapping.get(ja_difficulty)
        assert en_difficulty == expected_en_difficulty, f"Difficulty mapping mismatch: {ja_difficulty} -> {en_difficulty} (expected {expected_en_difficulty})"
        
        print(f"Scenario {ja_scenario['id']}: {ja_difficulty} -> {en_difficulty} ✅")
    
    print("✅ Difficulty level translation test passed!")

def test_service_consistency():
    """Test that correct services are consistent across languages"""
    print("\nTesting service consistency...")
    
    ja_scenarios = get_scenarios("ja")
    en_scenarios = get_scenarios("en")
    
    for ja_scenario, en_scenario in zip(ja_scenarios, en_scenarios):
        ja_services = set(ja_scenario["correct_services"])
        en_services = set(en_scenario["correct_services"])
        
        assert ja_services == en_services, f"Services should be identical for scenario {ja_scenario['id']}"
        print(f"Scenario {ja_scenario['id']}: Services consistent ✅")
    
    print("✅ Service consistency test passed!")

def demo_multilingual_output():
    """Demonstrate multilingual output"""
    print("\n" + "="*60)
    print("MULTILINGUAL OUTPUT DEMO")
    print("="*60)
    
    # Demo Japanese
    print("\n🇯🇵 JAPANESE OUTPUT:")
    print("-" * 30)
    print(get_message("ja", "game_title"))
    print(get_message("ja", "welcome_message", player_name="田中太郎"))
    print(get_message("ja", "available_scenarios"))
    
    ja_scenarios = get_scenarios("ja")
    for i, scenario in enumerate(ja_scenarios, 1):
        print(f"{i}. {scenario['title']} ({scenario['difficulty']})")
    
    # Demo English
    print("\n🇺🇸 ENGLISH OUTPUT:")
    print("-" * 30)
    print(get_message("en", "game_title"))
    print(get_message("en", "welcome_message", player_name="John Smith"))
    print(get_message("en", "available_scenarios"))
    
    en_scenarios = get_scenarios("en")
    for i, scenario in enumerate(en_scenarios, 1):
        print(f"{i}. {scenario['title']} ({scenario['difficulty']})")

if __name__ == "__main__":
    print("🧪 Running Multilingual Functionality Tests")
    print("=" * 50)
    
    try:
        test_language_support()
        test_messages()
        test_scenarios()
        test_difficulty_levels()
        test_service_consistency()
        
        print("\n🎉 All tests passed!")
        
        demo_multilingual_output()
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise
