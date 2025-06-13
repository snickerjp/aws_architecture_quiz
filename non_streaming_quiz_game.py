# -*- coding: utf-8 -*-
"""
Non-streaming version of multilingual quiz game
ストリーミングを使用しない多言語クイズゲーム
"""

import json
import boto3
from typing import Dict, List, Any
from languages import get_supported_languages, get_language_config, get_message, get_scenarios

AWS_SERVICES = {
    "Compute": ["EC2", "Lambda", "ECS", "EKS", "Fargate", "Batch"],
    "Storage": ["S3", "EBS", "EFS", "FSx"],
    "Database": ["RDS", "DynamoDB", "ElastiCache", "Redshift", "DocumentDB"],
    "Networking": ["VPC", "ALB", "NLB", "CloudFront", "Route 53", "API Gateway"],
    "Security": ["IAM", "WAF", "Shield", "ACM", "Secrets Manager", "KMS"],
    "Monitoring": ["CloudWatch", "X-Ray", "CloudTrail", "Config"],
    "Analytics": ["Kinesis", "EMR", "Glue", "Athena", "QuickSight"],
    "ML/AI": ["SageMaker", "Bedrock", "Rekognition", "Comprehend"],
    "Management": ["CloudFormation", "Systems Manager", "Auto Scaling"]
}

class NonStreamingQuizGame:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.current_scenario = None
        self.player_name = ""
        self.language = "en"
        self.bedrock_client = None
        
    def select_language(self):
        """Language selection interface"""
        print("\n" + "=" * 60)
        print(get_message("en", "select_language"))
        print("=" * 60)
        
        languages = get_supported_languages()
        for i, (code, name) in enumerate(languages, 1):
            print(f"{i}. {name} ({code})")
        
        while True:
            try:
                print(f"\nSelect language (1-{len(languages)}): ", end="", flush=True)
                choice = int(input().strip())
                if 1 <= choice <= len(languages):
                    self.language = languages[choice - 1][0]
                    language_name = languages[choice - 1][1]
                    print(get_message(self.language, "language_selected", language=language_name))
                    break
                else:
                    print(f"Invalid selection. Please enter a number between 1-{len(languages)}.")
            except ValueError:
                print("Please enter a number.")
            except KeyboardInterrupt:
                print("\nExiting...")
                return False
        
        # Initialize Bedrock client
        self._initialize_bedrock()
        return True
        
    def _initialize_bedrock(self):
        """Initialize Bedrock client"""
        try:
            self.bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
            print("✅ Bedrock client initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize Bedrock client: {e}")
            self.bedrock_client = None
        
    def call_claude(self, message: str) -> str:
        """Call Claude model directly using Bedrock client"""
        if not self.bedrock_client:
            return "Sorry, AI assistant is not available. Please check your AWS configuration."
        
        try:
            # Try Claude 3.7 Sonnet first
            model_ids = [
                "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
                "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
                "us.anthropic.claude-3-5-sonnet-20240620-v1:0"
            ]
            
            for model_id in model_ids:
                try:
                    body = {
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": 2000,
                        "messages": [
                            {
                                "role": "user",
                                "content": message
                            }
                        ]
                    }
                    
                    response = self.bedrock_client.invoke_model(
                        modelId=model_id,
                        body=json.dumps(body)
                    )
                    
                    response_body = json.loads(response['body'].read())
                    return response_body['content'][0]['text']
                    
                except Exception as e:
                    print(f"❌ Failed with {model_id}: {str(e)}")
                    continue
            
            return "Sorry, unable to connect to AI assistant. All models failed."
            
        except Exception as e:
            return f"Error calling AI assistant: {str(e)}"
        
    def start_game(self, player_name: str):
        """Start the game with player name"""
        self.player_name = player_name
        self.score = 0
        self.level = 1
        print(get_message(self.language, "welcome_message", player_name=player_name))
        print("=" * 60)

def check_architecture_cost(services: List[str], region: str = "us-east-1") -> Dict[str, Any]:
    """Calculate estimated monthly cost for selected AWS services configuration"""
    service_costs = {
        "EC2": {"t3.medium": 30.37, "m5.large": 70.08, "c5.xlarge": 156.82},
        "RDS": {"db.t3.micro": 16.79, "db.t3.small": 33.58, "db.m5.large": 140.16},
        "ALB": 22.27,
        "S3": 23.00,
        "CloudFront": 85.00,
        "Lambda": 20.00,
        "DynamoDB": 25.00,
        "API Gateway": 35.00,
        "EKS": 72.00,
        "Kinesis": 15.00,
        "Redshift": 180.00,
        "SageMaker": 50.00
    }
    
    total_cost = 0
    cost_breakdown = {}
    
    for service in services:
        if service in service_costs:
            if isinstance(service_costs[service], dict):
                cost = list(service_costs[service].values())[0]
            else:
                cost = service_costs[service]
            cost_breakdown[service] = cost
            total_cost += cost
        else:
            cost_breakdown[service] = 0
    
    return {
        "total_monthly_cost": round(total_cost, 2),
        "cost_breakdown": cost_breakdown,
        "region": region,
        "currency": "USD"
    }

def evaluate_architecture(selected_services: List[str], scenario_id: int, language: str = "en") -> Dict[str, Any]:
    """Evaluate selected architecture and calculate score"""
    scenarios = get_scenarios(language)
    scenario = next((s for s in scenarios if s["id"] == scenario_id), None)
    if not scenario:
        return {"error": "Invalid scenario ID"}
    
    correct_services = set(scenario["correct_services"])
    selected_services_set = set(selected_services)
    
    correct_matches = correct_services.intersection(selected_services_set)
    incorrect_services = selected_services_set - correct_services
    missed_services = correct_services - selected_services_set
    
    base_score = scenario["max_score"]
    correct_ratio = len(correct_matches) / len(correct_services)
    penalty = len(incorrect_services) * 10
    
    final_score = max(0, int(base_score * correct_ratio - penalty))
    
    if correct_ratio >= 0.9:
        grade = "S"
        comment = get_message(language, "grade_s_comment")
    elif correct_ratio >= 0.7:
        grade = "A"
        comment = get_message(language, "grade_a_comment")
    elif correct_ratio >= 0.5:
        grade = "B"
        comment = get_message(language, "grade_b_comment")
    elif correct_ratio >= 0.3:
        grade = "C"
        comment = get_message(language, "grade_c_comment")
    else:
        grade = "D"
        comment = get_message(language, "grade_d_comment")
    
    return {
        "score": final_score,
        "grade": grade,
        "comment": comment,
        "correct_services": list(correct_matches),
        "incorrect_services": list(incorrect_services),
        "missed_services": list(missed_services),
        "correct_ratio": round(correct_ratio * 100, 1)
    }

def get_player_name(language):
    """Get player name as required input"""
    while True:
        print(get_message(language, "enter_player_name"), end="", flush=True)
        player_name = input().strip()
        if player_name:
            return player_name
        else:
            print(get_message(language, "player_name_required"))

def validate_service_input(selected_input, available_services, language):
    """Validate user input and confirm with Yes/No if there are services not in suggestions"""
    all_services = []
    for services in available_services.values():
        all_services.extend(services)
    
    selected_services = [s.strip() for s in selected_input.split(",") if s.strip()]
    unknown_services = []
    
    for service in selected_services:
        if service not in all_services:
            unknown_services.append(service)
    
    if unknown_services:
        print(f"\n{get_message(language, 'unknown_services_warning')}")
        for service in unknown_services:
            print(f"  • {service}")
        
        while True:
            print(f"\n{get_message(language, 'continue_with_unknown')}", end="", flush=True)
            confirm = input().strip().lower()
            if confirm in ['yes', 'y']:
                return selected_services
            elif confirm in ['no', 'n']:
                print(get_message(language, "retry_service_selection"))
                return None
            else:
                print(get_message(language, "yes_no_prompt"))
    
    return selected_services

def main():
    """Main game loop"""
    game = NonStreamingQuizGame()
    
    # Language selection
    if not game.select_language():
        return
    
    print(f"\n{get_message(game.language, 'game_title')}")
    print("=" * 50)
    
    # Get player name as required input
    player_name = get_player_name(game.language)
    game.start_game(player_name)
    
    while True:
        print(f"\n{get_message(game.language, 'available_scenarios')}")
        scenarios = get_scenarios(game.language)
        for i, scenario in enumerate(scenarios, 1):
            print(f"{i}. {scenario['title']} ({scenario['difficulty']})")
        
        try:
            print(f"\n{get_message(game.language, 'select_scenario')}", end="", flush=True)
            choice = int(input().strip())
            if 1 <= choice <= len(scenarios):
                scenario = scenarios[choice - 1]
                
                # Scenario description
                print(f"\n{get_message(game.language, 'new_challenge')}")
                print("")
                print(f"📊 **{get_message(game.language, 'scenario')}: {scenario['title']}**")
                print(f"📝 **{get_message(game.language, 'description')}**: {scenario['description']}")
                print(f"🎯 **{get_message(game.language, 'difficulty')}**: {scenario['difficulty']}")
                if game.language == "ja":
                    print(f"💯 **{get_message(game.language, 'max_score')}**: {scenario['max_score']}点")
                else:
                    print(f"💯 **{get_message(game.language, 'max_score')}**: {scenario['max_score']} points")
                print("")
                print(f"**{get_message(game.language, 'requirements')}**")
                for req in scenario['requirements']:
                    print(f"• {req}")
                
                # AI guidance
                if game.bedrock_client:
                    if game.language == "ja":
                        ai_prompt = f"""
あなたはAWSアーキテクチャの専門家です。以下のシナリオに対して、適切なAWSサービスの選択をサポートしてください。

シナリオ: {scenario['title']}
説明: {scenario['description']}
要件: {', '.join(scenario['requirements'])}

利用可能なAWSサービスカテゴリ:
{chr(10).join([f"• {category}: {', '.join(services)}" for category, services in AWS_SERVICES.items()])}

このシナリオに最適なAWSサービスを推奨し、その理由を簡潔に説明してください。
"""
                    else:
                        ai_prompt = f"""
You are an AWS architecture expert. Please help with selecting appropriate AWS services for the following scenario.

Scenario: {scenario['title']}
Description: {scenario['description']}
Requirements: {', '.join(scenario['requirements'])}

Available AWS service categories:
{chr(10).join([f"• {category}: {', '.join(services)}" for category, services in AWS_SERVICES.items()])}

Please recommend the most suitable AWS services for this scenario and briefly explain your reasoning.
"""
                    
                    print(f"\n🤖 AI Quiz Master:")
                    print("-" * 40)
                    ai_response = game.call_claude(ai_prompt)
                    print(ai_response)
                
                # Accept player selection
                while True:
                    print(f"\n{get_message(game.language, 'select_services')}")
                    print(get_message(game.language, "service_example"))
                    print(f"{get_message(game.language, 'service_selection')}", end="", flush=True)
                    
                    selected_input = input().strip()
                    if not selected_input:
                        print(get_message(game.language, "no_services_selected"))
                        continue
                    
                    selected_services = validate_service_input(selected_input, AWS_SERVICES, game.language)
                    if selected_services is not None:
                        break
                
                if selected_services:
                    # Evaluation
                    print(f"\n{get_message(game.language, 'evaluation_result')}")
                    print("=" * 40)
                    
                    # Cost analysis
                    cost_result = check_architecture_cost(selected_services)
                    print(f"💰 Cost Analysis:")
                    print(f"Total monthly cost: ${cost_result['total_monthly_cost']}")
                    print("Cost breakdown:")
                    for service, cost in cost_result['cost_breakdown'].items():
                        if cost > 0:
                            print(f"  • {service}: ${cost}")
                    
                    # Architecture evaluation
                    eval_result = evaluate_architecture(selected_services, scenario['id'], game.language)
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
                    
                    # AI feedback
                    if game.bedrock_client:
                        if game.language == "ja":
                            feedback_prompt = f"""
プレイヤーが以下のサービスを選択しました: {', '.join(selected_services)}
シナリオ: {scenario['title']}
正解サービス: {', '.join(scenario['correct_services'])}
スコア: {eval_result['score']}/{scenario['max_score']} (グレード: {eval_result['grade']})

この選択に対する建設的なフィードバックと改善提案を日本語で提供してください。
"""
                        else:
                            feedback_prompt = f"""
The player selected these services: {', '.join(selected_services)}
Scenario: {scenario['title']}
Correct services: {', '.join(scenario['correct_services'])}
Score: {eval_result['score']}/{scenario['max_score']} (Grade: {eval_result['grade']})

Please provide constructive feedback and improvement suggestions for this selection.
"""
                        
                        print(f"\n🤖 AI Feedback:")
                        print("-" * 40)
                        ai_feedback = game.call_claude(feedback_prompt)
                        print(ai_feedback)
                
                # Continue confirmation
                print(f"\n{get_message(game.language, 'continue_game')}", end="", flush=True)
                continue_game = input().lower()
                if continue_game != 'y':
                    break
            else:
                print(get_message(game.language, "invalid_selection"))
                
        except ValueError:
            print(get_message(game.language, "enter_number"))
        except KeyboardInterrupt:
            print(f"\n\n{get_message(game.language, 'game_interrupted')}")
            break
    
    print(f"\n{get_message(game.language, 'game_end', player_name=player_name)}")

if __name__ == "__main__":
    main()
