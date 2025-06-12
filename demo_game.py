#!/usr/bin/env python3
"""
AWS アーキテクチャ・クイズマスター - デモ版
Strands Agent なしで動作する簡易版
"""

import json
import random
from typing import Dict, List, Any

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

def check_architecture_cost(services: List[str], region: str = "us-east-1") -> Dict[str, Any]:
    """選択されたAWSサービス構成の概算月額コストを計算"""
    service_costs = {
        "EC2": 30.37,  # t3.medium
        "RDS": 33.58,  # db.t3.small
        "ALB": 22.27,
        "S3": 23.00,
        "CloudFront": 85.00,
        "Lambda": 20.00,
        "DynamoDB": 25.00,
        "API Gateway": 35.00,
        "EKS": 72.00,
        "Kinesis": 15.00,
        "Redshift": 180.00,
        "SageMaker": 50.00,
        "Auto Scaling": 0.00,  # 無料
        "ACM": 0.00,  # 無料
        "WAF": 5.00,
        "CloudWatch": 10.00,
        "X-Ray": 5.00,
        "EMR": 100.00,
        "Glue": 44.00,
        "QuickSight": 18.00,
        "App Mesh": 0.00,
        "Secrets Manager": 0.40
    }
    
    total_cost = 0
    cost_breakdown = {}
    
    for service in services:
        cost = service_costs.get(service, 0)
        cost_breakdown[service] = cost
        total_cost += cost
    
    return {
        "total_monthly_cost": round(total_cost, 2),
        "cost_breakdown": cost_breakdown,
        "region": region,
        "currency": "USD"
    }

def evaluate_architecture(selected_services: List[str], scenario_id: int) -> Dict[str, Any]:
    """選択されたアーキテクチャを評価してスコアを計算"""
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
    correct_ratio = len(correct_matches) / len(correct_services) if correct_services else 0
    penalty = len(incorrect_services) * 10
    
    final_score = max(0, int(base_score * correct_ratio - penalty))
    
    # 評価コメント生成
    if correct_ratio >= 0.9:
        grade = "S"
        comment = "🌟 素晴らしい！完璧に近いアーキテクチャです。"
    elif correct_ratio >= 0.7:
        grade = "A"
        comment = "👏 とても良いアーキテクチャです。"
    elif correct_ratio >= 0.5:
        grade = "B"
        comment = "👍 良いアーキテクチャですが、改善の余地があります。"
    elif correct_ratio >= 0.3:
        grade = "C"
        comment = "📚 基本的な要件は満たしていますが、重要な要素が不足しています。"
    else:
        grade = "D"
        comment = "🔄 アーキテクチャの見直しが必要です。"
    
    return {
        "score": final_score,
        "grade": grade,
        "comment": comment,
        "correct_services": list(correct_matches),
        "incorrect_services": list(incorrect_services),
        "missed_services": list(missed_services),
        "correct_ratio": round(correct_ratio * 100, 1)
    }

def get_service_recommendations(requirements: List[str]) -> Dict[str, List[str]]:
    """要件に基づいてAWSサービスの推奨を提供"""
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
    
    recommendations = {}
    for req in requirements:
        if req in requirement_mapping:
            recommendations[req] = requirement_mapping[req]
    
    return recommendations

def display_services():
    """利用可能なAWSサービス一覧を表示"""
    print("\n📋 利用可能なAWSサービス:")
    print("=" * 50)
    for category, services in AWS_SERVICES.items():
        print(f"\n🔹 {category}:")
        print("  " + ", ".join(services))

def get_player_name():
    """プレイヤー名を必須入力として取得"""
    while True:
        player_name = input("プレイヤー名を入力してください: ").strip()
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
            confirm = input("\nこれらのサービスを含めて続行しますか？ (Yes/No): ").strip().lower()
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
    print("🎮 AWS アーキテクチャ・クイズマスター (デモ版)")
    print("=" * 60)
    
    # プレイヤー名を必須入力として取得
    player_name = get_player_name()
    total_score = 0
    
    print(f"\n👋 ようこそ、{player_name}さん！")
    print("AWSアーキテクチャの知識を試してみましょう！")
    
    while True:
        print("\n" + "="*60)
        print("📋 利用可能なシナリオ:")
        for i, scenario in enumerate(SCENARIOS, 1):
            print(f"{i}. {scenario['title']} ({scenario['difficulty']}) - 最大{scenario['max_score']}点")
        
        try:
            choice = input("\nシナリオを選択してください (1-3, q=終了): ").strip()
            
            if choice.lower() == 'q':
                break
                
            choice = int(choice)
            if 1 <= choice <= len(SCENARIOS):
                scenario = SCENARIOS[choice - 1]
                
                # シナリオの説明
                print(f"\n🎯 **{scenario['title']}**")
                print(f"📝 {scenario['description']}")
                print(f"🏆 難易度: {scenario['difficulty']} | 最大スコア: {scenario['max_score']}点")
                
                print(f"\n📋 **要件:**")
                for req in scenario['requirements']:
                    print(f"  • {req}")
                
                # 推奨サービスのヒント
                recommendations = get_service_recommendations(scenario['requirements'])
                print(f"\n💡 **ヒント - 要件別推奨サービス:**")
                for req, services in recommendations.items():
                    print(f"  • {req}: {', '.join(services)}")
                
                # サービス一覧表示
                display_services()
                
                # プレイヤーの選択を受付
                while True:
                    print(f"\n🎯 **{scenario['title']}** に最適なサービスを選択してください:")
                    print("サービス名をカンマ区切りで入力してください")
                    print("例: EC2, RDS, S3, CloudFront")
                    
                    selected_input = input("\n選択: ").strip()
                    if not selected_input:
                        print("❌ サービスが選択されていません。")
                        continue
                    
                    # 入力検証とYes/No確認
                    selected_services = validate_service_input(selected_input, AWS_SERVICES)
                    if selected_services is not None:
                        break
                
                if selected_services:
                    print(f"\n🔍 選択されたサービス: {', '.join(selected_services)}")
                    
                    # 評価を実行
                    evaluation = evaluate_architecture(selected_services, scenario['id'])
                    cost_analysis = check_architecture_cost(selected_services)
                    
                    # 結果表示
                    print(f"\n📊 **評価結果**")
                    print("=" * 40)
                    print(f"🏆 スコア: {evaluation['score']}/{scenario['max_score']}点")
                    print(f"📈 グレード: {evaluation['grade']}")
                    print(f"✅ 正解率: {evaluation['correct_ratio']}%")
                    print(f"💬 {evaluation['comment']}")
                    
                    if evaluation['correct_services']:
                        print(f"\n✅ **正解したサービス:**")
                        for service in evaluation['correct_services']:
                            print(f"  • {service}")
                    
                    if evaluation['missed_services']:
                        print(f"\n❌ **見逃したサービス:**")
                        for service in evaluation['missed_services']:
                            print(f"  • {service}")
                    
                    if evaluation['incorrect_services']:
                        print(f"\n⚠️  **不要なサービス:**")
                        for service in evaluation['incorrect_services']:
                            print(f"  • {service}")
                    
                    # コスト分析
                    print(f"\n💰 **コスト分析**")
                    print("=" * 40)
                    print(f"💵 月額概算コスト: ${cost_analysis['total_monthly_cost']}")
                    print(f"🌍 リージョン: {cost_analysis['region']}")
                    
                    if cost_analysis['cost_breakdown']:
                        print(f"\n📋 **サービス別コスト:**")
                        for service, cost in cost_analysis['cost_breakdown'].items():
                            if cost > 0:
                                print(f"  • {service}: ${cost}")
                            else:
                                print(f"  • {service}: 無料")
                    
                    total_score += evaluation['score']
                    
                    # 学習ポイント
                    print(f"\n📚 **学習ポイント:**")
                    if evaluation['grade'] in ['S', 'A']:
                        print("  • 素晴らしい選択です！AWSのベストプラクティスを理解していますね。")
                    elif evaluation['grade'] == 'B':
                        print("  • 基本的な構成は良好です。セキュリティや監視の観点も考慮してみましょう。")
                    elif evaluation['grade'] == 'C':
                        print("  • 要件を満たす基本サービスは選択できています。高可用性や拡張性も検討してみましょう。")
                    else:
                        print("  • 要件を再確認し、各要件に対応するサービスを選択してみましょう。")
                    
                    print("  • コスト最適化のため、適切なインスタンスサイズやリザーブドインスタンスも検討しましょう。")
                    print("  • 実際の本番環境では、災害復旧やバックアップ戦略も重要です。")
                
                # 続行確認
                continue_game = input("\n🎮 別のシナリオに挑戦しますか？ (y/n): ").lower().strip()
                if continue_game != 'y':
                    break
            else:
                print("❌ 無効な選択です。1-3の数字を入力してください。")
                
        except ValueError:
            print("❌ 数字を入力してください。")
        except KeyboardInterrupt:
            print("\n\n👋 ゲームを終了します。お疲れさまでした！")
            break
    
    print(f"\n🎉 **ゲーム終了！**")
    print("=" * 50)
    print(f"🏆 {player_name}さんの総スコア: {total_score}点")
    print("📚 AWSアーキテクチャの学習、お疲れさまでした！")
    print("💡 実際のプロジェクトでも今日学んだ知識を活用してくださいね。")

if __name__ == "__main__":
    main()
