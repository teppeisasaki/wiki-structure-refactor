import os
from openai import AzureOpenAI

import dotenv

# 環境変数から設定を読み込む（.envファイルを用意しておくと便利）
dotenv.load_dotenv()
api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # 例: gpt-4
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"), api_version="2023-07-01-preview"
)

# --- 1. Markdown から構成と要約を抽出する ---
from extract_wiki_summary import walk_directory

wiki_root = "./wiki"
tree_output, summary_output = walk_directory(wiki_root)


# --- 2. プロンプトを組み立てる ---
def build_prompt(tree_text, summary_text):
    return f"""
以下は Azure DevOps Wiki の現在のページ構成と、各ページの要約です。

この情報をもとに、今後情報が増えても破綻しないようなディレクトリ構成に再設計してください。  
目的は「拡張性」と「保守性」の高い情報設計です。

---

【現在のWiki構成】
{tree_text}

---

【各ページの要約】
{summary_text}

---

【期待する出力フォーマット】

1. 新しいディレクトリ構成（tree形式）
2. 各ディレクトリ/カテゴリの簡単な説明（任意）
3. 移動や統合が必要なファイルがあれば、旧パス→新パスの提案
"""


# --- 3. Azure OpenAI に投げる ---
def call_openai(prompt):
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "あなたは情報設計の専門家です。"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=4000,
    )
    return response.choices[0].message.content


prompt = build_prompt(tree_output, summary_output)
llm_response = call_openai(prompt)

# --- 4. 結果を保存 ---
with open("wiki_restructure_suggestion.txt", "w", encoding="utf-8") as f:
    f.write(llm_response)

print("✅ 提案構成を wiki_restructure_suggestion.txt に保存しました。")
