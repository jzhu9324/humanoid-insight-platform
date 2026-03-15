#!/usr/bin/env python3
"""
生成首页最新更新数据

自动读取最新的论文、公司动态、行业资讯，生成首页显示的数据
"""

import os
import re
from pathlib import Path
from datetime import datetime
import json


def extract_frontmatter(content):
    """提取 markdown 文件的 frontmatter"""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}

    frontmatter = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip().strip('"\'')

    return frontmatter


def get_latest_files(directory, limit=3):
    """获取目录下最新的文件"""
    files = []

    if not directory.exists():
        return []

    for file_path in directory.glob('*.md'):
        if file_path.name == 'index.md':
            continue

        try:
            content = file_path.read_text(encoding='utf-8')
            frontmatter = extract_frontmatter(content)

            title = frontmatter.get('title', file_path.stem)
            date = frontmatter.get('date', '')

            # 提取第一个标题作为标题（如果 frontmatter 没有）
            if not title or title == file_path.stem:
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                if title_match:
                    title = title_match.group(1)

            files.append({
                'title': title,
                'date': date,
                'link': f'/{directory.name}/{file_path.stem}',
                'file_date': file_path.stat().st_mtime
            })
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            continue

    # 按日期排序
    files.sort(key=lambda x: x.get('date', '') or str(x['file_date']), reverse=True)

    return files[:limit]


def generate_latest_updates():
    """生成最新更新数据"""
    project_root = Path(__file__).parent.parent
    docs_dir = project_root / 'docs'

    # 获取最新内容
    latest_papers = get_latest_files(docs_dir / 'papers', limit=3)
    latest_company_news = get_latest_files(docs_dir / 'company-news', limit=3)
    latest_wechat = get_latest_files(docs_dir / 'wechat', limit=3)

    # 生成数据
    data = {
        'papers': latest_papers,
        'companyNews': latest_company_news,
        'wechat': latest_wechat,
        'updated_at': datetime.now().isoformat()
    }

    # 保存到 JSON 文件
    output_file = docs_dir / 'public' / 'latest-updates.json'
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✓ 已生成最新更新数据: {output_file}")
    print(f"  - 论文: {len(latest_papers)} 篇")
    print(f"  - 公司动态: {len(latest_company_news)} 条")
    print(f"  - 行业资讯: {len(latest_wechat)} 篇")

    return data


if __name__ == '__main__':
    generate_latest_updates()
