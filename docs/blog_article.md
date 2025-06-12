# Strands Agentで作るAWSアーキテクチャ学習ゲーム開発記

## はじめに

AWSのアーキテクチャ設計スキルを楽しく学習できるゲームを作りたい！そんな思いから、最新のAI エージェントフレームワーク「Strands Agent」を使って、インタラクティブなクイズゲームを開発しました。

この記事では、企画から実装、そして改善までの開発過程を詳しく紹介します。

## 🎯 プロジェクトの背景

### なぜAWSアーキテクチャ学習ゲームなのか？

- **実践的なスキル習得**: 座学だけでは身につかないアーキテクチャ設計の感覚
- **コスト意識の向上**: 実際の料金を意識した設計判断
- **楽しい学習体験**: ゲーミフィケーションによる継続的な学習

### Strands Agentを選んだ理由

- **豊富なツールセット**: AWS連携、コスト計算、画像生成など
- **簡単な実装**: `@tool`デコレータで簡単にカスタムツール作成
- **AI駆動**: Claude 3.7による自然な対話とフィードバック

## 🚀 開発フェーズ1: 企画とアイデア出し

### 初期調査

まずはStrands Agentの機能を調査しました。

```python
# Strands Agentの基本構造
from strands import Agent, tool
from strands_tools import use_aws, calculator, generate_image

agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[use_aws, calculator, generate_image],
    system_prompt="あなたはAWSエキスパートです"
)
```

### 3つのゲームアイデア

1. **🏗️ AWS アーキテクチャ・クイズマスター** ← 採用！
   - シナリオベースのアーキテクチャ設計
   - コスト分析とスコアリング
   
2. **🚨 AWS インシデント・レスポンス・シミュレーター**
   - リアルタイム障害対応ゲーム
   
3. **🎯 AWS コスト最適化チャレンジ**
   - 既存環境の最適化競争

## 🛠️ 開発フェーズ2: 基本実装

### ゲームデータ構造の設計

```python
SCENARIOS = [
    {
        "id": 1,
        "title": "スタートアップのWebアプリケーション",
        "description": "月間10万PVのWebアプリケーションを構築",
        "requirements": ["高可用性", "自動スケーリング", "データベース"],
        "correct_services": ["EC2", "ALB", "Auto Scaling", "RDS"],
        "difficulty": "初級",
        "max_score": 100
    }
]
```

### カスタムツールの実装

#### コスト計算ツール

```python
@tool
def check_architecture_cost(services: List[str]) -> Dict[str, Any]:
    """選択されたAWSサービス構成の概算月額コストを計算"""
    service_costs = {
        "EC2": 30.37,  # t3.medium
        "RDS": 33.58,  # db.t3.small
        "ALB": 22.27,
        # ... 他のサービス
    }
    
    total_cost = sum(service_costs.get(service, 0) for service in services)
    return {
        "total_monthly_cost": round(total_cost, 2),
        "cost_breakdown": {s: service_costs.get(s, 0) for s in services}
    }
```

#### 評価システム

```python
@tool
def evaluate_architecture(selected_services: List[str], scenario_id: int) -> Dict:
    """アーキテクチャを評価してスコアを計算"""
    scenario = get_scenario(scenario_id)
    correct_services = set(scenario["correct_services"])
    selected_set = set(selected_services)
    
    correct_matches = correct_services.intersection(selected_set)
    correct_ratio = len(correct_matches) / len(correct_services)
    
    # スコア計算とグレード判定
    final_score = max(0, int(scenario["max_score"] * correct_ratio - penalty))
    grade = get_grade(correct_ratio)
    
    return {
        "score": final_score,
        "grade": grade,
        "correct_services": list(correct_matches),
        "missed_services": list(correct_services - selected_set)
    }
```

## 🎮 開発フェーズ3: ゲーム体験の向上

### 3つの難易度レベル

| 難易度 | シナリオ | 最大スコア | 主な技術要素 |
|--------|----------|------------|--------------|
| 初級 | スタートアップWeb | 100点 | EC2, RDS, S3 |
| 中級 | データ分析基盤 | 150点 | Kinesis, EMR, Redshift |
| 上級 | マイクロサービス | 200点 | EKS, API Gateway, X-Ray |

### 学習支援機能

```python
def get_service_recommendations(requirements: List[str]) -> Dict:
    """要件に基づくサービス推奨"""
    mapping = {
        "高可用性": ["ALB", "Auto Scaling", "Multi-AZ RDS"],
        "データベース": ["RDS", "DynamoDB", "ElastiCache"],
        "静的コンテンツ配信": ["S3", "CloudFront"]
    }
    return {req: mapping.get(req, []) for req in requirements}
```

## 🔧 開発フェーズ4: ユーザビリティ改善

### 課題1: プレイヤー名の必須化

**要求**: ユーザー名を必須入力にしたい

**実装**:
```python
def get_player_name():
    """プレイヤー名を必須入力として取得"""
    while True:
        player_name = input("プレイヤー名を入力してください: ").strip()
        if player_name:
            return player_name
        else:
            print("❌ プレイヤー名は必須です。名前を入力してください。")
```

### 課題2: 入力検証とYes/No確認

**要求**: 提案外のサービス入力時にYes/Noで確認したい

**実装**:
```python
def validate_service_input(selected_input, available_services):
    """入力検証とYes/No確認"""
    all_services = []
    for services in available_services.values():
        all_services.extend(services)
    
    selected_services = [s.strip() for s in selected_input.split(",")]
    unknown_services = [s for s in selected_services if s not in all_services]
    
    if unknown_services:
        print(f"⚠️  以下のサービスは提案リストにありません:")
        for service in unknown_services:
            print(f"  • {service}")
        
        while True:
            confirm = input("これらのサービスを含めて続行しますか？ (Yes/No): ")
            if confirm.lower() in ['yes', 'y']:
                return selected_services
            elif confirm.lower() in ['no', 'n']:
                print("サービス選択をやり直してください。")
                return None
            else:
                print("❌ 'Yes' または 'No' で答えてください。")
    
    return selected_services
```

### 課題3: プロンプト表示の問題

**問題**: 初回起動時にプロンプトが表示されない

**試行錯誤**:
```python
# 試行1: flush=True
print("プレイヤー名を入力してください: ", end="", flush=True)
player_name = input().strip()

# 試行2: sys.stdout
sys.stdout.write("プレイヤー名を入力してください: ")
sys.stdout.flush()
player_name = input().strip()

# 最終解決: 標準的なinput()
player_name = input("プレイヤー名を入力してください: ").strip()
```

**学び**: 複雑な方法より、標準的な`input()`関数が最も確実！

## 📊 完成したゲームの特徴

### 🎯 主要機能

- **3つの難易度レベル**: 初級〜上級まで段階的学習
- **リアルタイムコスト計算**: 実際のAWS料金に基づく概算
- **詳細な評価システム**: S/A/B/C/Dグレードと改善提案
- **入力検証**: 安全で使いやすいUI
- **学習支援**: 要件別サービス推奨とヒント

### 🎮 ゲーム体験

```
🎮 AWS アーキテクチャ・クイズマスター (デモ版)
============================================================
プレイヤー名を入力してください: 田中太郎

👋 ようこそ、田中太郎さん！
AWSアーキテクチャの知識を試してみましょう！

📋 利用可能なシナリオ:
1. スタートアップのWebアプリケーション (初級) - 最大100点
2. エンタープライズのマイクロサービス (上級) - 最大200点
3. データ分析プラットフォーム (中級) - 最大150点

シナリオを選択してください (1-3, q=終了): 1

🎯 **スタートアップのWebアプリケーション**
📝 月間10万PVのWebアプリケーションを構築したい。コスト効率と拡張性を重視。
🏆 難易度: 初級 | 最大スコア: 100点

📋 **要件:**
  • 高可用性
  • 自動スケーリング
  • データベース
  • 静的コンテンツ配信
  • SSL証明書

選択: EC2, ALB, Auto Scaling, RDS, S3, CloudFront, ACM

📊 **評価結果**
========================================
🏆 スコア: 100/100点
📈 グレード: S
✅ 正解率: 100.0%
💬 🌟 素晴らしい！完璧に近いアーキテクチャです。

💰 **コスト分析**
========================================
💵 月額概算コスト: $194.22
🌍 リージョン: us-east-1
```

## 🏗️ アーキテクチャ設計

### ファイル構成

```
aws_architecture_quiz/
├── requirements.txt          # 依存関係
├── quiz_game.py             # Strands Agent版（完全版）
├── demo_game.py             # デモ版（依存関係なし）
├── test_game.py             # テスト実行
├── README.md                # ドキュメント
└── blog_article.md          # この記事
```

### 2つのバージョン

1. **完全版** (`quiz_game.py`)
   - Strands Agent + Claude 3.7
   - AI による動的な説明とフィードバック
   - 画像生成機能（アーキテクチャ図）
   - AWS API連携

2. **デモ版** (`demo_game.py`)
   - 依存関係なしで即実行可能
   - 基本的なゲーム機能
   - 学習・検証用

## 🎓 開発で学んだこと

### 技術的な学び

1. **Strands Agentの威力**
   - `@tool`デコレータの簡単さ
   - 豊富な組み込みツール
   - AI との自然な連携

2. **ユーザビリティの重要性**
   - プロンプト表示の細かな配慮
   - エラーハンドリングの充実
   - 段階的な機能改善

3. **教育ゲームの設計**
   - 適切な難易度設定
   - 建設的なフィードバック
   - 実践的な学習内容

### プロジェクト管理の学び

1. **段階的開発**
   - MVP → 機能追加 → 改善のサイクル
   - ユーザーフィードバックの重要性

2. **デモ版の価値**
   - 依存関係なしで試せる重要性
   - 学習・検証での活用

## 🚀 今後の拡張予定

### 短期的な改善

- [ ] より多くのシナリオ追加
- [ ] 実際のAWS Pricing APIとの連携
- [ ] アーキテクチャ図の自動生成
- [ ] 学習進捗の保存機能

### 長期的な展望

- [ ] マルチプレイヤー対応
- [ ] カスタムシナリオ作成機能
- [ ] 他のクラウドプロバイダー対応
- [ ] Web版の開発

## 💡 まとめ

Strands Agentを使ったAWSアーキテクチャ学習ゲームの開発を通じて、以下のことを実感しました：

1. **AI エージェントの可能性**: 教育分野での AI 活用の大きな潜在力
2. **実践的学習の価値**: ゲーミフィケーションによる効果的なスキル習得
3. **段階的改善の重要性**: ユーザーフィードバックに基づく継続的な改善

このプロジェクトが、AWSを学ぶ多くの人にとって有用なツールになることを願っています。また、Strands Agentの教育分野での活用例として、他の開発者の参考になれば幸いです。

## 🔗 リソース

- **GitHub**: [プロジェクトリポジトリ](https://github.com/your-repo/aws-architecture-quiz)
- **Strands Agents**: [公式ドキュメント](https://strandsagents.com)
- **AWS**: [アーキテクチャセンター](https://aws.amazon.com/architecture/)

---

*この記事が役に立ったら、ぜひスターやシェアをお願いします！*

**タグ**: #AWS #StradsAgent #AI #教育 #ゲーミフィケーション #アーキテクチャ #Python
