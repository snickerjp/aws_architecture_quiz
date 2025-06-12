#!/usr/bin/env python3
"""
AWS アーキテクチャ・クイズマスター - テスト実行
正解例を使ってゲームをテスト
"""

from demo_game import evaluate_architecture, check_architecture_cost, SCENARIOS

def test_scenario_1():
    """シナリオ1: スタートアップのWebアプリケーション - 正解例"""
    print("🧪 テスト: シナリオ1 - 正解例")
    print("=" * 50)
    
    # 正解のサービス構成
    correct_services = ["EC2", "ALB", "Auto Scaling", "RDS", "S3", "CloudFront", "ACM"]
    
    # 評価実行
    evaluation = evaluate_architecture(correct_services, 1)
    cost_analysis = check_architecture_cost(correct_services)
    
    print(f"選択サービス: {', '.join(correct_services)}")
    print(f"スコア: {evaluation['score']}/100点")
    print(f"グレード: {evaluation['grade']}")
    print(f"正解率: {evaluation['correct_ratio']}%")
    print(f"月額コスト: ${cost_analysis['total_monthly_cost']}")
    print(f"コメント: {evaluation['comment']}")
    print()

def test_scenario_2():
    """シナリオ2: エンタープライズのマイクロサービス - 正解例"""
    print("🧪 テスト: シナリオ2 - 正解例")
    print("=" * 50)
    
    # 正解のサービス構成
    correct_services = ["EKS", "App Mesh", "API Gateway", "CloudWatch", "X-Ray", "WAF", "Secrets Manager"]
    
    # 評価実行
    evaluation = evaluate_architecture(correct_services, 2)
    cost_analysis = check_architecture_cost(correct_services)
    
    print(f"選択サービス: {', '.join(correct_services)}")
    print(f"スコア: {evaluation['score']}/200点")
    print(f"グレード: {evaluation['grade']}")
    print(f"正解率: {evaluation['correct_ratio']}%")
    print(f"月額コスト: ${cost_analysis['total_monthly_cost']}")
    print(f"コメント: {evaluation['comment']}")
    print()

def test_scenario_3():
    """シナリオ3: データ分析プラットフォーム - 正解例"""
    print("🧪 テスト: シナリオ3 - 正解例")
    print("=" * 50)
    
    # 正解のサービス構成
    correct_services = ["Kinesis", "S3", "EMR", "Redshift", "QuickSight", "SageMaker", "Glue"]
    
    # 評価実行
    evaluation = evaluate_architecture(correct_services, 3)
    cost_analysis = check_architecture_cost(correct_services)
    
    print(f"選択サービス: {', '.join(correct_services)}")
    print(f"スコア: {evaluation['score']}/150点")
    print(f"グレード: {evaluation['grade']}")
    print(f"正解率: {evaluation['correct_ratio']}%")
    print(f"月額コスト: ${cost_analysis['total_monthly_cost']}")
    print(f"コメント: {evaluation['comment']}")
    print()

def test_partial_answer():
    """部分的な回答のテスト"""
    print("🧪 テスト: 部分的な回答例")
    print("=" * 50)
    
    # 部分的な回答（一部正解、一部不正解）
    partial_services = ["EC2", "RDS", "S3", "Lambda", "DynamoDB"]  # 正解3つ、不正解2つ
    
    # 評価実行
    evaluation = evaluate_architecture(partial_services, 1)
    cost_analysis = check_architecture_cost(partial_services)
    
    print(f"選択サービス: {', '.join(partial_services)}")
    print(f"スコア: {evaluation['score']}/100点")
    print(f"グレード: {evaluation['grade']}")
    print(f"正解率: {evaluation['correct_ratio']}%")
    print(f"正解したサービス: {', '.join(evaluation['correct_services'])}")
    print(f"不要なサービス: {', '.join(evaluation['incorrect_services'])}")
    print(f"見逃したサービス: {', '.join(evaluation['missed_services'])}")
    print(f"月額コスト: ${cost_analysis['total_monthly_cost']}")
    print(f"コメント: {evaluation['comment']}")
    print()

if __name__ == "__main__":
    print("🎮 AWS アーキテクチャ・クイズマスター - テスト実行")
    print("=" * 60)
    print()
    
    # 各シナリオの正解例をテスト
    test_scenario_1()
    test_scenario_2() 
    test_scenario_3()
    test_partial_answer()
    
    print("✅ 全テスト完了！")
