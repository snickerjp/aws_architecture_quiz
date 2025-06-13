# AWS認証情報の設定方法 / AWS Credentials Setup Guide

このドキュメントでは、AWS Architecture Quiz Masterを使用するために必要なAWS認証情報の設定方法を説明します。

## 🔑 AWS認証情報が必要な理由

AWS Architecture Quiz Masterは以下のAWSサービスを使用します：
- **Amazon Bedrock**: AIエージェント（Claude 3.7 Sonnet）による評価とフィードバック
- **AWS Pricing API**: サービスコストの計算（将来の機能）

## 📋 前提条件

1. **AWSアカウント**: 有効なAWSアカウントが必要です
2. **IAMユーザー**: プログラムアクセス用のIAMユーザーまたはロール
3. **Amazon Bedrockアクセス**: Claude 3.7 Sonnetモデルへのアクセス権限

## 🛠️ 設定方法

### 方法1: AWS CLI を使用した設定（推奨）

#### ステップ1: AWS CLIの確認
```bash
aws --version
```

#### ステップ2: AWS認証情報の設定
```bash
aws configure
```

以下の情報を入力してください：
```
AWS Access Key ID [None]: YOUR_ACCESS_KEY_ID
AWS Secret Access Key [None]: YOUR_SECRET_ACCESS_KEY
Default region name [None]: us-east-1
Default output format [None]: json
```

#### ステップ3: 設定の確認
```bash
aws sts get-caller-identity
```

成功すると以下のような出力が表示されます：
```json
{
    "UserId": "AIDACKCEVSQ6C2EXAMPLE",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/your-username"
}
```

### 方法2: 環境変数を使用した設定

```bash
export AWS_ACCESS_KEY_ID=your_access_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_access_key
export AWS_DEFAULT_REGION=us-east-1
```

### 方法3: 認証情報ファイルの直接編集

#### Linux/Mac:
```bash
mkdir -p ~/.aws
cat > ~/.aws/credentials << EOF
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
EOF

cat > ~/.aws/config << EOF
[default]
region = us-east-1
output = json
EOF
```

#### Windows:
```cmd
mkdir %USERPROFILE%\.aws
echo [default] > %USERPROFILE%\.aws\credentials
echo aws_access_key_id = YOUR_ACCESS_KEY_ID >> %USERPROFILE%\.aws\credentials
echo aws_secret_access_key = YOUR_SECRET_ACCESS_KEY >> %USERPROFILE%\.aws\credentials

echo [default] > %USERPROFILE%\.aws\config
echo region = us-east-1 >> %USERPROFILE%\.aws\config
echo output = json >> %USERPROFILE%\.aws\config
```

## 🔐 IAMユーザーの作成

### ステップ1: AWSコンソールにログイン
1. [AWS Management Console](https://console.aws.amazon.com/)にアクセス
2. IAMサービスに移動

### ステップ2: IAMユーザーの作成
1. 「ユーザー」→「ユーザーを追加」をクリック
2. ユーザー名を入力（例：`quiz-master-user`）
3. 「プログラムによるアクセス」を選択

### ステップ3: 権限の設定
以下のポリシーをアタッチしてください：

#### 最小権限ポリシー（推奨）:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:ListFoundationModels"
            ],
            "Resource": "*"
        }
    ]
}
```

#### または既存のポリシー:
- `AmazonBedrockFullAccess`（開発・テスト環境用）

### ステップ4: アクセスキーの取得
1. ユーザー作成完了後、「アクセスキー ID」と「シークレットアクセスキー」をメモ
2. **重要**: シークレットアクセスキーは一度しか表示されません

## 🎯 Amazon Bedrockの設定

### ステップ1: Bedrockコンソールにアクセス
1. [Amazon Bedrock Console](https://console.aws.amazon.com/bedrock/)にアクセス
2. 左側メニューから「Model access」を選択

### ステップ2: Claude 3.7 Sonnetモデルの有効化
1. 「Manage model access」をクリック
2. 「Anthropic」セクションを展開
3. 「Claude 3.7 Sonnet」にチェックを入れる
4. 「Request model access」をクリック

### ステップ3: アクセス承認の確認
- 通常、数分でアクセスが承認されます
- ステータスが「Access granted」になることを確認

## 🌍 リージョンの選択

Amazon Bedrockが利用可能なリージョンを選択してください：

### 推奨リージョン:
- **us-east-1** (バージニア北部) - 最も多くのモデルが利用可能
- **us-west-2** (オレゴン)
- **eu-west-1** (アイルランド)
- **ap-southeast-1** (シンガポール)

### リージョンの設定:
```bash
aws configure set region us-east-1
```

## 🧪 設定のテスト

### 基本的な接続テスト:
```bash
aws sts get-caller-identity
```

### Bedrockアクセステスト:
```bash
aws bedrock list-foundation-models --region us-east-1
```

### ゲームの実行テスト:
```bash
cd /workspaces/aws_architecture_quiz
python simple_multilingual_demo.py
```

## ❌ トラブルシューティング

### よくあるエラーと解決方法:

#### 1. `NoCredentialsError: Unable to locate credentials`
**原因**: AWS認証情報が設定されていない
**解決方法**: 
```bash
aws configure
```

#### 2. `AccessDeniedException: User is not authorized to perform: bedrock:InvokeModel`
**原因**: Bedrockへのアクセス権限がない
**解決方法**: 
- IAMポリシーにBedrock権限を追加
- Bedrockコンソールでモデルアクセスを有効化

#### 3. `ValidationException: The model ID provided is invalid`
**原因**: 指定したモデルが利用できない
**解決方法**: 
- Bedrockコンソールでモデルアクセスを確認
- 正しいリージョンを使用しているか確認

#### 4. `EndpointConnectionError`
**原因**: ネットワーク接続またはリージョンの問題
**解決方法**: 
```bash
aws configure set region us-east-1
```

## 💰 コストについて

### Amazon Bedrock料金:
- **Claude 3.7 Sonnet**: 入力トークン $3.00/1M、出力トークン $15.00/1M
- **典型的なクイズセッション**: 約$0.01-0.05程度

### コスト管理:
1. **予算アラート**の設定を推奨
2. **使用量モニタリング**でコストを追跡
3. **開発環境**では使用量を制限

## 🔒 セキュリティのベストプラクティス

### 1. 最小権限の原則
- 必要最小限の権限のみを付与
- 定期的な権限の見直し

### 2. アクセスキーの管理
- アクセスキーを共有しない
- 定期的なローテーション
- 不要になったキーは削除

### 3. 環境の分離
- 開発・本番環境で異なる認証情報を使用
- 環境変数での管理を推奨

## 📞 サポート

### 設定でお困りの場合:

1. **AWS公式ドキュメント**: 
   - [AWS CLI設定ガイド](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)
   - [Amazon Bedrockユーザーガイド](https://docs.aws.amazon.com/bedrock/latest/userguide/)

2. **ゲーム固有の問題**:
   - `test_game_functionality.py`を実行して問題を特定
   - エラーメッセージを確認

3. **代替手段**:
   - AWS認証情報なしでも`simple_multilingual_demo.py`は動作します
   - 基本的な機能テストには十分です

---

## クイックスタートチェックリスト

- [ ] AWSアカウントの作成
- [ ] IAMユーザーの作成とアクセスキー取得
- [ ] AWS CLIのインストールと設定
- [ ] Amazon Bedrockでのモデルアクセス有効化
- [ ] 設定テストの実行
- [ ] ゲームの動作確認

設定完了後、以下のコマンドでゲームを開始できます：
```bash
python multilingual_quiz_game.py
```
