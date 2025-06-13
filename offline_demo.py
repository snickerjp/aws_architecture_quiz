#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Offline demo of AWS Architecture Quiz - No AWS credentials required
AWS認証情報不要のオフラインデモ
"""

from languages import get_supported_languages, get_message, get_scenarios
from multilingual_quiz_game import check_architecture_cost, evaluate_architecture

def mock_ai_feedback(selected_services, scenario, language):
    """Mock AI feedback without using Bedrock"""
    if language == "ja":
        feedback_templates = {
            "excellent": "素晴らしい選択です！このアーキテクチャは要件を完全に満たしています。",
            "good": "良いアーキテクチャですが、いくつかの改善点があります。",
            "needs_improvement": "基本的な要件は満たしていますが、重要な要素が不足しています。"
        }
        
        suggestions = [
            "CloudWatchを追加してモニタリングを強化することを検討してください。",
            "セキュリティを向上させるためにWAFの追加を検討してください。",
            "可用性を高めるためにマルチAZ構成を検討してください。",
            "コスト最適化のためにReserved Instancesの利用を検討してください。"
        ]
    else:
        feedback_templates = {
            "excellent": "Excellent choices! This architecture fully meets the requirements.",
            "good": "Good architecture, but there are some areas for improvement.",
            "needs_improvement": "Basic requirements are met, but important elements are missing."
        }
        
        suggestions = [
            "Consider adding CloudWatch for enhanced monitoring.",
            "Consider adding WAF to improve security.",
            "Consider Multi-AZ configuration for higher availability.",
            "Consider using Reserved Instances for cost optimization."
        ]
    
    # Simple scoring logic
    correct_services = set(scenario['correct_services'])
    selected_services_set = set(selected_services)
    correct_ratio = len(correct_services.intersection(selected_services_set)) / len(correct_services)
    
    if correct_ratio >= 0.8:
        feedback = feedback_templates["excellent"]
    elif correct_ratio >= 0.6:
        feedback = feedback_templates["good"]
    else:
        feedback = feedback_templates["needs_improvement"]
    
    # Add random suggestion
    import random
    suggestion = random.choice(suggestions)
    
    return f"{feedback}\n\n💡 {get_message(language, 'requirements') if language == 'ja' else 'Suggestion'}: {suggestion}"

def offline_demo():
    """Run offline demo without AWS dependencies"""
    print("🎮 AWS Architecture Quiz Master - Offline Demo")
    print("AWS認証情報不要のオフラインデモ")
    print("=" * 60)
    print("⚠️  Note: This demo uses mock AI responses instead of Amazon Bedrock")
    print("⚠️  注意: このデモはAmazon Bedrockの代わりにモックAI応答を使用します")
    print("=" * 60)
    
    # Language selection
    print(f"\n{get_message('en', 'select_language')}")
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
    
    while True:
        # Scenario selection
        print(f"\n{get_message(language, 'available_scenarios')}")
        scenarios = get_scenarios(language)
        for i, scenario in enumerate(scenarios, 1):
            print(f"{i}. {scenario['title']} ({scenario['difficulty']})")
        
        try:
            choice = input(f"\n{get_message(language, 'select_scenario')}").strip()
            if choice.lower() in ['q', 'quit', 'exit']:
                break
                
            choice_num = int(choice)
            if 1 <= choice_num <= len(scenarios):
                scenario = scenarios[choice_num - 1]
                
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
                
                # Mock AI feedback
                print(f"\n🤖 AI Quiz Master Feedback:")
                print("-" * 40)
                ai_feedback = mock_ai_feedback(selected_services, scenario, language)
                print(ai_feedback)
                
                # Continue or exit
                print(f"\n{get_message(language, 'continue_game')}", end="")
                continue_choice = input().lower()
                if continue_choice != 'y':
                    break
                    
            else:
                print(get_message(language, "invalid_selection"))
                
        except ValueError:
            print(get_message(language, "enter_number"))
        except KeyboardInterrupt:
            print(f"\n{get_message(language, 'game_interrupted')}")
            break
    
    print(f"\n{get_message(language, 'game_end', player_name=player_name)}")
    print("\n" + "="*60)
    print("💡 To use the full AI-powered version:")
    print("   1. Set up AWS credentials (see AWS_CREDENTIALS_SETUP.md)")
    print("   2. Run: python multilingual_quiz_game.py")
    print("="*60)

if __name__ == "__main__":
    try:
        offline_demo()
    except KeyboardInterrupt:
        print("\n\nGame terminated. Thank you for playing!")
    except Exception as e:
        print(f"\nError: {e}")
        print("Please check your setup and try again.")
