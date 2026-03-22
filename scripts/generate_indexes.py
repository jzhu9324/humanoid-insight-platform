#!/usr/bin/env python3
"""
自动生成 papers、company-news、reports 的 index.md
"""

from pathlib import Path
import re


def generate_papers_index(docs_dir: Path):
    papers_dir = docs_dir / 'papers'
    files = sorted(
        [f for f in papers_dir.glob('*.md') if f.name != 'index.md'],
        key=lambda f: f.stem,
        reverse=True
    )

    lines = ['---', 'title: 学术论文', '---', '', '# 学术论文', '',
             '这里汇集了人形机器人领域的最新学术研究论文，每篇论文都经过 AI 深度解读。', '',
             '## 最新论文', '']

    for f in files:
        # 从文件名提取日期，如 papers-2026-03-22
        date = f.stem.replace('papers-', '')
        # 统计论文数量
        content = f.read_text(encoding='utf-8')
        count = len(re.findall(r'^## \d+\.', content, re.MULTILINE))
        label = f'{date} 论文精选' + (f' ({count}篇)' if count else '')
        lines.append(f'- [{label}](/papers/{f.stem})')

    lines += ['', '---', '', '*由 AI 提供深度分析*', '']
    (papers_dir / 'index.md').write_text('\n'.join(lines), encoding='utf-8')
    print(f'✓ 已更新 papers/index.md（{len(files)} 个文件）')


def generate_company_news_index(docs_dir: Path):
    news_dir = docs_dir / 'company-news'
    files = sorted(
        [f for f in news_dir.glob('*.md') if f.name != 'index.md'],
        key=lambda f: f.stem,
        reverse=True
    )

    lines = ['---', 'title: 公司动态', '---', '', '# 公司动态', '',
             '追踪全球领先的人形机器人公司最新动态和产品发布。', '',
             '## 最新动态', '']

    for f in files:
        date = f.stem.replace('company-news-', '')
        content = f.read_text(encoding='utf-8')
        count = len(re.findall(r'^### ', content, re.MULTILINE))
        label = f'{date} 公司动态' + (f' ({count}条)' if count else '')
        lines.append(f'- [{label}](/company-news/{f.stem})')

    lines += ['', '---', '', '*由 AI 提供智能分析和总结*', '']
    (news_dir / 'index.md').write_text('\n'.join(lines), encoding='utf-8')
    print(f'✓ 已更新 company-news/index.md（{len(files)} 个文件）')


def generate_reports_index(docs_dir: Path):
    reports_dir = docs_dir / 'reports'
    files = sorted(
        [f for f in reports_dir.glob('*.md') if f.name != 'index.md'],
        key=lambda f: f.stem,
        reverse=True
    )

    lines = ['---', 'title: 行业报告', '---', '', '# 行业报告', '',
             'AI 自动生成的日报，提供趋势分析和行业洞察。', '',
             '## 最新报告', '']

    for f in files:
        stem = f.stem
        if stem.startswith('daily-report-'):
            date = stem.replace('daily-report-', '')
            label = f'{date} 日报'
        elif stem.startswith('weekly-report-'):
            date = stem.replace('weekly-report-', '')
            label = f'{date} 周报'
        else:
            label = stem
        lines.append(f'- [{label}](/reports/{stem})')

    lines += ['', '---', '', '*由 AI 提供深度分析*', '']
    (reports_dir / 'index.md').write_text('\n'.join(lines), encoding='utf-8')
    print(f'✓ 已更新 reports/index.md（{len(files)} 个文件）')


if __name__ == '__main__':
    docs_dir = Path(__file__).parent.parent / 'docs'
    generate_papers_index(docs_dir)
    generate_company_news_index(docs_dir)
    generate_reports_index(docs_dir)
