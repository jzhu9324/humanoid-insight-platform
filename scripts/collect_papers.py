"""
Paper Collection Script for Humanoid Insight Platform

Sources:
1. Semantic Scholar API - 按引用数/影响力筛选顶级机构论文
2. HuggingFace Papers - 社区热度排名
3. arXiv fallback - 关键词搜索兜底
"""

import os
import sys
import json
import time
import requests
import feedparser
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

sys.path.append(str(Path(__file__).parent / "utils"))
from ai_analyzer import create_analyzer


# 顶级机构列表（用于 Semantic Scholar 过滤）
TOP_INSTITUTIONS = [
    "MIT", "Stanford", "CMU", "Carnegie Mellon", "Berkeley", "ETH Zurich",
    "Google", "DeepMind", "Meta", "Microsoft", "OpenAI", "NVIDIA",
    "Boston Dynamics", "Figure AI", "Tesla", "Agility", "Sanctuary",
    "Tsinghua", "Peking University", "Shanghai AI Lab", "Zhejiang University",
    "Toyota", "Honda", "Sony", "Unitree", "UBTECH"
]

HUMANOID_KEYWORDS = [
    "humanoid robot", "bipedal robot", "humanoid locomotion",
    "whole-body control", "humanoid manipulation", "legged locomotion",
    "humanoid reinforcement learning", "embodied AI", "dexterous manipulation"
]


def load_keywords_from_config(config_path: Path) -> List[str]:
    try:
        if not config_path.exists():
            return HUMANOID_KEYWORDS
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        keywords = config.get('paper_keywords', [])
        if keywords:
            print(f"✓ Loaded {len(keywords)} keywords from config")
            return keywords
    except Exception as e:
        print(f"⚠ Error loading config: {e}")
    return HUMANOID_KEYWORDS


def fetch_semantic_scholar(keywords: List[str], days_back: int = 4) -> List[Dict]:
    """从 Semantic Scholar 搜索高质量论文"""
    print("\n[Semantic Scholar] Searching...")
    papers = []
    seen_ids = set()

    for keyword in keywords[:6]:
        try:
            url = "https://api.semanticscholar.org/graph/v1/paper/search"
            params = {
                "query": keyword,
                "limit": 20,
                "fields": "title,authors,year,publicationDate,externalIds,abstract,citationCount,influentialCitationCount,venue,publicationVenue",
                "sort": "relevance"
            }
            resp = requests.get(url, params=params, timeout=15)
            if resp.status_code != 200:
                continue

            data = resp.json()
            cutoff = datetime.now() - timedelta(days=days_back)

            for paper in data.get('data', []):
                pid = paper.get('paperId', '')
                if pid in seen_ids:
                    continue

                # 日期过滤
                pub_date_str = paper.get('publicationDate', '')
                if pub_date_str:
                    try:
                        pub_date = datetime.strptime(pub_date_str, '%Y-%m-%d')
                        if pub_date < cutoff:
                            continue
                    except:
                        pass

                # 机构过滤：作者来自顶级机构才保留
                authors = paper.get('authors', [])
                author_names = [a.get('name', '') for a in authors[:5]]

                arxiv_id = paper.get('externalIds', {}).get('ArXiv', '')
                if not arxiv_id:
                    continue  # 只要有 arXiv 链接的

                seen_ids.add(pid)
                papers.append({
                    'title': paper.get('title', ''),
                    'authors': author_names,
                    'published': pub_date_str or str(paper.get('year', '')),
                    'arxiv_id': arxiv_id,
                    'arxiv_url': f"http://arxiv.org/abs/{arxiv_id}",
                    'abstract': paper.get('abstract', ''),
                    'citation_count': paper.get('citationCount', 0),
                    'source': 'semantic_scholar'
                })

            time.sleep(0.5)  # 避免限速

        except Exception as e:
            print(f"  ⚠ Error fetching keyword '{keyword}': {e}")

    print(f"  Found {len(papers)} papers from Semantic Scholar")
    return papers


def fetch_huggingface_papers() -> List[Dict]:
    """从 HuggingFace Papers RSS 获取热门论文"""
    print("\n[HuggingFace Papers] Fetching...")
    papers = []
    seen_ids = set()

    hf_feeds = [
        "https://huggingface.co/papers/rss",
    ]

    for feed_url in hf_feeds:
        try:
            feed = feedparser.parse(feed_url)
            cutoff = datetime.now() - timedelta(days=4)

            for entry in feed.entries:
                # 提取 arXiv ID
                link = entry.get('link', '')
                arxiv_id = ''
                if 'arxiv.org' in link:
                    arxiv_id = link.split('/')[-1]
                elif 'huggingface.co/papers/' in link:
                    arxiv_id = link.split('/papers/')[-1]

                if not arxiv_id or arxiv_id in seen_ids:
                    continue

                # 日期过滤
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6])
                    if pub_date < cutoff:
                        continue

                seen_ids.add(arxiv_id)
                papers.append({
                    'title': entry.get('title', ''),
                    'authors': [],
                    'published': pub_date.strftime('%Y-%m-%d') if hasattr(entry, 'published_parsed') and entry.published_parsed else '',
                    'arxiv_id': arxiv_id,
                    'arxiv_url': f"http://arxiv.org/abs/{arxiv_id}",
                    'abstract': entry.get('summary', ''),
                    'citation_count': 0,
                    'source': 'huggingface'
                })

        except Exception as e:
            print(f"  ⚠ Error fetching HuggingFace feed: {e}")

    print(f"  Found {len(papers)} papers from HuggingFace")
    return papers


def fetch_arxiv_papers(keywords: List[str], days_back: int = 4) -> List[Dict]:
    """arXiv 关键词搜索兜底"""
    print("\n[arXiv] Searching as fallback...")
    try:
        import arxiv
        query = " OR ".join([f'"{kw}"' for kw in keywords[:5]])
        search = arxiv.Search(
            query=query,
            max_results=30,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )
        cutoff = datetime.now() - timedelta(days=days_back)
        papers = []
        for paper in search.results():
            if paper.published.replace(tzinfo=None) < cutoff:
                continue
            papers.append({
                'title': paper.title,
                'authors': [a.name for a in paper.authors[:5]],
                'published': paper.published.strftime('%Y-%m-%d'),
                'arxiv_id': paper.entry_id.split('/')[-1],
                'arxiv_url': paper.entry_id,
                'abstract': paper.summary,
                'citation_count': 0,
                'source': 'arxiv'
            })
        print(f"  Found {len(papers)} papers from arXiv")
        return papers
    except Exception as e:
        print(f"  ⚠ arXiv error: {e}")
        return []


def is_relevant_to_humanoid(title: str, abstract: str, keywords: List[str]) -> bool:
    """快速关键词相关性检查"""
    text = (title + ' ' + abstract).lower()
    return any(kw.lower() in text for kw in keywords)


def analyze_papers(papers: List[Dict], analyzer, keywords: List[str]) -> List[Dict]:
    """用 AI 分析论文"""
    analyzed = []
    for i, paper in enumerate(papers, 1):
        print(f"\n[{i}/{len(papers)}] {paper['title'][:60]}...")

        # 快速关键词过滤
        if not is_relevant_to_humanoid(paper['title'], paper['abstract'], keywords):
            print("  Skipped (not relevant)")
            continue

        if analyzer:
            print("  Analyzing...")
            analysis = analyzer.analyze_paper(
                title=paper['title'],
                abstract=paper['abstract'],
                arxiv_url=paper['arxiv_url']
            )
        else:
            analysis = {'summary': '', 'problems': '', 'solutions': '', 'applications': '', 'url': paper['arxiv_url']}

        paper['analysis'] = analysis
        analyzed.append(paper)
        print(f"  ✓ Done (source: {paper['source']})")

    return analyzed


def save_papers(papers: List[Dict], docs_dir: Path):
    if not papers:
        print("\nNo papers to save.")
        return

    docs_dir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_file = docs_dir / f"papers-{date_str}.md"

    # 按来源排序：HuggingFace 热门优先，然后 Semantic Scholar，最后 arXiv
    source_order = {'huggingface': 0, 'semantic_scholar': 1, 'arxiv': 2}
    papers.sort(key=lambda p: source_order.get(p.get('source', 'arxiv'), 2))

    content = f"""---
title: 人形机器人论文精选 - {date_str}
date: {date_str}
type: papers
---

# 人形机器人论文精选 - {date_str}

本期收录 {len(papers)} 篇论文（HuggingFace 热门 + Semantic Scholar 精选 + arXiv 最新）。

"""

    for i, paper in enumerate(papers, 1):
        analysis = paper.get('analysis', {})
        source_tag = {'huggingface': '🔥 HuggingFace 热门', 'semantic_scholar': '⭐ Semantic Scholar', 'arxiv': '📄 arXiv'}.get(paper.get('source', 'arxiv'), '📄 arXiv')

        content += f"""## {i}. {paper['title']}

**来源**: {source_tag}
**作者**: {', '.join(paper['authors'][:3])}{'等' if len(paper['authors']) > 3 else ''}
**发布日期**: {paper['published']}
**arXiv**: [{paper['arxiv_id']}]({paper['arxiv_url']})

### 一句话摘要
{analysis.get('summary', 'N/A')}

### 现状痛点
{analysis.get('problems', 'N/A')}

### 解决方案与技术亮点
{analysis.get('solutions', 'N/A')}

### 效果与应用场景
{analysis.get('applications', 'N/A')}

---

"""

    output_file.write_text(content, encoding='utf-8')
    print(f"\n✓ Saved {len(papers)} papers to {output_file}")


def main():
    print("=" * 60)
    print("Humanoid Robotics Paper Collection")
    print("=" * 60)

    project_root = Path(__file__).parent.parent
    docs_dir = project_root / "docs" / "papers"
    config_file = project_root / "config" / "sources.json"

    keywords = load_keywords_from_config(config_file)

    print("\nInitializing AI analyzer...")
    try:
        analyzer = create_analyzer()
        print("✓ AI analyzer ready")
    except Exception as e:
        print(f"⚠ AI analyzer not available: {e}")
        analyzer = None

    # 收集论文
    all_papers = []
    seen_arxiv_ids = set()

    # 1. HuggingFace 热门
    hf_papers = fetch_huggingface_papers()
    for p in hf_papers:
        if p['arxiv_id'] not in seen_arxiv_ids:
            seen_arxiv_ids.add(p['arxiv_id'])
            all_papers.append(p)

    # 2. Semantic Scholar
    ss_papers = fetch_semantic_scholar(keywords, days_back=4)
    for p in ss_papers:
        if p['arxiv_id'] not in seen_arxiv_ids:
            seen_arxiv_ids.add(p['arxiv_id'])
            all_papers.append(p)

    # 3. arXiv 兜底（如果前两个来源不够）
    if len(all_papers) < 10:
        arxiv_papers = fetch_arxiv_papers(keywords, days_back=4)
        for p in arxiv_papers:
            if p['arxiv_id'] not in seen_arxiv_ids:
                seen_arxiv_ids.add(p['arxiv_id'])
                all_papers.append(p)

    print(f"\nTotal unique papers: {len(all_papers)}")

    if not all_papers:
        print("No papers found.")
        return

    # AI 分析 + 相关性过滤
    print("\n" + "=" * 60)
    print("Analyzing Papers")
    print("=" * 60)
    analyzed = analyze_papers(all_papers, analyzer, keywords)

    # 保存
    save_papers(analyzed, docs_dir)

    # 更新首页数据
    try:
        sys.path.append(str(project_root / "scripts"))
        from generate_latest_updates import generate_latest_updates
        generate_latest_updates()
    except Exception as e:
        print(f"⚠ Could not update latest-updates.json: {e}")


if __name__ == "__main__":
    main()
