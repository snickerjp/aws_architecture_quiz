import json
import random
from typing import Dict, List, Any
from strands import Agent, tool
from strands_tools import use_aws, calculator, generate_image

# ゲームデータ
SCENARIOS = [
    {
        "id": 1,
        "title": "スタートアップのWebアプリケーション",
        "description": "月間10万PVのWebアプリケーションを構築したい。コスト効率と拡張性を重視。",
        "requirements": [
            "高可用性",
            "自動スケーリング", 
            "データベース",
            "静的コンテンツ配信",
            "SSL証明書"
        ],
        "correct_services": [
            "EC2", "ALB", "Auto Scaling", "RDS", "S3", "CloudFront", "ACM"
        ],
        "difficulty": "初級",
        "max_score": 100
    },
    {
        "id": 2,
        "title": "エンタープライズのマイクロサービス",
        "description": "大規模なマイクロサービスアーキテクチャを構築。セキュリティとモニタリングが重要。",
        "requirements": [
            "コンテナオーケストレーション",
            "サービスメッシュ",
            "API管理",
            "ログ集約",
            "メトリクス監視",
            "セキュリティ"
        ],
        "correct_services": [
            "EKS", "App Mesh", "API Gateway", "CloudWatch", "X-Ray", "WAF", "Secrets Manager"
        ],
        "difficulty": "上級",
        "max_score": 200
    },
    {
        "id": 3,
        "title": "データ分析プラットフォーム",
        "description": "リアルタイムデータ処理とバッチ処理を組み合わせた分析基盤を構築。",
        "requirements": [
            "ストリーミングデータ処理",
            "データレイク",
            "バッチ処理",
            "データウェアハウス",
            "可視化",
            "機械学習"
        ],
        "correct_services": [
            "Kinesis", "S3", "EMR", "Redshift", "QuickSight", "SageMaker", "Glue"
        ],
        "difficulty": "中級",
        "max_score": 150
    }
]

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

class QuizGame:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.current_scenario = None
        self.player_name = ""
        
    def start_game(self, player_name: str):
        self.player_name = player_name
        self.score = 0
        self.level = 1
        print(f"🎮 AWS アーキテクチャ・クイズマスターへようこそ、{player_name}さん！")
        print("=" * 60)
        
    def get_scenario(self, difficulty: str = None) -> Dict:
        if difficulty:
            scenarios = [s for s in SCENARIOS if s["difficulty"] == difficulty]
        else:
            scenarios = SCENARIOS
        return random.choice(scenarios)

@tool
def check_architecture_cost(services: List[str], region: str = "us-east-1") -> Dict[str, Any]:
    """
    選択されたAWSサービス構成の概算月額コストを計算
    
    Args:
        services: 選択されたAWSサービスのリスト
        region: AWSリージョン
    
    Returns:
        コスト情報を含む辞書
    """
    # 簡易的なコスト計算（実際のPricing APIを使用する場合はより複雑になります）
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
                # EC2やRDSなど、インスタンスタイプがあるサービス
                cost = list(service_costs[service].values())[0]  # デフォルトで最小構成
            else:
                cost = service_costs[service]
            
            cost_breakdown[service] = cost
            total_cost += cost
        else:
            cost_breakdown[service] = 0  # 未知のサービスは0円
    
    return {
        "total_monthly_cost": round(total_cost, 2),
        "cost_breakdown": cost_breakdown,
        "region": region,
        "currency": "USD"
    }

@tool
def evaluate_architecture(selected_services: List[str], scenario_id: int) -> Dict[str, Any]:
    """
    選択されたアーキテクチャを評価してスコアを計算
    
    Args:
        selected_services: プレイヤーが選択したサービスのリスト
        scenario_id: シナリオID
    
    Returns:
        評価結果とスコア
    """
    scenario = next((s for s in SCENARIOS if s["id"] == scenario_id), None)
    if not scenario:
        return {"error": "Invalid scenario ID"}
    
    correct_services = set(scenario["correct_services"])
    selected_services_set = set(selected_services)
    
    # 正解したサービス
    correct_matches = correct_services.intersection(selected_services_set)
    # 不正解（余分なサービス）
    incorrect_services = selected_services_set - correct_services
    # 見逃したサービス
    missed_services = correct_services - selected_services_set
    
    # スコア計算
    base_score = scenario["max_score"]
    correct_ratio = len(correct_matches) / len(correct_services)
    penalty = len(incorrect_services) * 10  # 余分なサービス1つにつき10点減点
    
    final_score = max(0, int(base_score * correct_ratio - penalty))
    
    # 評価コメント生成
    if correct_ratio >= 0.9:
        grade = "S"
        comment = "素晴らしい！完璧に近いアーキテクチャです。"
    elif correct_ratio >= 0.7:
        grade = "A"
        comment = "とても良いアーキテクチャです。"
    elif correct_ratio >= 0.5:
        grade = "B"
        comment = "良いアーキテクチャですが、改善の余地があります。"
    elif correct_ratio >= 0.3:
        grade = "C"
        comment = "基本的な要件は満たしていますが、重要な要素が不足しています。"
    else:
        grade = "D"
        comment = "アーキテクチャの見直しが必要です。"
    
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
def get_service_recommendations(requirements: List[str]) -> Dict[str, List[str]]:
    """
    要件に基づいてAWSサービスの推奨を提供
    
    Args:
        requirements: 要件のリスト
    
    Returns:
        カテゴリ別の推奨サービス
    """
    recommendations = {}
    
    requirement_mapping = {
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
    
    for req in requirements:
        if req in requirement_mapping:
            recommendations[req] = requirement_mapping[req]
    
    return recommendations

# エージェントの作成
quiz_agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[
        check_architecture_cost,
        evaluate_architecture, 
        get_service_recommendations,
        calculator,
        generate_image
    ],
    system_prompt="""
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
"""
)

def get_player_name():
    """プレイヤー名を必須入力として取得"""
    while True:
        print("プレイヤー名を入力してください: ", end="", flush=True)
        player_name = input().strip()
        if player_name:
            return player_name
        else:
            print("❌ プレイヤー名は必須です。名前を入力してください。")

def validate_service_input(selected_input, available_services):
    """
    ユーザーの入力を検証し、提案以外のサービスがある場合はYes/Noで確認
    """
    # 全ての利用可能なサービスのリストを作成
    all_services = []
    for services in available_services.values():
        all_services.extend(services)
    
    selected_services = [s.strip() for s in selected_input.split(",") if s.strip()]
    unknown_services = []
    
    # 提案にないサービスをチェック
    for service in selected_services:
        if service not in all_services:
            unknown_services.append(service)
    
    if unknown_services:
        print(f"\n⚠️  以下のサービスは提案リストにありません:")
        for service in unknown_services:
            print(f"  • {service}")
        
        while True:
            print(f"\nこれらのサービスを含めて続行しますか？ (Yes/No): ", end="", flush=True)
            confirm = input().strip().lower()
            if confirm in ['yes', 'y']:
                return selected_services
            elif confirm in ['no', 'n']:
                print("サービス選択をやり直してください。")
                return None
            else:
                print("❌ 'Yes' または 'No' で答えてください。")
    
    return selected_services

def main():
    """メインゲームループ"""
    game = QuizGame()
    
    print("🎮 AWS アーキテクチャ・クイズマスター")
    print("=" * 50)
    
    # プレイヤー名を必須入力として取得
    player_name = get_player_name()
    game.start_game(player_name)
    
    while True:
        print("\n📋 利用可能なシナリオ:")
        for i, scenario in enumerate(SCENARIOS, 1):
            print(f"{i}. {scenario['title']} ({scenario['difficulty']})")
        
        try:
            print(f"\nシナリオを選択してください (1-3): ", end="", flush=True)
            choice = int(input().strip())
            if 1 <= choice <= len(SCENARIOS):
                scenario = SCENARIOS[choice - 1]
                
                # シナリオの説明
                message = f"""
新しいチャレンジを開始します！

📊 **シナリオ: {scenario['title']}**
📝 **説明**: {scenario['description']}
🎯 **難易度**: {scenario['difficulty']}
💯 **最大スコア**: {scenario['max_score']}点

**要件:**
{chr(10).join(f"• {req}" for req in scenario['requirements'])}

このシナリオに最適なAWSサービスを選択してください。
利用可能なサービス一覧も提示し、プレイヤーが選択しやすいようにサポートしてください。
"""
                
                # エージェントにシナリオを処理させる
                response = quiz_agent(message)
                print(f"\n🤖 クイズマスター: {response}")
                
                # プレイヤーの選択を受付
                while True:
                    print("\n選択したサービスをカンマ区切りで入力してください:")
                    print("例: EC2, RDS, S3, CloudFront")
                    print("選択: ", end="", flush=True)
                    
                    selected_input = input().strip()
                    if not selected_input:
                        print("❌ サービスが選択されていません。")
                        continue
                    
                    # 入力検証とYes/No確認
                    selected_services = validate_service_input(selected_input, AWS_SERVICES)
                    if selected_services is not None:
                        break
                
                if selected_services:
                    # 評価を実行
                    evaluation_message = f"""
プレイヤーが以下のサービスを選択しました:
{', '.join(selected_services)}

シナリオID {scenario['id']} に対してこの選択を評価し、以下の情報を提供してください:
1. 評価結果とスコア
2. コスト分析
3. 改善提案
4. 学習ポイント

evaluate_architecture と check_architecture_cost ツールを使用して詳細な分析を行ってください。
"""
                    
                    evaluation_response = quiz_agent(evaluation_message)
                    print(f"\n📊 評価結果:\n{evaluation_response}")
                
                # 続行確認
                print("\n別のシナリオに挑戦しますか？ (y/n): ", end="", flush=True)
                continue_game = input().lower()
                if continue_game != 'y':
                    break
            else:
                print("無効な選択です。1-3の数字を入力してください。")
                
        except ValueError:
            print("数字を入力してください。")
        except KeyboardInterrupt:
            print("\n\nゲームを終了します。お疲れさまでした！")
            break
    
    print(f"\n🎉 ゲーム終了！{player_name}さん、お疲れさまでした！")

if __name__ == "__main__":
    main()
