# -*- coding: utf-8 -*-
import json
import random
from typing import Dict, List, Any
from strands import Agent, tool
from strands_tools import use_aws, calculator, generate_image
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

class MultilingualQuizGame:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.current_scenario = None
        self.player_name = ""
        self.language = "en"  # Default language
        self.quiz_agent = None
        
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
        
        # Initialize agent with appropriate language
        self._initialize_agent()
        return True
        
    def _initialize_agent(self):
        """Initialize the quiz agent with language-specific system prompt"""
        if self.language == "ja":
            system_prompt = """
あなたはAWSアーキテクチャ・クイズマスターです。プレイヤーがAWSアーキテクチャの問題を解決するのを支援します。

役割：
1. シナリオを分かりやすく説明する
2. プレイヤーの選択を評価し、建設的なフィードバックを提供する
3. AWSのベストプラクティスを教える
4. コスト効率と技術的な最適性のバランスを重視する

口調：
- 親しみやすく、励ましの言葉をかける
- 技術的に正確だが、初心者にも分かりやすい説明
- 間違いを指摘する際も建設的で学習につながるアドバイス

ゲームの進行：
1. シナリオの提示
2. 要件の説明
3. プレイヤーのサービス選択の受付
4. 評価とフィードバック
5. 改善提案とベストプラクティスの共有

すべての回答は日本語で行ってください。
"""
        else:
            system_prompt = """
You are an AWS Architecture Quiz Master. You help players solve AWS architecture challenges.

Your role:
1. Explain scenarios clearly and comprehensively
2. Evaluate player choices and provide constructive feedback
3. Teach AWS best practices
4. Balance cost efficiency with technical optimization

Communication style:
- Friendly and encouraging
- Technically accurate but accessible to beginners
- Constructive and educational when pointing out mistakes

Game flow:
1. Present scenarios
2. Explain requirements
3. Accept player service selections
4. Provide evaluation and feedback
5. Offer improvement suggestions and best practices

Please respond in English for all interactions.
"""
        
        self.quiz_agent = Agent(
            model="anthropic.claude-3-haiku-20240307-v1:0",
            tools=[
                check_architecture_cost,
                evaluate_architecture, 
                get_service_recommendations,
                calculator,
                generate_image
            ],
            system_prompt=system_prompt
        )
        
    def start_game(self, player_name: str):
        """Start the game with player name"""
        self.player_name = player_name
        self.score = 0
        self.level = 1
        print(get_message(self.language, "welcome_message", player_name=player_name))
        print("=" * 60)
        
    def get_scenario(self, difficulty: str = None) -> Dict:
        """Get scenario in current language"""
        scenarios = get_scenarios(self.language)
        if difficulty:
            scenarios = [s for s in scenarios if s["difficulty"] == difficulty]
        return random.choice(scenarios)

@tool
def check_architecture_cost(services: List[str], region: str = "us-east-1") -> Dict[str, Any]:
    """
    Calculate estimated monthly cost for selected AWS services configuration
    選択されたAWSサービス構成の概算月額コストを計算
    
    Args:
        services: List of selected AWS services / 選択されたAWSサービスのリスト
        region: AWS region / AWSリージョン
    
    Returns:
        Dictionary containing cost information / コスト情報を含む辞書
    """
    # Simplified cost calculation (actual Pricing API would be more complex)
    service_costs = {
        "EC2": {"t3.medium": 30.37, "m5.large": 70.08, "c5.xlarge": 156.82},
        "RDS": {"db.t3.micro": 16.79, "db.t3.small": 33.58, "db.m5.large": 140.16},
        "ALB": 22.27,
        "S3": 23.00,  # 1TB standard storage
        "CloudFront": 85.00,  # 1TB data transfer
        "Lambda": 20.00,  # 1M requests
        "DynamoDB": 25.00,  # 25 RCU/WCU
        "API Gateway": 35.00,  # 1M requests
        "EKS": 72.00,  # cluster cost
        "Kinesis": 15.00,  # 1 shard
        "Redshift": 180.00,  # dc2.large
        "SageMaker": 50.00   # ml.t3.medium
    }
    
    total_cost = 0
    cost_breakdown = {}
    
    for service in services:
        if service in service_costs:
            if isinstance(service_costs[service], dict):
                # Services with instance types like EC2, RDS
                cost = list(service_costs[service].values())[0]  # Default to smallest config
            else:
                cost = service_costs[service]
            
            cost_breakdown[service] = cost
            total_cost += cost
        else:
            cost_breakdown[service] = 0  # Unknown services cost $0
    
    return {
        "total_monthly_cost": round(total_cost, 2),
        "cost_breakdown": cost_breakdown,
        "region": region,
        "currency": "USD"
    }

@tool
def evaluate_architecture(selected_services: List[str], scenario_id: int, language: str = "en") -> Dict[str, Any]:
    """
    Evaluate selected architecture and calculate score
    選択されたアーキテクチャを評価してスコアを計算
    
    Args:
        selected_services: List of services selected by player / プレイヤーが選択したサービスのリスト
        scenario_id: Scenario ID / シナリオID
        language: Language code for localized messages / ローカライズされたメッセージの言語コード
    
    Returns:
        Evaluation results and score / 評価結果とスコア
    """
    scenarios = get_scenarios(language)
    scenario = next((s for s in scenarios if s["id"] == scenario_id), None)
    if not scenario:
        return {"error": "Invalid scenario ID"}
    
    correct_services = set(scenario["correct_services"])
    selected_services_set = set(selected_services)
    
    # Correct matches
    correct_matches = correct_services.intersection(selected_services_set)
    # Incorrect services (extra services)
    incorrect_services = selected_services_set - correct_services
    # Missed services
    missed_services = correct_services - selected_services_set
    
    # Score calculation
    base_score = scenario["max_score"]
    correct_ratio = len(correct_matches) / len(correct_services)
    penalty = len(incorrect_services) * 10  # 10 points penalty per extra service
    
    final_score = max(0, int(base_score * correct_ratio - penalty))
    
    # Generate evaluation comment
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

@tool
def get_service_recommendations(requirements: List[str], language: str = "en") -> Dict[str, List[str]]:
    """
    Provide AWS service recommendations based on requirements
    要件に基づいてAWSサービスの推奨を提供
    
    Args:
        requirements: List of requirements / 要件のリスト
        language: Language code / 言語コード
    
    Returns:
        Recommended services by category / カテゴリ別の推奨サービス
    """
    recommendations = {}
    
    # English requirement mapping
    en_requirement_mapping = {
        "High availability": ["ALB", "Auto Scaling", "Multi-AZ RDS"],
        "Auto scaling": ["Auto Scaling", "ECS", "Lambda"],
        "Database": ["RDS", "DynamoDB", "ElastiCache"],
        "Static content delivery": ["S3", "CloudFront"],
        "SSL certificate": ["ACM", "ALB"],
        "Container orchestration": ["EKS", "ECS", "Fargate"],
        "API management": ["API Gateway", "ALB"],
        "Log aggregation": ["CloudWatch Logs", "Kinesis"],
        "Metrics monitoring": ["CloudWatch", "X-Ray"],
        "Security": ["WAF", "Shield", "IAM"],
        "Streaming data processing": ["Kinesis", "MSK"],
        "Data lake": ["S3", "Lake Formation"],
        "Batch processing": ["EMR", "Batch", "Glue"],
        "Data warehouse": ["Redshift", "Athena"],
        "Visualization": ["QuickSight", "Grafana"],
        "Machine learning": ["SageMaker", "Bedrock"]
    }
    
    # Japanese requirement mapping
    ja_requirement_mapping = {
        "高可用性": ["ALB", "Auto Scaling", "Multi-AZ RDS"],
        "自動スケーリング": ["Auto Scaling", "ECS", "Lambda"],
        "データベース": ["RDS", "DynamoDB", "ElastiCache"],
        "静的コンテンツ配信": ["S3", "CloudFront"],
        "SSL証明書": ["ACM", "ALB"],
        "コンテナオーケストレーション": ["EKS", "ECS", "Fargate"],
        "API管理": ["API Gateway", "ALB"],
        "ログ集約": ["CloudWatch Logs", "Kinesis"],
        "メトリクス監視": ["CloudWatch", "X-Ray"],
        "セキュリティ": ["WAF", "Shield", "IAM"],
        "ストリーミングデータ処理": ["Kinesis", "MSK"],
        "データレイク": ["S3", "Lake Formation"],
        "バッチ処理": ["EMR", "Batch", "Glue"],
        "データウェアハウス": ["Redshift", "Athena"],
        "可視化": ["QuickSight", "Grafana"],
        "機械学習": ["SageMaker", "Bedrock"]
    }
    
    requirement_mapping = ja_requirement_mapping if language == "ja" else en_requirement_mapping
    
    for req in requirements:
        if req in requirement_mapping:
            recommendations[req] = requirement_mapping[req]
    
    return recommendations

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
    """
    Validate user input and confirm with Yes/No if there are services not in suggestions
    """
    # Create list of all available services
    all_services = []
    for services in available_services.values():
        all_services.extend(services)
    
    selected_services = [s.strip() for s in selected_input.split(",") if s.strip()]
    unknown_services = []
    
    # Check for services not in suggestions
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
    game = MultilingualQuizGame()
    
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
                message_parts = [
                    get_message(game.language, "new_challenge"),
                    "",
                    f"📊 **{get_message(game.language, 'scenario')}: {scenario['title']}**",
                    f"📝 **{get_message(game.language, 'description')}**: {scenario['description']}",
                    f"🎯 **{get_message(game.language, 'difficulty')}**: {scenario['difficulty']}",
                    f"💯 **{get_message(game.language, 'max_score')}**: {scenario['max_score']}点" if game.language == "ja" else f"💯 **{get_message(game.language, 'max_score')}**: {scenario['max_score']} points",
                    "",
                    f"**{get_message(game.language, 'requirements')}**"
                ]
                
                for req in scenario['requirements']:
                    message_parts.append(f"• {req}")
                
                if game.language == "ja":
                    message_parts.extend([
                        "",
                        "このシナリオに最適なAWSサービスを選択してください。",
                        "利用可能なサービス一覧も提示し、プレイヤーが選択しやすいようにサポートしてください。"
                    ])
                else:
                    message_parts.extend([
                        "",
                        "Please select the most appropriate AWS services for this scenario.",
                        "Please also provide a list of available services to help the player make their selection."
                    ])
                
                message = "\n".join(message_parts)
                
                # Let agent process the scenario
                response = game.quiz_agent(message)
                print(f"\n🤖 Quiz Master: {response}")
                
                # Accept player selection
                while True:
                    print(f"\n{get_message(game.language, 'select_services')}")
                    print(get_message(game.language, "service_example"))
                    print(f"{get_message(game.language, 'service_selection')}", end="", flush=True)
                    
                    selected_input = input().strip()
                    if not selected_input:
                        print(get_message(game.language, "no_services_selected"))
                        continue
                    
                    # Input validation and Yes/No confirmation
                    selected_services = validate_service_input(selected_input, AWS_SERVICES, game.language)
                    if selected_services is not None:
                        break
                
                if selected_services:
                    # Execute evaluation
                    if game.language == "ja":
                        evaluation_message = f"""
プレイヤーが以下のサービスを選択しました:
{', '.join(selected_services)}

シナリオID {scenario['id']} に対してこの選択を評価し、以下の情報を提供してください:
1. 評価結果とスコア
2. コスト分析
3. 改善提案
4. 学習ポイント

evaluate_architecture と check_architecture_cost ツールを使用して詳細な分析を行ってください。
言語コードとして 'ja' を指定してください。
"""
                    else:
                        evaluation_message = f"""
The player has selected the following services:
{', '.join(selected_services)}

Please evaluate this selection for scenario ID {scenario['id']} and provide the following information:
1. Evaluation results and score
2. Cost analysis
3. Improvement suggestions
4. Learning points

Please use the evaluate_architecture and check_architecture_cost tools for detailed analysis.
Please specify 'en' as the language code.
"""
                    
                    evaluation_response = game.quiz_agent(evaluation_message)
                    print(f"\n{get_message(game.language, 'evaluation_result')}\n{evaluation_response}")
                
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
