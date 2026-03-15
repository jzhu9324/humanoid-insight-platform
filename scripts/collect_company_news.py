"""
Company News Collection Script for Humanoid Insight Platform

This script:
1. Collects news from major humanoid robotics companies
2. Fetches RSS feeds, blog posts, and press releases
3. Uses AI to analyze and summarize company updates
4. Saves results in VitePress-compatible format
"""

import os
import sys
import json
import feedparser
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from bs4 import BeautifulSoup

# Add utils directory to path for imports
sys.path.append(str(Path(__file__).parent / "utils"))
from ai_analyzer import create_analyzer


# Major humanoid robotics companies and their news sources (fallback)
COMPANIES = {
    "Tesla": {
        "rss_feeds": [
            "https://www.tesla.com/blog/rss",
        ],
        "keywords": ["optimus", "robot", "humanoid", "ai", "automation"]
    },
    "Boston Dynamics": {
        "rss_feeds": [
            "https://bostondynamics.com/blog/feed/",
        ],
        "keywords": ["atlas", "humanoid", "robot", "robotics"]
    },
    "Figure AI": {
        "website": "https://www.figure.ai/",
        "keywords": ["figure", "humanoid", "robot", "ai"]
    },
    "Agility Robotics": {
        "website": "https://agilityrobotics.com/news",
        "keywords": ["digit", "humanoid", "robot", "bipedal"]
    },
    "Sanctuary AI": {
        "website": "https://sanctuary.ai/news/",
        "keywords": ["phoenix", "humanoid", "robot", "ai"]
    },
    "Unitree Robotics": {
        "website": "https://www.unitree.com/",
        "keywords": ["humanoid", "robot", "h1", "g1"]
    }
}


def load_companies_from_config(config_path: Path) -> Dict:
    """
    Load companies configuration from JSON file.

    Args:
        config_path: Path to sources.json config file

    Returns:
        Dictionary of companies with their configurations
    """
    try:
        if not config_path.exists():
            print(f"⚠ Config file not found: {config_path}")
            print("  Using hardcoded companies as fallback")
            return COMPANIES

        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        companies = {}
        for company in config.get('companies', []):
            name = company.get('name')
            if not name:
                continue

            rss_feeds = company.get('rss_feeds', [])

            # 如果没有配置 RSS，自动生成 Google News RSS
            if not rss_feeds:
                query = f"{name} humanoid robot"
                auto_rss = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"
                rss_feeds = [auto_rss]
                print(f"  ℹ {name}: 无 RSS 配置，自动使用 Google News 搜索")

            companies[name] = {
                'keywords': company.get('keywords', []),
                'website': company.get('website', ''),
                'rss_feeds': rss_feeds
            }

        print(f"✓ Loaded {len(companies)} companies from config file")
        return companies

    except Exception as e:
        print(f"⚠ Error loading config: {e}")
        print("  Using hardcoded companies as fallback")
        return COMPANIES


def fetch_rss_feed(feed_url: str, days_back: int = 7) -> List[Dict]:
    """
    Fetch and parse RSS feed.

    Args:
        feed_url: URL of the RSS feed
        days_back: How many days back to fetch

    Returns:
        List of feed entries with metadata
    """
    try:
        print(f"  Fetching RSS feed: {feed_url}")
        feed = feedparser.parse(feed_url)

        # Filter by date
        cutoff_date = datetime.now() - timedelta(days=days_back)
        entries = []

        for entry in feed.entries:
            # Parse publish date
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                pub_date = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                pub_date = datetime(*entry.updated_parsed[:6])
            else:
                pub_date = datetime.now()

            # Check if within date range
            if pub_date >= cutoff_date:
                entries.append({
                    "title": entry.get('title', 'No title'),
                    "link": entry.get('link', ''),
                    "published": pub_date.strftime("%Y-%m-%d"),
                    "summary": entry.get('summary', entry.get('description', ''))[:500]
                })

        print(f"    Found {len(entries)} recent entries")
        return entries

    except Exception as e:
        print(f"    Error fetching RSS feed: {e}")
        return []


def fetch_website_news(url: str, keywords: List[str]) -> List[Dict]:
    """
    Scrape news from company website (basic implementation).

    Args:
        url: Website URL
        keywords: Keywords to look for

    Returns:
        List of news items
    """
    try:
        print(f"  Fetching website: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Simple extraction - look for article/news elements
        # Note: This is a basic implementation. Each website may need custom parsing.
        articles = []

        # Try common HTML patterns
        for tag in ['article', 'div']:
            elements = soup.find_all(tag, class_=lambda x: x and any(
                kw in str(x).lower() for kw in ['news', 'blog', 'post', 'article']
            ))

            for elem in elements[:5]:  # Limit to first 5
                title_elem = elem.find(['h1', 'h2', 'h3', 'a'])
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    link = title_elem.get('href', '') if title_elem.name == 'a' else ''

                    # Make link absolute
                    if link and not link.startswith('http'):
                        from urllib.parse import urljoin
                        link = urljoin(url, link)

                    articles.append({
                        "title": title,
                        "link": link,
                        "published": datetime.now().strftime("%Y-%m-%d"),
                        "summary": ""
                    })

        print(f"    Found {len(articles)} articles")
        return articles[:3]  # Return top 3

    except Exception as e:
        print(f"    Error fetching website: {e}")
        return []


def collect_company_news(company_name: str, config: Dict, days_back: int = 7) -> List[Dict]:
    """
    Collect news for a specific company.

    Args:
        company_name: Name of the company
        config: Company configuration with feeds/websites
        days_back: How many days back to collect

    Returns:
        List of news items
    """
    print(f"\n[{company_name}]")
    all_news = []

    # Fetch RSS feeds
    if "rss_feeds" in config:
        for feed_url in config["rss_feeds"]:
            entries = fetch_rss_feed(feed_url, days_back)
            all_news.extend(entries)

    # Fetch website news
    if "website" in config and not config.get("rss_feeds"):
        news = fetch_website_news(config["website"], config["keywords"])
        all_news.extend(news)

    return all_news


def analyze_news_with_ai(news_items: List[Dict], company_name: str, analyzer) -> List[Dict]:
    """
    Analyze news items using AI.

    Args:
        news_items: List of raw news items
        company_name: Company name
        analyzer: AI analyzer instance

    Returns:
        List of analyzed news with AI summaries
    """
    analyzed_news = []

    for item in news_items:
        try:
            # Create analysis prompt
            prompt = f"""你是人形机器人行业分析专家。请分析以下来自 {company_name} 的新闻动态。

标题: {item['title']}
链接: {item['link']}
摘要: {item.get('summary', 'N/A')}

请用1-2句话（50字以内）总结这条新闻的关键信息和对人形机器人行业的意义。

要求：
1. 直接输出摘要内容，不要包含任何思考过程
2. 不要使用 <think> 标签
3. 简洁明了，突出关键信息"""

            response = analyzer.client.chat.completions.create(
                model="MiniMax-M2.5",
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )

            ai_summary = response.choices[0].message.content.strip()

            # 移除 <think> 标签及其内容
            import re
            ai_summary = re.sub(r'<think>.*?</think>', '', ai_summary, flags=re.DOTALL)
            ai_summary = ai_summary.strip()

            analyzed_news.append({
                "company": company_name,
                "title": item["title"],
                "link": item["link"],
                "published": item["published"],
                "original_summary": item.get("summary", ""),
                "ai_summary": ai_summary
            })

            print(f"    ✓ Analyzed: {item['title'][:50]}...")

        except Exception as e:
            print(f"    ✗ Error analyzing news: {e}")
            # Add without AI summary
            analyzed_news.append({
                "company": company_name,
                "title": item["title"],
                "link": item["link"],
                "published": item["published"],
                "original_summary": item.get("summary", ""),
                "ai_summary": ""
            })

    return analyzed_news


def save_news_to_markdown(news_items: List[Dict], output_dir: Path):
    """
    Save company news to markdown files for VitePress.

    Args:
        news_items: List of analyzed news items
        output_dir: Directory to save markdown files
    """
    if not news_items:
        print("\nNo news to save.")
        return

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename with date
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_file = output_dir / f"company-news-{date_str}.md"

    # Group by company and filter valid items
    by_company = {}
    valid_count = 0
    for item in news_items:
        # 只统计有完整信息的新闻
        if not item['link'] or item['link'] == '' or not item['title'] or item['title'].strip() == '':
            continue
        # 如果摘要提示信息不完整，跳过
        if '无法从给定信息' in item.get('ai_summary', '') or '建议提供完整' in item.get('ai_summary', ''):
            continue

        company = item["company"]
        if company not in by_company:
            by_company[company] = []
        by_company[company].append(item)
        valid_count += 1

    # Build markdown content
    content = f"""---
title: 人形机器人公司动态 - {date_str}
date: {date_str}
type: company-news
---

# 人形机器人公司动态 - {date_str}

本期收录 {len(by_company)} 家公司的 {valid_count} 条动态。

"""

    for company, items in by_company.items():
        content += f"""## {company}

"""
        for item in items:
            content += f"""### {item['title']}

**发布日期**: {item['published']}
**链接**: [查看原文]({item['link']})

{item['ai_summary'] if item['ai_summary'] else item['original_summary'][:200]}

---

"""

    # Write to file
    output_file.write_text(content, encoding='utf-8')
    print(f"\n✓ Saved {len(news_items)} news items to {output_file}")


def save_news_to_json(news_items: List[Dict], output_dir: Path):
    """
    Save company news to JSON for backup/processing.

    Args:
        news_items: List of news items
        output_dir: Directory to save JSON file
    """
    if not news_items:
        return

    # Create cache directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename with date
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_file = output_dir / f"company-news-{date_str}.json"

    # Write JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(news_items, f, ensure_ascii=False, indent=2)

    print(f"✓ Saved JSON backup to {output_file}")


def main():
    """Main execution function."""
    print("=" * 60)
    print("Humanoid Robotics Company News Collection")
    print("=" * 60)

    # Setup paths
    project_root = Path(__file__).parent.parent
    docs_dir = project_root / "docs" / "company-news"
    cache_dir = project_root / "cache" / "company-news"
    config_file = project_root / "config" / "sources.json"

    # Load companies from config file
    print("\nLoading companies configuration...")
    companies = load_companies_from_config(config_file)

    # Initialize AI analyzer
    print("\nInitializing AI analyzer...")
    try:
        analyzer = create_analyzer()
        print("✓ AI analyzer ready")
    except Exception as e:
        print(f"✗ Failed to initialize analyzer: {e}")
        print("Note: AI analysis will be skipped if API key is not available.")
        analyzer = None

    # Collect news from all companies
    all_news = []
    days_back = 2  # 每2天更新

    print("\n" + "=" * 60)
    print("Collecting Company News")
    print("=" * 60)

    for company_name, config in companies.items():
        news_items = collect_company_news(company_name, config, days_back)

        # Analyze with AI if available
        if analyzer and news_items:
            print(f"  Analyzing {len(news_items)} items with AI...")
            analyzed = analyze_news_with_ai(news_items, company_name, analyzer)
            all_news.extend(analyzed)
        else:
            # Add without AI analysis
            for item in news_items:
                all_news.append({
                    "company": company_name,
                    "title": item["title"],
                    "link": item["link"],
                    "published": item["published"],
                    "original_summary": item.get("summary", ""),
                    "ai_summary": ""
                })

    # Save results
    print("\n" + "=" * 60)
    print("Saving Results")
    print("=" * 60)

    save_news_to_markdown(all_news, docs_dir)
    save_news_to_json(all_news, cache_dir)

    print("\n" + "=" * 60)
    print(f"✓ Collection complete! Processed {len(all_news)} news items from {len(companies)} companies.")
    print("=" * 60)

    # 更新首页最新内容
    print("\nUpdating homepage latest updates...")
    try:
        import subprocess
        subprocess.run([
            'python3',
            str(project_root / 'scripts' / 'generate_latest_updates.py')
        ], check=True)
    except Exception as e:
        print(f"⚠ Failed to update homepage: {e}")


if __name__ == "__main__":
    main()
