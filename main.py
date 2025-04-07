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


# --- トークン使用量を削減するための修正 ---
def build_prompt(tree_text, summary_text):
    # プロンプトを簡略化
    return f"""
以下は現在のWiki構成と要約です。

【構成】
{tree_text}

【要約】
{summary_text}

期待する出力:
1. 新しい構成
2. 簡単な説明
3. ファイル移動提案
"""


# --- デバッグ用にプロンプトをテキストファイルに出力 ---
def save_prompt_to_file(prompt, file_path="debug_prompt.txt"):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(prompt)
    print(f"✅ プロンプトを {file_path} に保存しました。")


# --- max_tokens を削減 ---
def call_openai(prompt):
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "あなたは情報設計の専門家です。"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=2000,  # トークン数を削減
    )
    return response.choices[0].message.content


prompt = build_prompt(tree_output, summary_output)

# プロンプトを保存
save_prompt_to_file(prompt)

llm_response = call_openai(prompt)

# --- 4. 結果を保存 ---
with open("wiki_restructure_suggestion.txt", "w", encoding="utf-8") as f:
    f.write(llm_response)

print("✅ 提案構成を wiki_restructure_suggestion.txt に保存しました。")
