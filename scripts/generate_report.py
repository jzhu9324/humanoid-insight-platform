"""
Report Generation Script for Humanoid Insight Platform

This script:
1. Aggregates data from papers, company news, and WeChat articles
2. Generates daily/weekly reports with AI-powered insights
3. Creates VitePress-compatible markdown reports
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from collections import defaultdict

# Add utils directory to path for imports
sys.path.append(str(Path(__file__).parent / "utils"))
from ai_analyzer import create_analyzer


def load_json_data(file_path: Path) -> Optional[List[Dict]]:
    """
    Load data from JSON file.

    Args:
        file_path: Path to JSON file

    Returns:
        List of data items or None
    """
    if not file_path.exists():
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"  Error loading {file_path}: {e}")
        return None


def collect_recent_data(cache_dir: Path, days_back: int = 7) -> Dict[str, List[Dict]]:
    """
    Collect all recent data from cache.

    Args:
        cache_dir: Cache directory root
        days_back: How many days back to collect

    Returns:
        Dictionary with papers, company_news, and wechat_articles
    """
    print(f"\nCollecting data from the past {days_back} days...")

    data = {
        "papers": [],
        "company_news": [],
        "wechat_articles": []
    }

    # Generate date range
    dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days_back)]

    # Collect papers
    papers_dir = cache_dir / "papers"
    if papers_dir.exists():
        for date in dates:
            file_path = papers_dir / f"papers-{date}.json"
            papers = load_json_data(file_path)
            if papers:
                data["papers"].extend(papers)
                print(f"  ✓ Loaded {len(papers)} papers from {date}")

    # Collect company news
    news_dir = cache_dir / "company-news"
    if news_dir.exists():
        for date in dates:
            file_path = news_dir / f"company-news-{date}.json"
            news = load_json_data(file_path)
            if news:
                data["company_news"].extend(news)
                print(f"  ✓ Loaded {len(news)} company news items from {date}")

    # Collect WeChat articles
    wechat_dir = cache_dir / "wechat"
    if wechat_dir.exists():
        for date in dates:
            file_path = wechat_dir / f"wechat-articles-{date}.json"
            articles = load_json_data(file_path)
            if articles:
                data["wechat_articles"].extend(articles)
                print(f"  ✓ Loaded {len(articles)} WeChat articles from {date}")

    total_items = len(data["papers"]) + len(data["company_news"]) + len(data["wechat_articles"])
    print(f"\nTotal items collected: {total_items}")

    return data


def generate_executive_summary(data: Dict, analyzer) -> str:
    """
    Generate executive summary using AI.

    Args:
        data: Collected data dictionary
        analyzer: AI analyzer instance

    Returns:
        Executive summary text
    """
    print("\nGenerating executive summary with AI...")

    # Prepare summary of all data
    summary_text = f"""
我们收集了过去一周的人形机器人行业数据:
- 论文: {len(data['papers'])} 篇
- 公司动态: {len(data['company_news'])} 条
- 微信文章: {len(data['wechat_articles'])} 篇

主要论文标题:
{chr(10).join([f"- {p['title']}" for p in data['papers'][:5]])}

主要公司动态:
{chr(10).join([f"- {n['company']}: {n['title']}" for n in data['company_news'][:5]])}
"""

    prompt = f"""你是人形机器人行业的首席分析师。请基于以下数据，撰写一份简明的行业周报摘要（200-300字）。

{summary_text}

请包含以下内容:
1. 本周行业整体态势（1-2句）
2. 技术研究主要方向和突破（2-3句）
3. 主要公司动态和产业进展（2-3句）
4. 值得关注的趋势或信号（1-2句）

请使用简洁、专业的语言，突出关键信息。"""

    try:
        response = analyzer.client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}]
        )

        summary = response.content[0].text.strip()
        print("  ✓ Executive summary generated")
        return summary

    except Exception as e:
        print(f"  Error generating summary: {e}")
        return "本周收集了人形机器人领域的最新研究论文、公司动态和行业资讯。"


def generate_trend_analysis(data: Dict, analyzer) -> str:
    """
    Generate trend analysis using AI.

    Args:
        data: Collected data dictionary
        analyzer: AI analyzer instance

    Returns:
        Trend analysis text
    """
    print("\nGenerating trend analysis with AI...")

    # Extract key topics
    paper_titles = [p['title'] for p in data['papers']]
    news_titles = [f"{n['company']}: {n['title']}" for n in data['company_news']]

    prompt = f"""你是人形机器人行业趋势分析专家。请分析以下数据，识别本周的主要技术趋势和热点话题。

论文标题:
{chr(10).join([f"- {t}" for t in paper_titles[:10]])}

公司动态:
{chr(10).join([f"- {t}" for t in news_titles[:10]])}

请提供:
1. 3-5个主要技术趋势或热点话题
2. 每个趋势用1-2句话说明其重要性和影响

格式: 使用 markdown 列表"""

    try:
        response = analyzer.client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        analysis = response.content[0].text.strip()
        print("  ✓ Trend analysis generated")
        return analysis

    except Exception as e:
        print(f"  Error generating analysis: {e}")
        return "- 人形机器人技术持续发展\n- 多家公司发布产品更新\n- 学术界持续探索新方向"


def generate_report(data: Dict, report_type: str, analyzer) -> str:
    """
    Generate comprehensive report in markdown format.

    Args:
        data: Collected data dictionary
        report_type: 'daily' or 'weekly'
        analyzer: AI analyzer instance

    Returns:
        Markdown report content
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    week_str = datetime.now().strftime("%Y年第%W周")

    title = f"人形机器人行业{'周报' if report_type == 'weekly' else '日报'}"
    subtitle = week_str if report_type == "weekly" else date_str

    # Generate AI summaries
    executive_summary = generate_executive_summary(data, analyzer) if analyzer else "数据收集完成"
    trend_analysis = generate_trend_analysis(data, analyzer) if analyzer else ""

    # Build report
    content = f"""---
title: {title} - {subtitle}
date: {date_str}
type: report
---

# {title}
## {subtitle}

---

## 📊 数据概览

本期共收录:
- **学术论文**: {len(data['papers'])} 篇
- **公司动态**: {len(data['company_news'])} 条
- **行业资讯**: {len(data['wechat_articles'])} 篇

---

## 🎯 核心摘要

{executive_summary}

---

## 📈 趋势分析

{trend_analysis}

---

## 📚 学术前沿

本期收录 {len(data['papers'])} 篇高质量论文：

"""

    # Add top papers
    for i, paper in enumerate(data['papers'][:10], 1):
        analysis = paper.get('analysis', {})
        content += f"""### {i}. {paper['title']}

**相关性**: {paper.get('relevance_score', 'N/A')} | **发布日期**: {paper['published']}
**链接**: [{paper['arxiv_id']}]({paper['arxiv_url']})

**一句话摘要**: {analysis.get('summary', 'N/A')}

<details>
<summary>详细分析</summary>

**现状痛点**: {analysis.get('problems', 'N/A')}

**解决方案**: {analysis.get('solutions', 'N/A')}

**应用场景**: {analysis.get('applications', 'N/A')}

</details>

---

"""

    # Add company news
    content += f"""## 🏢 产业动态

本期收录 {len(data['company_news'])} 条公司动态：

"""

    # Group by company
    news_by_company = defaultdict(list)
    for news in data['company_news']:
        news_by_company[news['company']].append(news)

    for company, news_items in sorted(news_by_company.items()):
        content += f"\n### {company}\n\n"
        for news in news_items[:5]:
            content += f"""**{news['title']}**
- 发布时间: {news['published']}
- 链接: [{news['link']}]({news['link']})
- 简介: {news.get('ai_summary', news.get('original_summary', ''))[:150]}

"""

    # Add WeChat articles
    if data['wechat_articles']:
        content += f"""---

## 📱 行业资讯

本期收录 {len(data['wechat_articles'])} 篇微信文章：

"""

        for i, article in enumerate(data['wechat_articles'][:10], 1):
            content += f"""### {i}. {article['title']}

**公众号**: {article['author']} | **发布时间**: {article['published']}
**链接**: [阅读原文]({article['url']})

{article.get('ai_summary', article.get('summary', ''))[:200]}

---

"""

    # Footer
    content += f"""
---

## 📌 关于本报告

本报告由 **Humanoid Insight Platform** 自动生成，基于 Claude AI 的深度分析能力，汇总人形机器人领域的最新学术研究、产业动态和行业资讯。

**数据来源**:
- 学术论文: arXiv
- 公司动态: 官方网站和 RSS 订阅
- 行业资讯: 微信公众号

**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

*由 Claude AI 驱动 | [GitHub](https://github.com/yourusername/humanoid-insight-platform)*
"""

    return content


def save_report(content: str, output_dir: Path, report_type: str):
    """
    Save report to markdown file.

    Args:
        content: Report content
        output_dir: Output directory
        report_type: 'daily' or 'weekly'
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{report_type}-report-{date_str}.md"
    output_file = output_dir / filename

    output_file.write_text(content, encoding='utf-8')
    print(f"\n✓ Report saved to: {output_file}")


def main(report_type: str = "weekly"):
    """
    Main execution function.

    Args:
        report_type: Type of report - 'daily' or 'weekly'
    """
    print("=" * 60)
    print(f"Humanoid Robotics {report_type.capitalize()} Report Generation")
    print("=" * 60)

    # Setup paths
    project_root = Path(__file__).parent.parent
    cache_dir = project_root / "cache"
    docs_dir = project_root / "docs" / "reports"

    # Initialize AI analyzer
    print("\nInitializing AI analyzer...")
    try:
        analyzer = create_analyzer()
        print("✓ AI analyzer ready")
    except Exception as e:
        print(f"⚠ Warning: AI analyzer not available: {e}")
        print("Report will be generated without AI insights.")
        analyzer = None

    # Collect data
    print("\n" + "=" * 60)
    print("Collecting Data")
    print("=" * 60)

    days_back = 7 if report_type == "weekly" else 1
    data = collect_recent_data(cache_dir, days_back)

    # Check if we have data
    total_items = len(data['papers']) + len(data['company_news']) + len(data['wechat_articles'])
    if total_items == 0:
        print("\n⚠ No data found. Please run collection scripts first:")
        print("  - python scripts/collect_papers.py")
        print("  - python scripts/collect_company_news.py")
        print("  - python scripts/collect_wechat_articles.py")
        return

    # Generate report
    print("\n" + "=" * 60)
    print("Generating Report")
    print("=" * 60)

    report_content = generate_report(data, report_type, analyzer)

    # Save report
    print("\n" + "=" * 60)
    print("Saving Report")
    print("=" * 60)

    save_report(report_content, docs_dir, report_type)

    print("\n" + "=" * 60)
    print(f"✓ {report_type.capitalize()} report generation complete!")
    print("=" * 60)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate humanoid robotics reports")
    parser.add_argument(
        "--type",
        choices=["daily", "weekly"],
        default="weekly",
        help="Type of report to generate"
    )

    args = parser.parse_args()
    main(args.type)
