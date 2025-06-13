# -*- coding: utf-8 -*-
"""
Multilingual support for AWS Architecture Quiz
多言語対応設定ファイル
"""

LANGUAGES = {
    "ja": {
        "name": "日本語",
        "code": "ja",
        "messages": {
            # Game title and welcome
            "game_title": "🎮 AWS アーキテクチャ・クイズマスター",
            "welcome_message": "AWS アーキテクチャ・クイズマスターへようこそ、{player_name}さん！",
            
            # Language selection
            "select_language": "言語を選択してください / Please select your language:",
            "language_selected": "言語が選択されました: {language}",
            
            # Player input
            "enter_player_name": "プレイヤー名を入力してください: ",
            "player_name_required": "❌ プレイヤー名は必須です。名前を入力してください。",
            
            # Scenario selection
            "available_scenarios": "📋 利用可能なシナリオ:",
            "select_scenario": "シナリオを選択してください (1-3): ",
            "invalid_selection": "無効な選択です。1-3の数字を入力してください。",
            "enter_number": "数字を入力してください。",
            
            # Service selection
            "select_services": "選択したサービスをカンマ区切りで入力してください:",
            "service_example": "例: EC2, RDS, S3, CloudFront",
            "service_selection": "選択: ",
            "no_services_selected": "❌ サービスが選択されていません。",
            
            # Validation
            "unknown_services_warning": "⚠️  以下のサービスは提案リストにありません:",
            "continue_with_unknown": "これらのサービスを含めて続行しますか？ (Yes/No): ",
            "retry_service_selection": "サービス選択をやり直してください。",
            "yes_no_prompt": "❌ 'Yes' または 'No' で答えてください。",
            
            # Game flow
            "new_challenge": "新しいチャレンジを開始します！",
            "scenario": "シナリオ",
            "description": "説明",
            "difficulty": "難易度",
            "max_score": "最大スコア",
            "requirements": "要件:",
            "evaluation_result": "📊 評価結果:",
            "continue_game": "別のシナリオに挑戦しますか？ (y/n): ",
            "game_end": "🎉 ゲーム終了！{player_name}さん、お疲れさまでした！",
            "game_interrupted": "ゲームを終了します。お疲れさまでした！",
            
            # Difficulty levels
            "beginner": "初級",
            "intermediate": "中級",
            "advanced": "上級",
            
            # Evaluation grades and comments
            "grade_s_comment": "素晴らしい！完璧に近いアーキテクチャです。",
            "grade_a_comment": "とても良いアーキテクチャです。",
            "grade_b_comment": "良いアーキテクチャですが、改善の余地があります。",
            "grade_c_comment": "基本的な要件は満たしていますが、重要な要素が不足しています。",
            "grade_d_comment": "アーキテクチャの見直しが必要です。",
        },
        
        # Scenarios
        "scenarios": [
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
    },
    
    "en": {
        "name": "English",
        "code": "en",
        "messages": {
            # Game title and welcome
            "game_title": "🎮 AWS Architecture Quiz Master",
            "welcome_message": "Welcome to AWS Architecture Quiz Master, {player_name}!",
            
            # Language selection
            "select_language": "言語を選択してください / Please select your language:",
            "language_selected": "Language selected: {language}",
            
            # Player input
            "enter_player_name": "Please enter your player name: ",
            "player_name_required": "❌ Player name is required. Please enter your name.",
            
            # Scenario selection
            "available_scenarios": "📋 Available Scenarios:",
            "select_scenario": "Please select a scenario (1-3): ",
            "invalid_selection": "Invalid selection. Please enter a number between 1-3.",
            "enter_number": "Please enter a number.",
            
            # Service selection
            "select_services": "Please enter your selected services separated by commas:",
            "service_example": "Example: EC2, RDS, S3, CloudFront",
            "service_selection": "Selection: ",
            "no_services_selected": "❌ No services selected.",
            
            # Validation
            "unknown_services_warning": "⚠️  The following services are not in the suggested list:",
            "continue_with_unknown": "Do you want to continue with these services? (Yes/No): ",
            "retry_service_selection": "Please retry service selection.",
            "yes_no_prompt": "❌ Please answer with 'Yes' or 'No'.",
            
            # Game flow
            "new_challenge": "Starting a new challenge!",
            "scenario": "Scenario",
            "description": "Description",
            "difficulty": "Difficulty",
            "max_score": "Max Score",
            "requirements": "Requirements:",
            "evaluation_result": "📊 Evaluation Result:",
            "continue_game": "Would you like to try another scenario? (y/n): ",
            "game_end": "🎉 Game Over! Thank you for playing, {player_name}!",
            "game_interrupted": "Game terminated. Thank you for playing!",
            
            # Difficulty levels
            "beginner": "Beginner",
            "intermediate": "Intermediate",
            "advanced": "Advanced",
            
            # Evaluation grades and comments
            "grade_s_comment": "Excellent! Near-perfect architecture.",
            "grade_a_comment": "Very good architecture.",
            "grade_b_comment": "Good architecture, but there's room for improvement.",
            "grade_c_comment": "Basic requirements are met, but important elements are missing.",
            "grade_d_comment": "Architecture needs review.",
        },
        
        # Scenarios
        "scenarios": [
            {
                "id": 1,
                "title": "Startup Web Application",
                "description": "Build a web application with 100K monthly page views. Focus on cost efficiency and scalability.",
                "requirements": [
                    "High availability",
                    "Auto scaling", 
                    "Database",
                    "Static content delivery",
                    "SSL certificate"
                ],
                "correct_services": [
                    "EC2", "ALB", "Auto Scaling", "RDS", "S3", "CloudFront", "ACM"
                ],
                "difficulty": "Beginner",
                "max_score": 100
            },
            {
                "id": 2,
                "title": "Enterprise Microservices",
                "description": "Build a large-scale microservices architecture. Security and monitoring are critical.",
                "requirements": [
                    "Container orchestration",
                    "Service mesh",
                    "API management",
                    "Log aggregation",
                    "Metrics monitoring",
                    "Security"
                ],
                "correct_services": [
                    "EKS", "App Mesh", "API Gateway", "CloudWatch", "X-Ray", "WAF", "Secrets Manager"
                ],
                "difficulty": "Advanced",
                "max_score": 200
            },
            {
                "id": 3,
                "title": "Data Analytics Platform",
                "description": "Build an analytics platform combining real-time and batch processing.",
                "requirements": [
                    "Streaming data processing",
                    "Data lake",
                    "Batch processing",
                    "Data warehouse",
                    "Visualization",
                    "Machine learning"
                ],
                "correct_services": [
                    "Kinesis", "S3", "EMR", "Redshift", "QuickSight", "SageMaker", "Glue"
                ],
                "difficulty": "Intermediate",
                "max_score": 150
            }
        ]
    }
}

def get_supported_languages():
    """Get list of supported languages"""
    return [(code, lang["name"]) for code, lang in LANGUAGES.items()]

def get_language_config(language_code):
    """Get language configuration"""
    return LANGUAGES.get(language_code, LANGUAGES["en"])

def get_message(language_code, key, **kwargs):
    """Get localized message"""
    config = get_language_config(language_code)
    message = config["messages"].get(key, key)
    if kwargs:
        return message.format(**kwargs)
    return message

def get_scenarios(language_code):
    """Get scenarios in specified language"""
    config = get_language_config(language_code)
    return config["scenarios"]
