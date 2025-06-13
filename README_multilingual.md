# AWS Architecture Quiz Master / AWS アーキテクチャ・クイズマスター

A multilingual AWS architecture learning game using Strands Agent.  
Strands Agentを使用した多言語対応AWSアーキテクチャ学習ゲームです。

## Overview / 概要

This game helps you improve your AWS service knowledge and architecture design skills by designing optimal AWS architectures for various scenarios. Now available in multiple languages!

このゲームでは、様々なシナリオに対して最適なAWSアーキテクチャを設計することで、AWSサービスの知識とアーキテクチャ設計スキルを向上させることができます。多言語対応になりました！

## Features / 特徴

- 🌍 **Multilingual Support**: English and Japanese / **多言語対応**: 英語と日本語
- 🎯 **3 Difficulty Levels**: Beginner, Intermediate, Advanced / **3つの難易度レベル**: 初級、中級、上級
- 💰 **Cost Analysis**: Automatic cost calculation for selected services / **コスト分析**: 選択したサービス構成の概算コストを自動計算
- 📊 **Detailed Evaluation**: Accuracy, improvement points, and best practices / **詳細な評価**: 正解率、改善点、ベストプラクティスを提示
- 🤖 **AI Quiz Master**: Strands Agent provides friendly guidance / **AI クイズマスター**: Strands Agentが親切にガイド
- 🏆 **Scoring System**: Performance-based scoring / **スコアリングシステム**: パフォーマンスに基づいた採点
- 👤 **User Authentication**: Required player name input / **ユーザー認証**: プレイヤー名の必須入力
- ✅ **Input Validation**: Confirmation for non-suggested services / **入力検証**: 提案外サービスの確認機能

## Supported Languages / 対応言語

- **English** - Full support for English interface and scenarios
- **日本語** - 日本語インターフェースとシナリオの完全サポート

## Scenarios / シナリオ

### 1. Startup Web Application / スタートアップのWebアプリケーション (Beginner/初級)
- **English**: Web application with 100K monthly page views, focusing on cost efficiency and scalability
- **日本語**: 月間10万PVのWebアプリケーション、コスト効率と拡張性を重視
- **Max Score / 最大スコア**: 100 points / 100点

### 2. Enterprise Microservices / エンタープライズのマイクロサービス (Advanced/上級)  
- **English**: Large-scale microservices architecture with critical security and monitoring requirements
- **日本語**: 大規模なマイクロサービスアーキテクチャ、セキュリティとモニタリングが重要
- **Max Score / 最大スコア**: 200 points / 200点

### 3. Data Analytics Platform / データ分析プラットフォーム (Intermediate/中級)
- **English**: Analytics platform combining real-time and batch processing
- **日本語**: リアルタイムデータ処理とバッチ処理を組み合わせた分析基盤
- **Max Score / 最大スコア**: 150 points / 150点

## Setup / セットアップ

### Prerequisites / 前提条件

- Python 3.8 or higher / Python 3.8以上
- AWS credentials configured (AWS CLI or environment variables) / AWS認証情報の設定（AWS CLI または環境変数）
- Amazon Bedrock access permissions / Amazon Bedrock へのアクセス権限

### Installation / インストール

```bash
# Install dependencies / 依存関係のインストール
pip install -r requirements.txt

# Configure AWS credentials (if not already set) / AWS認証情報の設定（未設定の場合）
aws configure
```

⚠️ **AWS認証情報について / About AWS Credentials**:
- フルゲーム機能にはAWS認証情報が必要です / AWS credentials are required for full game features
- 詳細な設定方法は `AWS_CREDENTIALS_SETUP.md` をご覧ください / See `AWS_CREDENTIALS_SETUP.md` for detailed setup instructions
- 認証情報なしでも `offline_demo.py` で基本機能をお試しいただけます / You can try basic features with `offline_demo.py` without credentials

### Amazon Bedrock Model Access / Amazon Bedrock モデルアクセスの有効化

1. Access Amazon Bedrock in AWS Console / AWS コンソールで Amazon Bedrock にアクセス
2. Enable access to Claude 3.7 Sonnet model in "Model access" / 「Model access」で Claude 3.7 Sonnet モデルへのアクセスを有効化
3. Optionally enable access to image generation models / 必要に応じて画像生成モデルへのアクセスも有効化

## Usage / 使用方法

### Option 1: Full Game with AI Agent (Requires AWS credentials)
### オプション1: AIエージェント付きフルゲーム（AWS認証情報必要）
```bash
python multilingual_quiz_game.py
```

### Option 2: Simple Demo (No AWS credentials required)
### オプション2: 簡単デモ（AWS認証情報不要）
```bash
python simple_multilingual_demo.py
```

### Option 3: Offline Demo with Mock AI (No AWS credentials required)
### オプション3: モックAI付きオフラインデモ（AWS認証情報不要）
```bash
python offline_demo.py
```

### Game Flow / ゲームの流れ

1. **Select Language / 言語選択**
   - Choose between English and Japanese / 英語と日本語から選択
2. **Enter Player Name / プレイヤー名を入力** (Required / 必須)
   - Error message displayed if empty / 空の場合はエラーメッセージが表示され再入力
3. **Select Scenario / シナリオを選択** (1-3)
4. **Review Requirements / 要件を確認**
5. **Select Appropriate AWS Services / 適切なAWSサービスを選択**
   - Yes/No confirmation for services not in suggestions / 提案リスト外のサービスがある場合はYes/No確認
   - Re-input on No, evaluation on Yes / No選択時は再入力、Yes選択時は評価実行
6. **Review Evaluation Results and Feedback / 評価結果とフィードバックを確認**
7. **Challenge Next Scenario or Exit / 次のシナリオに挑戦または終了**

### Input Examples / 入力例

```
# Language Selection / 言語選択
言語を選択してください / Please select your language:
1. 日本語 (ja)
2. English (en)
Select language (1-2): 2

# Player Name (Required) / プレイヤー名（必須）
Please enter your player name: John Smith

# Service Selection / サービス選択
Please enter your selected services separated by commas:
Example: EC2, RDS, S3, CloudFront
Selection: EC2, ALB, Auto Scaling, RDS, S3, CloudFront, ACM

# Non-suggested Services Warning / 提案外サービスがある場合
⚠️  The following services are not in the suggested list:
  • CustomService
Do you want to continue with these services? (Yes/No): No
Please retry service selection.
```

## Evaluation System / 評価システム

### Score Calculation / スコア計算
- **Base Score / 基本スコア** = Scenario Max Score × Accuracy Rate / シナリオの最大スコア × 正解率
- **Penalty / ペナルティ** = Number of Unnecessary Services × 10 points / 不要なサービス数 × 10点
- **Final Score / 最終スコア** = Base Score - Penalty / 基本スコア - ペナルティ

### Grades / グレード
- **S**: 90%+ accuracy / 90%以上の正解率
- **A**: 70-89% accuracy / 70-89%の正解率  
- **B**: 50-69% accuracy / 50-69%の正解率
- **C**: 30-49% accuracy / 30-49%の正解率
- **D**: Under 30% accuracy / 30%未満の正解率

## Customization / カスタマイズ

### Adding New Languages / 新しい言語の追加

Add new language configurations to `languages.py`:

```python
LANGUAGES["es"] = {
    "name": "Español",
    "code": "es",
    "messages": {
        # Add Spanish messages here
    },
    "scenarios": [
        # Add Spanish scenarios here
    ]
}
```

### Adding New Scenarios / 新しいシナリオの追加

Add new scenarios to the `scenarios` list in each language configuration in `languages.py`:

```python
{
    "id": 4,
    "title": "New Scenario Title",
    "description": "Scenario description",
    "requirements": ["Requirement 1", "Requirement 2"],
    "correct_services": ["Service1", "Service2"],
    "difficulty": "Intermediate",
    "max_score": 120
}
```

### Updating Cost Information / コスト情報の更新

Update the `service_costs` dictionary in the `check_architecture_cost` function to reflect the latest pricing information.

## File Structure / ファイル構成

```
aws_architecture_quiz/
├── multilingual_quiz_game.py    # Main multilingual game file
├── languages.py                 # Language configurations
├── quiz_game.py                # Original Japanese-only version
├── requirements.txt            # Python dependencies
└── README_multilingual.md      # This file
```

## Troubleshooting / トラブルシューティング

### Common Issues / よくある問題

1. **Bedrock Access Error / Bedrock アクセスエラー**
   - Verify model access is enabled in Amazon Bedrock / Amazon Bedrock でモデルアクセスが有効化されているか確認
   - Check AWS credentials are properly configured / AWS認証情報が正しく設定されているか確認

2. **Module Not Found Error / モジュールが見つからないエラー**
   - Run `pip install -r requirements.txt` / `pip install -r requirements.txt` を実行
   - Verify Python environment is properly configured / Python環境が正しく設定されているか確認

3. **Inaccurate Cost Calculation / コスト計算が不正確**
   - Actual AWS pricing varies by region and usage / 実際のAWS料金は地域や使用量により変動します
   - Use AWS Pricing Calculator for more accurate estimates / より正確な見積もりには AWS Pricing Calculator を使用してください

## Future Enhancements / 今後の拡張予定

- [ ] More language support (Spanish, French, German, etc.) / より多くの言語サポート（スペイン語、フランス語、ドイツ語など）
- [ ] More scenarios / より多くのシナリオの追加
- [ ] Integration with actual AWS Pricing API / 実際のAWS Pricing APIとの連携
- [ ] Automatic architecture diagram generation / アーキテクチャ図の自動生成
- [ ] Multiplayer support / マルチプレイヤー対応
- [ ] Learning progress saving / 学習進捗の保存機能
- [ ] Custom scenario creation / カスタムシナリオの作成機能

## License / ライセンス

MIT License

## Contributing / 貢献

Pull requests and issue reports are welcome!  
プルリクエストやイシューの報告を歓迎します！

---

## Quick Start / クイックスタート

1. **Clone and setup / クローンとセットアップ**:
   ```bash
   git clone <repository-url>
   cd aws_architecture_quiz
   pip install -r requirements.txt
   ```

2. **Configure AWS / AWS設定**:
   ```bash
   aws configure
   ```

3. **Run the game / ゲーム実行**:
   ```bash
   python multilingual_quiz_game.py
   ```

4. **Select your language and start playing! / 言語を選択してプレイ開始！**
