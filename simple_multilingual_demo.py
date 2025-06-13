#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple interactive demo of multilingual quiz game
多言語クイズゲームの簡単なインタラクティブデモ
"""

from languages import get_supported_languages, get_message, get_scenarios
from multilingual_quiz_game import check_architecture_cost, evaluate_architecture

def simple_demo():
    """Simple interactive demo without Bedrock dependency"""
    print("🎮 AWS Architecture Quiz Master - Simple Demo")
    print("多言語対応 AWS アーキテクチャ・クイズマスター - 簡単デモ")
    print("=" * 60)
    
    # Language selection
    print(get_message("en", "select_language"))
    print("=" * 60)
    
    languages = get_supported_languages()
    for i, (code, name) in enumerate(languages, 1):
        print(f"{i}. {name} ({code})")
    
    while True:
        try:
            choice = input(f"\nSelect language (1-{len(languages)}): ").strip()
            choice_num = int(choice)
            if 1 <= choice_num <= len(languages):
                language = languages[choice_num - 1][0]
                language_name = languages[choice_num - 1][1]
                print(get_message(language, "language_selected", language=language_name))
                break
            else:
                print(f"Invalid selection. Please enter 1 or 2.")
        except ValueError:
            print("Please enter a number.")
        except KeyboardInterrupt:
            print("\nExiting...")
            return
    
    # Player name
    while True:
        player_name = input(f"\n{get_message(language, 'enter_player_name')}").strip()
        if player_name:
            break
        else:
            print(get_message(language, "player_name_required"))
    
    print(f"\n{get_message(language, 'welcome_message', player_name=player_name)}")
    print("=" * 60)
    
    # Scenario selection
    print(f"\n{get_message(language, 'available_scenarios')}")
    scenarios = get_scenarios(language)
    for i, scenario in enumerate(scenarios, 1):
        print(f"{i}. {scenario['title']} ({scenario['difficulty']})")
    
    while True:
        try:
            choice = input(f"\n{get_message(language, 'select_scenario')}").strip()
            choice_num = int(choice)
            if 1 <= choice_num <= len(scenarios):
                scenario = scenarios[choice_num - 1]
                break
            else:
                print(get_message(language, "invalid_selection"))
        except ValueError:
            print(get_message(language, "enter_number"))
        except KeyboardInterrupt:
            print(f"\n{get_message(language, 'game_interrupted')}")
            return
    
    # Display scenario
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
    
    # Service selection
    print(f"\n{get_message(language, 'select_services')}")
    print(get_message(language, "service_example"))
    
    while True:
        selected_input = input(f"{get_message(language, 'service_selection')}").strip()
        if selected_input:
            break
        else:
            print(get_message(language, "no_services_selected"))
    
    selected_services = [s.strip() for s in selected_input.split(",") if s.strip()]
    
    # Evaluation
    print(f"\n{get_message(language, 'evaluation_result')}")
    print("=" * 40)
    
    # Cost analysis
    try:
        cost_result = check_architecture_cost(selected_services)
        print(f"💰 Cost Analysis:")
        print(f"Total monthly cost: ${cost_result['total_monthly_cost']}")
        print("Cost breakdown:")
        for service, cost in cost_result['cost_breakdown'].items():
            if cost > 0:
                print(f"  • {service}: ${cost}")
    except Exception as e:
        print(f"Cost analysis error: {e}")
    
    # Architecture evaluation
    try:
        eval_result = evaluate_architecture(selected_services, scenario['id'], language)
        print(f"\n📊 Architecture Evaluation:")
        print(f"Score: {eval_result['score']}/{scenario['max_score']} (Grade: {eval_result['grade']})")
        print(f"Comment: {eval_result['comment']}")
        print(f"Correct ratio: {eval_result['correct_ratio']}%")
        
        if eval_result['correct_services']:
            print(f"✅ Correct services: {', '.join(eval_result['correct_services'])}")
        if eval_result['missed_services']:
            print(f"❌ Missed services: {', '.join(eval_result['missed_services'])}")
        if eval_result['incorrect_services']:
            print(f"⚠️  Unnecessary services: {', '.join(eval_result['incorrect_services'])}")
            
    except Exception as e:
        print(f"Evaluation error: {e}")
    
    # End game
    print(f"\n{get_message(language, 'game_end', player_name=player_name)}")

if __name__ == "__main__":
    try:
        simple_demo()
    except KeyboardInterrupt:
        print("\n\nGame terminated. Thank you for playing!")
    except Exception as e:
        print(f"\nError: {e}")
        print("Please check your setup and try again.")
