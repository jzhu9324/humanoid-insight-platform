#!/usr/bin/env python3
"""
生成首页最新更新数据 - 提取具体文章标题和摘要
"""

import re
from pathlib import Path
from datetime import datetime
import json


def extract_items_from_md(file_path: Path, file_type: str, limit: int = 5):
    """从 markdown 文件中提取具体条目"""
    items = []
    try:
        content = file_path.read_text(encoding='utf-8')

        if file_type == 'papers':
            # 提取论文：标题 + 一句话摘要
            blocks = re.split(r'\n---\n', content)
            for block in blocks:
                title_match = re.search(r'^## \d+\.\s+(.+)$', block, re.MULTILINE)
                summary_match = re.search(r'### 一句话摘要\s*\n(.+)', block)
                date_match = re.search(r'\*\*发布日期\*\*:\s*(\S+)', block)
                link_match = re.search(r'\*\*arXiv\*\*:.*?\((.+?)\)', block)

                if title_match:
                    items.append({
                        'title': title_match.group(1).strip(),
                        'summary': summary_match.group(1).strip() if summary_match else '',
                        'date': date_match.group(1) if date_match else '',
                        'link': link_match.group(1) if link_match else ''
                    })
                if len(items) >= limit:
                    break

        elif file_type == 'company-news':
            # 提取公司动态：标题 + 摘要
            blocks = re.split(r'\n---\n', content)
            for block in blocks:
                title_match = re.search(r'^### (.+)$', block, re.MULTILINE)
                date_match = re.search(r'\*\*发布日期\*\*:\s*(\S+)', block)
                link_match = re.search(r'\[查看原文\]\((.+?)\)', block)
                # 摘要是链接后面的第一段文字
                summary_match = re.search(r'\[查看原文\]\(.+?\)\s*\n+(.+)', block)

                if title_match and title_match.group(1).strip() not in ('', '---'):
                    items.append({
                        'title': title_match.group(1).strip(),
                        'summary': summary_match.group(1).strip()[:100] if summary_match else '',
                        'date': date_match.group(1) if date_match else '',
                        'link': link_match.group(1) if link_match else ''
                    })
                if len(items) >= limit:
                    break

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

    return items


def get_latest_from_dir(directory: Path, file_type: str, limit: int = 5):
    """获取目录下最新文件中的条目"""
    if not directory.exists():
        return []

    # 找最新的非 index 文件
    files = sorted(
        [f for f in directory.glob('*.md') if f.name != 'index.md'],
        key=lambda f: f.stem,
        reverse=True
    )

    if not files:
        return []

    return extract_items_from_md(files[0], file_type, limit)


def generate_latest_updates():
    project_root = Path(__file__).parent.parent
    docs_dir = project_root / 'docs'

    data = {
        'papers': get_latest_from_dir(docs_dir / 'papers', 'papers', limit=5),
        'companyNews': get_latest_from_dir(docs_dir / 'company-news', 'company-news', limit=5),
        'wechat': get_latest_from_dir(docs_dir / 'wechat', 'wechat', limit=5),
        'updated_at': datetime.now().isoformat()
    }

    output_file = docs_dir / 'public' / 'latest-updates.json'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✓ 已生成最新更新数据")
    print(f"  - 论文: {len(data['papers'])} 篇")
    print(f"  - 公司动态: {len(data['companyNews'])} 条")
    print(f"  - 行业资讯: {len(data['wechat'])} 篇")
    return data


if __name__ == '__main__':
    generate_latest_updates()
