# AWS Architecture Quiz Master - Usage Guide
# AWS アーキテクチャ・クイズマスター - 使用ガイド

## Quick Start / クイックスタート

### 1. Installation / インストール
```bash
# Install dependencies / 依存関係のインストール
pip install -r requirements.txt
```

### 2. Run the Game / ゲーム実行

#### Option A: Simple Demo (No AWS credentials required)
#### オプション A: 簡単デモ（AWS認証情報不要）
```bash
python simple_multilingual_demo.py
```

#### Option B: Full Game with AI Agent (AWS credentials required)
#### オプション B: AIエージェント付きフルゲーム（AWS認証情報必要）
```bash
# Configure AWS credentials first / 最初にAWS認証情報を設定
aws configure

# Run full game / フルゲーム実行
python multilingual_quiz_game.py
```

## Game Features / ゲーム機能

### 🌍 Language Support / 言語サポート
- **English**: Full English interface and scenarios
- **日本語**: 完全な日本語インターフェースとシナリオ

### 🎯 Scenarios / シナリオ
1. **Startup Web Application / スタートアップのWebアプリケーション** (Beginner/初級)
2. **Enterprise Microservices / エンタープライズのマイクロサービス** (Advanced/上級)
3. **Data Analytics Platform / データ分析プラットフォーム** (Intermediate/中級)

### 💰 Cost Analysis / コスト分析
- Automatic cost calculation for selected services
- 選択したサービスの自動コスト計算

### 📊 Evaluation System / 評価システム
- Score: 0-200 points depending on scenario
- Grade: S, A, B, C, D
- Detailed feedback and improvement suggestions

## Game Flow / ゲームの流れ

### 1. Language Selection / 言語選択
```
言語を選択してください / Please select your language:
1. 日本語 (ja)
2. English (en)
Select language (1-2): 
```

### 2. Player Registration / プレイヤー登録
```
Please enter your player name: John Smith
Welcome to AWS Architecture Quiz Master, John Smith!
```

### 3. Scenario Selection / シナリオ選択
```
📋 Available Scenarios:
1. Startup Web Application (Beginner)
2. Enterprise Microservices (Advanced)
3. Data Analytics Platform (Intermediate)
Please select a scenario (1-3): 
```

### 4. Service Selection / サービス選択
```
Please enter your selected services separated by commas:
Example: EC2, RDS, S3, CloudFront
Selection: EC2, ALB, Auto Scaling, RDS, S3, CloudFront, ACM
```

### 5. Evaluation / 評価
```
📊 Evaluation Result:
💰 Cost Analysis: $177.43/month
📊 Architecture Evaluation: 100/100 (Grade: S)
Comment: Excellent! Near-perfect architecture.
```

## Available AWS Services / 利用可能なAWSサービス

### Compute / コンピューティング
- EC2, Lambda, ECS, EKS, Fargate, Batch

### Storage / ストレージ
- S3, EBS, EFS, FSx

### Database / データベース
- RDS, DynamoDB, ElastiCache, Redshift, DocumentDB

### Networking / ネットワーキング
- VPC, ALB, NLB, CloudFront, Route 53, API Gateway

### Security / セキュリティ
- IAM, WAF, Shield, ACM, Secrets Manager, KMS

### Monitoring / モニタリング
- CloudWatch, X-Ray, CloudTrail, Config

### Analytics / 分析
- Kinesis, EMR, Glue, Athena, QuickSight

### ML/AI / 機械学習・AI
- SageMaker, Bedrock, Rekognition, Comprehend

### Management / 管理
- CloudFormation, Systems Manager, Auto Scaling

## Scoring System / スコアリングシステム

### Score Calculation / スコア計算
```
Base Score = Scenario Max Score × Correct Ratio
Penalty = Number of Unnecessary Services × 10
Final Score = Base Score - Penalty
```

### Grades / グレード
- **S**: 90%+ accuracy (素晴らしい！)
- **A**: 70-89% accuracy (とても良い)
- **B**: 50-69% accuracy (良い、改善の余地あり)
- **C**: 30-49% accuracy (基本要件は満たしている)
- **D**: <30% accuracy (見直しが必要)

## Tips for Success / 成功のコツ

### English Tips:
1. **Read requirements carefully** - Each scenario has specific needs
2. **Consider cost efficiency** - Don't over-engineer solutions
3. **Think about scalability** - Plan for growth
4. **Security first** - Always include security services
5. **Monitor everything** - Include monitoring and logging

### 日本語のコツ:
1. **要件を注意深く読む** - 各シナリオには特定のニーズがあります
2. **コスト効率を考慮** - 過度に複雑な解決策は避ける
3. **拡張性を考える** - 成長を見込んだ計画を立てる
4. **セキュリティ第一** - 常にセキュリティサービスを含める
5. **すべてを監視** - モニタリングとログ記録を含める

## Troubleshooting / トラブルシューティング

### Common Issues / よくある問題

#### 1. Module Not Found Error
```bash
pip install -r requirements.txt
```

#### 2. AWS Credentials Error (Full game only)
```bash
aws configure
# Enter your AWS Access Key ID, Secret Access Key, and region
```

#### 3. Permission Denied for Bedrock (Full game only)
- Enable model access in Amazon Bedrock console
- Ensure your AWS user has Bedrock permissions

### Error Messages / エラーメッセージ

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'strands_tools'` | Run `pip install strands-agents-tools` |
| `AWS credentials not configured` | Run `aws configure` |
| `Access denied to Bedrock` | Enable model access in AWS console |

## File Structure / ファイル構成

```
aws_architecture_quiz/
├── multilingual_quiz_game.py     # Full game with AI agent
├── simple_multilingual_demo.py   # Simple demo without AI
├── languages.py                  # Language configurations
├── test_multilingual.py          # Test suite
├── test_game_functionality.py    # Functionality tests
├── requirements.txt              # Dependencies
├── README_multilingual.md        # Documentation
└── USAGE_GUIDE.md               # This file
```

## Support / サポート

For issues or questions:
- Check the troubleshooting section above
- Review the test files for examples
- Ensure all dependencies are installed

問題や質問がある場合：
- 上記のトラブルシューティングセクションを確認
- 例についてはテストファイルを確認
- すべての依存関係がインストールされていることを確認
