# Azure DevOps Wiki Restructure Tool

このプロジェクトは、Azure DevOps Wiki のディレクトリ構成を再設計するためのツールです。現在の Wiki 構成と要約をもとに、拡張性と保守性の高い情報設計を提案します。

## 主な機能

1. **Wiki 構成と要約の抽出**
   - `extract_wiki_summary.py` を使用して、指定された Wiki ディレクトリから現在の構成と要約を抽出します。

2. **プロンプトの生成**
   - 抽出した情報をもとに、Azure OpenAI に送信するプロンプトを生成します。

3. **Azure OpenAI との連携**
   - Azure OpenAI サービスを使用して、再設計されたディレクトリ構成を生成します。

4. **結果の保存**
   - 提案された構成を `wiki_restructure_suggestion.txt` に保存します。

## 必要な環境

- Python 3.11 以上
- Azure OpenAI サービス
- `.env` ファイルに以下の環境変数を設定してください:
  - `AZURE_OPENAI_ENDPOINT`: Azure OpenAI のエンドポイント
  - `AZURE_OPENAI_KEY`: Azure OpenAI の API キー
  - `AZURE_OPENAI_DEPLOYMENT`: 使用するモデルのデプロイ名 (例: `gpt-4`)

## 使用方法

1. 必要な Python パッケージをインストールします。

   ```bash
   pip install -r requirements.txt
   ```

2. Wiki ディレクトリを指定してスクリプトを実行します。

   ```bash
   python main.py
   ```

3. 結果は `wiki_restructure_suggestion.txt` に保存されます。

## ファイル構成

- `main.py`: メインスクリプト。
- `extract_wiki_summary.py`: Wiki 構成と要約を抽出するモジュール。
- `wiki/`: サンプルの Wiki ディレクトリ。
- `wiki_restructure_suggestion.txt`: 提案された構成が保存されるファイル。

## 注意事項

- Azure OpenAI サービスを利用するため、適切なサブスクリプションとリソースが必要です。
- 提案された構成はあくまで参考です。実際の運用に適用する前に十分な確認を行ってください。

## ライセンス

このプロジェクトは [MIT ライセンス](./LICENSE) のもとで公開されています。
