#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo script for multilingual AWS Architecture Quiz
多言語AWS アーキテクチャ・クイズのデモスクリプト
"""

from languages import get_supported_languages, get_message, get_scenarios

def demo_language_selection():
    """Demonstrate language selection interface"""
    print("\n" + "="*60)
    print("LANGUAGE SELECTION DEMO / 言語選択デモ")
    print("="*60)
    
    print(get_message("en", "select_language"))
    print("="*60)
    
    languages = get_supported_languages()
    for i, (code, name) in enumerate(languages, 1):
        print(f"{i}. {name} ({code})")
    
    print("\nSelect language (1-2): [Demo - selecting English]")
    print("Language selected: English")

def demo_game_flow(language="en"):
    """Demonstrate game flow in specified language"""
    print(f"\n" + "="*60)
    print(f"GAME FLOW DEMO - {language.upper()}")
    print("="*60)
    
    # Game title and welcome
    print(get_message(language, "game_title"))
    print("=" * 50)
    
    # Player name input
    player_name = "John Smith" if language == "en" else "田中太郎"
    print(f"{get_message(language, 'enter_player_name')}{player_name}")
    print(get_message(language, "welcome_message", player_name=player_name))
    print("=" * 60)
    
    # Scenario selection
    print(f"\n{get_message(language, 'available_scenarios')}")
    scenarios = get_scenarios(language)
    for i, scenario in enumerate(scenarios, 1):
        print(f"{i}. {scenario['title']} ({scenario['difficulty']})")
    
    # Demo scenario 1 selection
    print(f"\n{get_message(language, 'select_scenario')}1")
    scenario = scenarios[0]
    
    # Scenario details
    print(f"\n{get_message(language, 'new_challenge')}")
    print("")
    print(f"📊 **{get_message(language, 'scenario')}: {scenario['title']}**")
    print(f"📝 **{get_message(language, 'description')}**: {scenario['description']}")
    print(f"🎯 **{get_message(language, 'difficulty')}**: {scenario['difficulty']}")
    if language == "ja":
        print(f"💯 **{get_message(language, 'max_score')}**: {scenario['max_score']}点")
    else:
        print(f"💯 **{get_message(language, 'max_score')}**: {scenario['max_score']} points")
    print("")
    print(f"**{get_message(language, 'requirements')}**")
    for req in scenario['requirements']:
        print(f"• {req}")
    
    # Service selection demo
    print(f"\n{get_message(language, 'select_services')}")
    print(get_message(language, "service_example"))
    demo_services = "EC2, ALB, Auto Scaling, RDS, S3, CloudFront, ACM"
    print(f"{get_message(language, 'service_selection')}{demo_services}")
    
    # Evaluation demo
    print(f"\n{get_message(language, 'evaluation_result')}")
    print("🤖 Quiz Master: [Evaluation results would appear here]")
    print("Score: 85/100 (Grade: A)")
    print("Cost Analysis: $187.42/month")
    print("Correct services: 6/7")
    print("Suggestions: Consider adding CloudWatch for monitoring")
    
    # Continue game
    print(f"\n{get_message(language, 'continue_game')}n")
    print(get_message(language, "game_end", player_name=player_name))

def demo_service_validation(language="en"):
    """Demonstrate service validation feature"""
    print(f"\n" + "="*60)
    print(f"SERVICE VALIDATION DEMO - {language.upper()}")
    print("="*60)
    
    print(f"{get_message(language, 'select_services')}")
    print(get_message(language, "service_example"))
    
    # Demo with unknown service
    demo_input = "EC2, RDS, S3, CustomService, MySpecialTool"
    print(f"{get_message(language, 'service_selection')}{demo_input}")
    
    print(f"\n{get_message(language, 'unknown_services_warning')}")
    print("  • CustomService")
    print("  • MySpecialTool")
    
    print(f"\n{get_message(language, 'continue_with_unknown')}No")
    print(get_message(language, "retry_service_selection"))
    
    # Retry with valid services
    valid_input = "EC2, RDS, S3, CloudFront"
    print(f"\n{get_message(language, 'service_selection')}{valid_input}")
    print("✅ Valid services - proceeding with evaluation...")

def main():
    """Run all demos"""
    print("🎮 AWS Architecture Quiz Master - Multilingual Demo")
    print("多言語対応 AWS アーキテクチャ・クイズマスター デモ")
    
    # Language selection demo
    demo_language_selection()
    
    # English game flow
    demo_game_flow("en")
    
    # Japanese game flow
    demo_game_flow("ja")
    
    # Service validation demo
    demo_service_validation("en")
    demo_service_validation("ja")
    
    print("\n" + "="*60)
    print("DEMO COMPLETE / デモ完了")
    print("="*60)
    print("To run the actual game: python multilingual_quiz_game.py")
    print("実際のゲームを実行するには: python multilingual_quiz_game.py")

if __name__ == "__main__":
    main()
