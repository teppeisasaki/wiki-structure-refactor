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


# --- トークン数を計算する関数を追加 ---
def calculate_token_count(text):
    # トークン数を計算する簡易的な方法
    return len(text.split())


# --- ファイル一覧と概要を取得する関数を追加 ---
def get_file_list_and_summaries(directory):
    file_summaries = []
    for root, _, files in os.walk(directory):
        # wiki直下のattachmentsフォルダと.gitフォルダを無視
        if root == os.path.join(directory, "attachments") or root == os.path.join(
            directory, ".git"
        ):
            continue
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    summary = content[:200]  # ファイルの最初の200文字を概要として使用
                    file_summaries.append((file_path, summary))
            except (UnicodeDecodeError, FileNotFoundError) as e:
                print(f"⚠️ ファイルを処理中にエラーが発生しました: {file_path} - {e}")
    return file_summaries


# --- プロンプトを構築するロジックを変更 ---
def build_prompt_from_files(file_summaries):
    file_details = "\n".join(
        [f"- {path}: {summary}" for path, summary in file_summaries]
    )
    base_prompt = f"""
以下は現在のファイル一覧とそれぞれの概要です。

{file_details}

期待する出力:
1. 新しいフォルダ構成
2. 簡単な説明
3. ファイル移動提案
"""

    # トークン数を計算
    token_count = calculate_token_count(base_prompt)
    print(f"🔢 プロンプトのトークン数: {token_count}")

    return base_prompt


# --- デバッグ用にプロンプトをテキストファイルに出力 ---
def save_prompt_to_file(prompt, file_path="debug_prompt.txt"):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(prompt)
    print(f"✅ プロンプトを {file_path} に保存しました。")


# --- LLM 呼び出しのトークン数を最大化 ---
def call_openai(prompt):
    max_tokens_for_response = 4096 - calculate_token_count(
        prompt
    )  # 最大トークン数からプロンプトのトークン数を引く
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "あなたは情報設計の専門家です。"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=max_tokens_for_response,  # 動的に計算したトークン数を設定
        stream=True,  # ストリーミングを有効化
    )

    result = ""
    print("🔄 ストリーミング中...")
    for chunk in response:
        if hasattr(chunk, "choices") and chunk.choices:
            delta = chunk.choices[0].delta
            if hasattr(delta, "content"):
                content = delta.content
                if content is not None:
                    print(content, end="", flush=True)  # 途中結果を表示
                    result += content

    print("\n✅ ストリーミング完了")
    return result


wiki_root = "./wiki"

# --- ファイル一覧と概要を取得 ---
file_summaries = get_file_list_and_summaries(wiki_root)

# --- 新しいプロンプトを構築 ---
prompt = build_prompt_from_files(file_summaries)

# プロンプトを保存
save_prompt_to_file(prompt)

# --- LLM 呼び出し ---
llm_response = call_openai(prompt)

# --- 結果を保存 ---
with open("wiki_restructure_suggestion.txt", "w", encoding="utf-8") as f:
    f.write(llm_response)

print("✅ 提案構成を wiki_restructure_suggestion.txt に保存しました。")
