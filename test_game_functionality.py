#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify game functionality without interactive input
ゲーム機能をインタラクティブ入力なしで検証するテストスクリプト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from multilingual_quiz_game import MultilingualQuizGame, check_architecture_cost, evaluate_architecture, get_service_recommendations
from languages import get_scenarios, get_message

def test_game_initialization():
    """Test game initialization"""
    print("Testing game initialization...")
    
    game = MultilingualQuizGame()
    assert game.language == "en", "Default language should be English"
    assert game.score == 0, "Initial score should be 0"
    assert game.player_name == "", "Initial player name should be empty"
    
    print("✅ Game initialization test passed!")

def test_language_switching():
    """Test language switching functionality"""
    print("\nTesting language switching...")
    
    game = MultilingualQuizGame()
    
    # Test English
    game.language = "en"
    game._initialize_agent()
    assert game.language == "en", "Language should be set to English"
    assert game.quiz_agent is not None, "Agent should be initialized"
    
    # Test Japanese
    game.language = "ja"
    game._initialize_agent()
    assert game.language == "ja", "Language should be set to Japanese"
    assert game.quiz_agent is not None, "Agent should be initialized"
    
    print("✅ Language switching test passed!")

def test_cost_calculation():
    """Test cost calculation functionality"""
    print("\nTesting cost calculation...")
    
    services = ["EC2", "RDS", "S3", "CloudFront"]
    result = check_architecture_cost(services)
    
    assert "total_monthly_cost" in result, "Result should contain total cost"
    assert "cost_breakdown" in result, "Result should contain cost breakdown"
    assert result["total_monthly_cost"] > 0, "Total cost should be positive"
    assert len(result["cost_breakdown"]) == len(services), "Cost breakdown should match services"
    
    print(f"✅ Cost calculation test passed! Total cost: ${result['total_monthly_cost']}")

def test_architecture_evaluation():
    """Test architecture evaluation functionality"""
    print("\nTesting architecture evaluation...")
    
    # Test English evaluation
    services = ["EC2", "ALB", "Auto Scaling", "RDS", "S3", "CloudFront", "ACM"]
    result_en = evaluate_architecture(services, 1, "en")
    
    assert "score" in result_en, "Result should contain score"
    assert "grade" in result_en, "Result should contain grade"
    assert "comment" in result_en, "Result should contain comment"
    assert result_en["score"] >= 0, "Score should be non-negative"
    
    # Test Japanese evaluation
    result_ja = evaluate_architecture(services, 1, "ja")
    
    assert "score" in result_ja, "Result should contain score"
    assert "grade" in result_ja, "Result should contain grade"
    assert "comment" in result_ja, "Result should contain comment"
    assert result_ja["score"] == result_en["score"], "Scores should be identical regardless of language"
    
    print(f"✅ Architecture evaluation test passed! Score: {result_en['score']}, Grade: {result_en['grade']}")

def test_service_recommendations():
    """Test service recommendations functionality"""
    print("\nTesting service recommendations...")
    
    # Test English recommendations
    requirements_en = ["High availability", "Database", "Static content delivery"]
    result_en = get_service_recommendations(requirements_en, "en")
    
    assert len(result_en) > 0, "Should return recommendations"
    assert "High availability" in result_en, "Should contain high availability recommendations"
    
    # Test Japanese recommendations
    requirements_ja = ["高可用性", "データベース", "静的コンテンツ配信"]
    result_ja = get_service_recommendations(requirements_ja, "ja")
    
    assert len(result_ja) > 0, "Should return recommendations"
    assert "高可用性" in result_ja, "Should contain high availability recommendations"
    
    print("✅ Service recommendations test passed!")

def test_scenario_consistency():
    """Test scenario consistency across languages"""
    print("\nTesting scenario consistency...")
    
    en_scenarios = get_scenarios("en")
    ja_scenarios = get_scenarios("ja")
    
    assert len(en_scenarios) == len(ja_scenarios), "Should have same number of scenarios"
    
    for en_scenario, ja_scenario in zip(en_scenarios, ja_scenarios):
        assert en_scenario["id"] == ja_scenario["id"], "Scenario IDs should match"
        assert en_scenario["max_score"] == ja_scenario["max_score"], "Max scores should match"
        assert set(en_scenario["correct_services"]) == set(ja_scenario["correct_services"]), "Correct services should match"
    
    print("✅ Scenario consistency test passed!")

def demo_full_evaluation():
    """Demonstrate full evaluation process"""
    print("\n" + "="*60)
    print("FULL EVALUATION DEMO")
    print("="*60)
    
    # Demo scenario
    scenario = get_scenarios("en")[0]  # First scenario
    print(f"Scenario: {scenario['title']}")
    print(f"Description: {scenario['description']}")
    print(f"Requirements: {', '.join(scenario['requirements'])}")
    
    # Demo service selection
    selected_services = ["EC2", "ALB", "Auto Scaling", "RDS", "S3", "CloudFront", "ACM"]
    print(f"\nSelected services: {', '.join(selected_services)}")
    
    # Cost analysis
    cost_result = check_architecture_cost(selected_services)
    print(f"\n💰 Cost Analysis:")
    print(f"Total monthly cost: ${cost_result['total_monthly_cost']}")
    print("Cost breakdown:")
    for service, cost in cost_result['cost_breakdown'].items():
        print(f"  • {service}: ${cost}")
    
    # Architecture evaluation
    eval_result = evaluate_architecture(selected_services, scenario['id'], "en")
    print(f"\n📊 Evaluation Results:")
    print(f"Score: {eval_result['score']}/{scenario['max_score']} (Grade: {eval_result['grade']})")
    print(f"Comment: {eval_result['comment']}")
    print(f"Correct ratio: {eval_result['correct_ratio']}%")
    print(f"Correct services: {', '.join(eval_result['correct_services'])}")
    if eval_result['missed_services']:
        print(f"Missed services: {', '.join(eval_result['missed_services'])}")
    if eval_result['incorrect_services']:
        print(f"Unnecessary services: {', '.join(eval_result['incorrect_services'])}")

def main():
    """Run all tests"""
    print("🧪 Testing Multilingual Quiz Game Functionality")
    print("=" * 60)
    
    try:
        test_game_initialization()
        test_language_switching()
        test_cost_calculation()
        test_architecture_evaluation()
        test_service_recommendations()
        test_scenario_consistency()
        
        print("\n🎉 All functionality tests passed!")
        
        demo_full_evaluation()
        
        print("\n" + "="*60)
        print("✅ GAME IS READY TO USE!")
        print("Run: python multilingual_quiz_game.py")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
