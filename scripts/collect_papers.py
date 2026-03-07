"""
Paper Collection Script for Humanoid Insight Platform

This script:
1. Searches arXiv for humanoid robotics papers
2. Scores relevance using AI analyzer
3. Performs deep analysis on highly relevant papers
4. Saves results in VitePress-compatible format
"""

import os
import sys
import json
import yaml
import arxiv
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict

# Add utils directory to path for imports
sys.path.append(str(Path(__file__).parent / "utils"))
from ai_analyzer import create_analyzer


# Keywords for humanoid robotics research
HUMANOID_KEYWORDS = [
    "humanoid robot",
    "bipedal robot",
    "humanoid locomotion",
    "whole-body control",
    "humanoid manipulation",
    "human-robot interaction",
    "legged locomotion",
    "biped walking",
    "humanoid learning",
    "humanoid reinforcement learning"
]

# Relevance threshold (0.0 to 1.0)
# Set to 0.0 to analyze all papers since arXiv search already filters by relevant keywords
RELEVANCE_THRESHOLD = 0.0


def search_arxiv_papers(query: str, max_results: int = 50, days_back: int = 7) -> List[arxiv.Result]:
    """
    Search arXiv for recent papers.

    Args:
        query: Search query string
        max_results: Maximum number of results to return
        days_back: How many days back to search

    Returns:
        List of arXiv paper results
    """
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)

    print(f"Searching arXiv for papers from {start_date.date()} to {end_date.date()}...")

    # Create search
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )

    # Fetch results
    results = list(search.results())
    print(f"Found {len(results)} papers")

    return results


def filter_and_analyze_papers(papers: List[arxiv.Result], analyzer) -> List[Dict]:
    """
    Filter papers by relevance and analyze relevant ones.

    Args:
        papers: List of arXiv paper results
        analyzer: AI analyzer instance

    Returns:
        List of analyzed papers with metadata
    """
    analyzed_papers = []

    for i, paper in enumerate(papers, 1):
        print(f"\n[{i}/{len(papers)}] Processing: {paper.title}")

        # Score relevance
        relevance_score = analyzer.score_relevance(
            title=paper.title,
            abstract=paper.summary,
            keywords=HUMANOID_KEYWORDS
        )

        print(f"  Relevance score: {relevance_score:.2f}")

        # Skip low-relevance papers
        if relevance_score < RELEVANCE_THRESHOLD:
            print(f"  Skipped (below threshold {RELEVANCE_THRESHOLD})")
            continue

        # Perform deep analysis for relevant papers
        print("  Performing deep analysis...")
        analysis = analyzer.analyze_paper(
            title=paper.title,
            abstract=paper.summary,
            arxiv_url=paper.entry_id
        )

        # Compile paper data
        paper_data = {
            "title": paper.title,
            "authors": [author.name for author in paper.authors],
            "published": paper.published.strftime("%Y-%m-%d"),
            "arxiv_id": paper.entry_id.split("/")[-1],
            "arxiv_url": paper.entry_id,
            "pdf_url": paper.pdf_url,
            "relevance_score": round(relevance_score, 2),
            "categories": paper.categories,
            "analysis": analysis
        }

        analyzed_papers.append(paper_data)
        print(f"  ✓ Analyzed and saved")

    return analyzed_papers


def save_papers_to_markdown(papers: List[Dict], output_dir: Path):
    """
    Save analyzed papers to markdown files for VitePress.

    Args:
        papers: List of analyzed paper data
        output_dir: Directory to save markdown files
    """
    if not papers:
        print("\nNo papers to save.")
        return

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename with date
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_file = output_dir / f"papers-{date_str}.md"

    # Build markdown content
    content = f"""---
title: 人形机器人论文精选 - {date_str}
date: {date_str}
type: papers
---

# 人形机器人论文精选 - {date_str}

本期收录 {len(papers)} 篇高质量论文。

"""

    for i, paper in enumerate(papers, 1):
        analysis = paper["analysis"]

        content += f"""## {i}. {paper['title']}

**作者**: {', '.join(paper['authors'][:3])}{'等' if len(paper['authors']) > 3 else ''}
**发布日期**: {paper['published']}
**arXiv**: [{paper['arxiv_id']}]({paper['arxiv_url']})
**相关性**: {paper['relevance_score']}

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

    # Write to file
    output_file.write_text(content, encoding='utf-8')
    print(f"\n✓ Saved {len(papers)} papers to {output_file}")


def save_papers_to_json(papers: List[Dict], output_dir: Path):
    """
    Save analyzed papers to JSON for backup/processing.

    Args:
        papers: List of analyzed paper data
        output_dir: Directory to save JSON file
    """
    if not papers:
        return

    # Create cache directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename with date
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_file = output_dir / f"papers-{date_str}.json"

    # Write JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)

    print(f"✓ Saved JSON backup to {output_file}")


def main():
    """Main execution function."""
    print("=" * 60)
    print("Humanoid Robotics Paper Collection")
    print("=" * 60)

    # Setup paths
    project_root = Path(__file__).parent.parent
    docs_dir = project_root / "docs" / "papers"
    cache_dir = project_root / "cache" / "papers"

    # Initialize AI analyzer
    print("\nInitializing AI analyzer...")
    try:
        analyzer = create_analyzer()
        print("✓ AI analyzer ready")
    except Exception as e:
        print(f"✗ Failed to initialize analyzer: {e}")
        print("Please ensure ANTHROPIC_API_KEY environment variable is set.")
        sys.exit(1)

    # Search arXiv (半周更新：3-4天)
    query = " OR ".join([f'"{kw}"' for kw in HUMANOID_KEYWORDS[:5]])
    papers = search_arxiv_papers(query, max_results=30, days_back=4)

    if not papers:
        print("\nNo papers found.")
        return

    # Filter and analyze papers
    print("\n" + "=" * 60)
    print("Filtering and Analyzing Papers")
    print("=" * 60)

    analyzed_papers = filter_and_analyze_papers(papers, analyzer)

    # Save results
    print("\n" + "=" * 60)
    print("Saving Results")
    print("=" * 60)

    save_papers_to_markdown(analyzed_papers, docs_dir)
    save_papers_to_json(analyzed_papers, cache_dir)

    print("\n" + "=" * 60)
    print(f"✓ Collection complete! Processed {len(analyzed_papers)} relevant papers.")
    print("=" * 60)


if __name__ == "__main__":
    main()
