# 技術詳解: Strands AgentによるAWSアーキテクチャ学習ゲーム

## 🔧 技術スタック詳細

### 使用技術

| 技術 | バージョン | 用途 |
|------|------------|------|
| Python | 3.8+ | メイン言語 |
| Strands Agents | 0.1.0+ | AI エージェントフレームワーク |
| Amazon Bedrock | - | Claude 3.7 Sonnet モデル |
| boto3 | 1.34.0+ | AWS SDK |

### 依存関係

```txt
strands-agents>=0.1.0
strands-agents-tools>=0.1.0
boto3>=1.34.0
```

## 🏗️ アーキテクチャ詳細

### システム構成図

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  Game Engine    │───▶│  AI Agent       │
│                 │    │                 │    │ (Claude 3.7)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │ Custom Tools    │    │ Built-in Tools  │
                       │ - Cost Calc     │    │ - AWS CLI       │
                       │ - Evaluation    │    │ - Calculator    │
                       │ - Validation    │    │ - Image Gen     │
                       └─────────────────┘    └─────────────────┘
```

### データフロー

```python
# 1. ユーザー入力
user_input = "EC2, RDS, S3, CloudFront"

# 2. 入力検証
validated_services = validate_service_input(user_input, AWS_SERVICES)

# 3. 評価実行
evaluation = evaluate_architecture(validated_services, scenario_id)

# 4. コスト分析
cost_analysis = check_architecture_cost(validated_services)

# 5. AI フィードバック生成
feedback = quiz_agent(f"評価結果: {evaluation}, コスト: {cost_analysis}")
```

## 🛠️ カスタムツール実装詳細

### 1. コスト計算ツール

```python
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
    # サービス別料金テーブル（2024年12月時点の概算）
    service_costs = {
        # Compute
        "EC2": {"t3.medium": 30.37, "m5.large": 70.08, "c5.xlarge": 156.82},
        "Lambda": 20.00,  # 1M requests/month
        "ECS": 0.00,      # EC2起動タイプの場合
        "EKS": 72.00,     # クラスター料金
        "Fargate": 0.00,  # 使用量ベース
        
        # Storage
        "S3": 23.00,      # 1TB Standard
        "EBS": 10.00,     # 100GB gp3
        "EFS": 30.00,     # 100GB Standard
        
        # Database
        "RDS": {"db.t3.micro": 16.79, "db.t3.small": 33.58, "db.m5.large": 140.16},
        "DynamoDB": 25.00,    # 25 RCU/WCU
        "ElastiCache": 45.00, # cache.t3.micro
        "Redshift": 180.00,   # dc2.large
        
        # Networking
        "ALB": 22.27,
        "NLB": 22.27,
        "CloudFront": 85.00,  # 1TB data transfer
        "Route 53": 0.50,     # hosted zone
        "API Gateway": 35.00, # 1M requests
        
        # Security & Management
        "WAF": 5.00,
        "Shield": 0.00,       # Standard is free
        "ACM": 0.00,          # 無料
        "Secrets Manager": 0.40,
        "KMS": 1.00,
        "CloudWatch": 10.00,
        "X-Ray": 5.00,
        "CloudTrail": 0.00,   # 管理イベントは無料
        
        # Analytics & ML
        "Kinesis": 15.00,     # 1 shard
        "EMR": 100.00,        # m5.xlarge cluster
        "Glue": 44.00,        # 10 DPU-hours/day
        "Athena": 50.00,      # 1TB scanned/month
        "QuickSight": 18.00,  # Standard edition
        "SageMaker": 50.00,   # ml.t3.medium
        "Bedrock": 0.00,      # 使用量ベース
        
        # Others
        "Auto Scaling": 0.00, # 無料
        "CloudFormation": 0.00, # 無料
        "Systems Manager": 0.00, # 基本機能は無料
    }
    
    total_cost = 0
    cost_breakdown = {}
    
    for service in services:
        if service in service_costs:
            cost_data = service_costs[service]
            if isinstance(cost_data, dict):
                # 複数の料金オプションがある場合、最小構成を選択
                cost = min(cost_data.values())
            else:
                cost = cost_data
            
            cost_breakdown[service] = cost
            total_cost += cost
        else:
            # 未知のサービスは0円として扱う
            cost_breakdown[service] = 0
    
    return {
        "total_monthly_cost": round(total_cost, 2),
        "cost_breakdown": cost_breakdown,
        "region": region,
        "currency": "USD",
        "note": "概算料金です。実際の料金は使用量や契約により異なります。"
    }
```

### 2. 評価システム

```python
@tool
def evaluate_architecture(selected_services: List[str], scenario_id: int) -> Dict[str, Any]:
    """
    選択されたアーキテクチャを評価してスコアを計算
    
    評価アルゴリズム:
    1. 正解率計算: 正解したサービス数 / 必要なサービス数
    2. ペナルティ計算: 不要なサービス数 × 10点
    3. 最終スコア: 基本スコア × 正解率 - ペナルティ
    """
    scenario = next((s for s in SCENARIOS if s["id"] == scenario_id), None)
    if not scenario:
        return {"error": "Invalid scenario ID"}
    
    correct_services = set(scenario["correct_services"])
    selected_services_set = set(selected_services)
    
    # 集合演算による分析
    correct_matches = correct_services.intersection(selected_services_set)
    incorrect_services = selected_services_set - correct_services
    missed_services = correct_services - selected_services_set
    
    # スコア計算
    base_score = scenario["max_score"]
    correct_ratio = len(correct_matches) / len(correct_services) if correct_services else 0
    penalty = len(incorrect_services) * 10  # 余分なサービス1つにつき10点減点
    
    final_score = max(0, int(base_score * correct_ratio - penalty))
    
    # グレード判定
    grade_thresholds = [
        (0.9, "S", "🌟 素晴らしい！完璧に近いアーキテクチャです。"),
        (0.7, "A", "👏 とても良いアーキテクチャです。"),
        (0.5, "B", "👍 良いアーキテクチャですが、改善の余地があります。"),
        (0.3, "C", "📚 基本的な要件は満たしていますが、重要な要素が不足しています。"),
        (0.0, "D", "🔄 アーキテクチャの見直しが必要です。")
    ]
    
    grade, comment = next(
        (grade, comment) for threshold, grade, comment in grade_thresholds 
        if correct_ratio >= threshold
    )
    
    return {
        "score": final_score,
        "max_score": base_score,
        "grade": grade,
        "comment": comment,
        "correct_services": list(correct_matches),
        "incorrect_services": list(incorrect_services),
        "missed_services": list(missed_services),
        "correct_ratio": round(correct_ratio * 100, 1),
        "penalty": penalty,
        "analysis": {
            "total_selected": len(selected_services_set),
            "total_correct": len(correct_services),
            "matches": len(correct_matches),
            "extras": len(incorrect_services),
            "missing": len(missed_services)
        }
    }
```

### 3. 入力検証システム

```python
def validate_service_input(selected_input: str, available_services: Dict[str, List[str]]) -> Optional[List[str]]:
    """
    ユーザー入力の検証とサニタイゼーション
    
    処理フロー:
    1. 入力文字列の分割とトリミング
    2. 利用可能サービスとの照合
    3. 不正なサービスの検出
    4. ユーザー確認（Yes/No）
    5. 最終的なサービスリストの返却
    """
    # 全ての利用可能なサービスのフラットリスト作成
    all_services = []
    for category_services in available_services.values():
        all_services.extend(category_services)
    
    # 入力の分割とサニタイゼーション
    selected_services = [
        service.strip() 
        for service in selected_input.split(",") 
        if service.strip()
    ]
    
    # 重複除去（順序保持）
    seen = set()
    unique_services = []
    for service in selected_services:
        if service not in seen:
            seen.add(service)
            unique_services.append(service)
    
    # 不正なサービスの検出
    unknown_services = [
        service for service in unique_services 
        if service not in all_services
    ]
    
    if unknown_services:
        print(f"\n⚠️  以下のサービスは提案リストにありません:")
        for service in unknown_services:
            print(f"  • {service}")
        
        # ユーザー確認ループ
        while True:
            confirm = input("\nこれらのサービスを含めて続行しますか？ (Yes/No): ").strip().lower()
            
            if confirm in ['yes', 'y', 'はい']:
                return unique_services
            elif confirm in ['no', 'n', 'いいえ']:
                print("サービス選択をやり直してください。")
                return None
            else:
                print("❌ 'Yes' または 'No' で答えてください。")
    
    return unique_services
```

## 🎮 ゲームエンジン設計

### 状態管理

```python
class QuizGame:
    """ゲーム状態管理クラス"""
    
    def __init__(self):
        self.score = 0
        self.level = 1
        self.current_scenario = None
        self.player_name = ""
        self.game_history = []
        
    def start_game(self, player_name: str):
        """ゲーム開始"""
        self.player_name = player_name
        self.score = 0
        self.level = 1
        self.game_history = []
        
    def add_result(self, scenario_id: int, score: int, services: List[str]):
        """結果を履歴に追加"""
        result = {
            "scenario_id": scenario_id,
            "score": score,
            "services": services,
            "timestamp": datetime.now().isoformat()
        }
        self.game_history.append(result)
        self.score += score
        
    def get_total_score(self) -> int:
        """総スコア取得"""
        return sum(result["score"] for result in self.game_history)
```

### エラーハンドリング

```python
def safe_input(prompt: str, validator=None, error_message: str = "無効な入力です。") -> str:
    """安全な入力取得"""
    while True:
        try:
            user_input = input(prompt).strip()
            if validator and not validator(user_input):
                print(f"❌ {error_message}")
                continue
            return user_input
        except KeyboardInterrupt:
            print("\n\n👋 ゲームを終了します。")
            sys.exit(0)
        except EOFError:
            print("\n\n❌ 入力エラーが発生しました。")
            sys.exit(1)

def validate_scenario_choice(choice: str) -> bool:
    """シナリオ選択の検証"""
    if choice.lower() == 'q':
        return True
    try:
        num = int(choice)
        return 1 <= num <= len(SCENARIOS)
    except ValueError:
        return False
```

## 🧪 テスト戦略

### 単体テスト

```python
import unittest
from demo_game import evaluate_architecture, check_architecture_cost

class TestGameLogic(unittest.TestCase):
    
    def test_perfect_score(self):
        """完璧な回答のテスト"""
        correct_services = ["EC2", "ALB", "Auto Scaling", "RDS", "S3", "CloudFront", "ACM"]
        result = evaluate_architecture(correct_services, 1)
        
        self.assertEqual(result["score"], 100)
        self.assertEqual(result["grade"], "S")
        self.assertEqual(result["correct_ratio"], 100.0)
        
    def test_partial_score(self):
        """部分的な回答のテスト"""
        partial_services = ["EC2", "RDS", "S3"]  # 3/7 正解
        result = evaluate_architecture(partial_services, 1)
        
        self.assertLess(result["score"], 100)
        self.assertEqual(len(result["correct_services"]), 3)
        self.assertEqual(len(result["missed_services"]), 4)
        
    def test_cost_calculation(self):
        """コスト計算のテスト"""
        services = ["EC2", "RDS", "S3"]
        result = check_architecture_cost(services)
        
        self.assertGreater(result["total_monthly_cost"], 0)
        self.assertEqual(len(result["cost_breakdown"]), 3)
        self.assertEqual(result["currency"], "USD")

if __name__ == "__main__":
    unittest.main()
```

### 統合テスト

```python
def test_full_game_flow():
    """完全なゲームフローのテスト"""
    # シミュレートされた入力
    inputs = [
        "テストプレイヤー",  # プレイヤー名
        "1",                 # シナリオ選択
        "EC2, RDS, S3",     # サービス選択
        "n"                  # 続行しない
    ]
    
    # 入力をモック
    with patch('builtins.input', side_effect=inputs):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            
            # 期待される出力の確認
            assert "テストプレイヤー" in output
            assert "評価結果" in output
            assert "コスト分析" in output
```

## 🔒 セキュリティ考慮事項

### 入力サニタイゼーション

```python
def sanitize_service_name(service: str) -> str:
    """サービス名のサニタイゼーション"""
    # 英数字、ハイフン、スペースのみ許可
    import re
    sanitized = re.sub(r'[^a-zA-Z0-9\-\s]', '', service)
    return sanitized.strip()

def validate_player_name(name: str) -> bool:
    """プレイヤー名の検証"""
    if not name or len(name) > 50:
        return False
    # 基本的な文字のみ許可
    import re
    return bool(re.match(r'^[a-zA-Z0-9\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF\s\-_]+$', name))
```

### エラー処理

```python
def safe_execute_tool(tool_func, *args, **kwargs):
    """ツール実行の安全なラッパー"""
    try:
        return tool_func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Tool execution failed: {tool_func.__name__}, Error: {str(e)}")
        return {
            "error": "処理中にエラーが発生しました。",
            "details": str(e) if DEBUG else None
        }
```

## 📊 パフォーマンス最適化

### メモリ使用量の最適化

```python
# 大きなデータ構造の遅延読み込み
class LazyServiceCosts:
    def __init__(self):
        self._costs = None
    
    @property
    def costs(self):
        if self._costs is None:
            self._costs = self._load_service_costs()
        return self._costs
    
    def _load_service_costs(self):
        # 実際のコストデータの読み込み
        return {...}
```

### レスポンス時間の改善

```python
# キャッシュ機能
from functools import lru_cache

@lru_cache(maxsize=128)
def get_service_recommendations(requirements_tuple):
    """要件に基づくサービス推奨（キャッシュ付き）"""
    requirements = list(requirements_tuple)
    return _calculate_recommendations(requirements)
```

## 🚀 デプロイメント

### Docker化

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "demo_game.py"]
```

### 環境変数設定

```bash
# AWS認証情報
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1

# Bedrock設定
export BEDROCK_REGION=us-west-2
export BEDROCK_MODEL_ID=us.anthropic.claude-3-7-sonnet-20250219-v1:0

# ゲーム設定
export GAME_DEBUG=false
export GAME_LOG_LEVEL=INFO
```

## 📈 監視とログ

### ログ設定

```python
import logging

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('game.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# ゲームイベントのログ
def log_game_event(event_type: str, player: str, data: dict):
    """ゲームイベントのログ記録"""
    logger.info(f"GAME_EVENT: {event_type} | Player: {player} | Data: {data}")
```

## 🔮 将来の拡張

### プラグインシステム

```python
class GamePlugin:
    """ゲームプラグインの基底クラス"""
    
    def __init__(self, name: str):
        self.name = name
    
    def on_game_start(self, player_name: str):
        """ゲーム開始時のフック"""
        pass
    
    def on_scenario_complete(self, result: dict):
        """シナリオ完了時のフック"""
        pass

class LeaderboardPlugin(GamePlugin):
    """リーダーボード機能"""
    
    def on_scenario_complete(self, result: dict):
        self.update_leaderboard(result)
```

### API化

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class GameRequest(BaseModel):
    player_name: str
    scenario_id: int
    selected_services: List[str]

@app.post("/evaluate")
async def evaluate_architecture_api(request: GameRequest):
    """アーキテクチャ評価API"""
    result = evaluate_architecture(
        request.selected_services, 
        request.scenario_id
    )
    return result
```

---

この技術詳解が、Strands Agentを使った教育ゲーム開発の参考になれば幸いです！
