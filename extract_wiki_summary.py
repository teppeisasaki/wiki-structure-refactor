import os


def extract_summary_from_markdown(file_path, max_paragraphs=3):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.readlines()

        title = ""
        summary_lines = []
        inside_code_block = False

        for line in content:
            stripped = line.strip()

            # コードブロックの開始/終了をトグル
            if stripped.startswith("```"):
                inside_code_block = not inside_code_block
                continue

            # 箇条書きやコードブロック内の内容はスキップ
            if inside_code_block or stripped.startswith(("- ", "* ", ">")):
                continue

            # h1 をタイトルとして取得
            if not title and stripped.startswith("# "):
                title = stripped.strip("# ").strip()
                continue

            # 最初の数段落を要約として取得
            if stripped:
                summary_lines.append(stripped)
            if len(summary_lines) >= max_paragraphs:
                break

        summary = " ".join(summary_lines).strip()
        return title or os.path.basename(file_path), summary or "(No summary)"
    except Exception as e:
        return os.path.basename(file_path), f"(Error: {e})"


def walk_directory(root_dir):
    structure_lines = []
    summaries = []

    def walk(dir_path, prefix=""):
        items = sorted(os.listdir(dir_path))
        for i, item in enumerate(items):
            path = os.path.join(dir_path, item)
            connector = "└── " if i == len(items) - 1 else "├── "
            structure_lines.append(f"{prefix}{connector}{item}")
            if os.path.isdir(path):
                new_prefix = prefix + ("    " if i == len(items) - 1 else "│   ")
                walk(path, new_prefix)
            elif item.endswith(".md"):
                title, summary = extract_summary_from_markdown(path)
                rel_path = os.path.relpath(path, root_dir)
                summaries.append(f"- {rel_path}: {title} — {summary}")

    walk(root_dir)
    return "\n".join(structure_lines), "\n".join(summaries)


if __name__ == "__main__":
    root = "./wiki"  # 必要に応じて Wiki のルートディレクトリに変更
    tree_output, summary_output = walk_directory(root)

    with open("wiki_structure.txt", "w", encoding="utf-8") as f:
        f.write("【Wiki 構成（tree 形式）】\n")
        f.write(tree_output)

    with open("wiki_summaries.txt", "w", encoding="utf-8") as f:
        f.write("【各ページの要約】\n")
        f.write(summary_output)

    print("出力完了: wiki_structure.txt / wiki_summaries.txt")
