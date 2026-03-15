"""
WeChat Public Account Collection Script for Humanoid Insight Platform

This script collects articles from WeChat public accounts (公众号) related to humanoid robotics.

Note: WeChat has strict API access requirements. This script provides:
1. Manual URL input method for WeChat article links
2. Integration with third-party WeChat article aggregators (if available)
3. Placeholder for future WeChat API integration
"""

import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import re

# Add utils directory to path for imports
sys.path.append(str(Path(__file__).parent / "utils"))
from ai_analyzer import create_analyzer


# WeChat public accounts to monitor (account names) - fallback
WECHAT_ACCOUNTS = [
    "机器人大讲堂",
    "机器人在线",
    "高工机器人",
    "智东西",
    "量子位",
    "机器之心",
    "新智元",
    "36氪",
    "钛媒体"
]

# Keywords for filtering humanoid content - fallback
HUMANOID_KEYWORDS = [
    "人形机器人", "人型机器人", "仿人机器人",
    "Optimus", "Tesla Bot", "特斯拉机器人",
    "Figure", "Atlas", "Digit",
    "波士顿动力", "Boston Dynamics",
    "具身智能", "embodied AI"
]


def load_wechat_config(config_path: Path) -> tuple[List[str], List[str]]:
    """
    Load WeChat accounts and keywords from JSON config file.

    Args:
        config_path: Path to sources.json config file

    Returns:
        Tuple of (account_names, keywords)
    """
    try:
        if not config_path.exists():
            print(f"⚠ Config file not found: {config_path}")
            print("  Using hardcoded accounts and keywords as fallback")
            return WECHAT_ACCOUNTS, HUMANOID_KEYWORDS

        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        wechat_accounts = config.get('wechat_accounts', [])

        if not wechat_accounts:
            print("⚠ No WeChat accounts found in config file")
            print("  Using hardcoded accounts and keywords as fallback")
            return WECHAT_ACCOUNTS, HUMANOID_KEYWORDS

        # Extract account names and combine all keywords
        account_names = []
        all_keywords = set()

        for account in wechat_accounts:
            name = account.get('name')
            if name:
                account_names.append(name)

            keywords = account.get('keywords', [])
            all_keywords.update(keywords)

        keywords_list = list(all_keywords)

        print(f"✓ Loaded {len(account_names)} WeChat accounts and {len(keywords_list)} keywords from config file")
        return account_names, keywords_list

    except Exception as e:
        print(f"⚠ Error loading config: {e}")
        print("  Using hardcoded accounts and keywords as fallback")
        return WECHAT_ACCOUNTS, HUMANOID_KEYWORDS


def parse_wechat_article_url(url: str) -> Optional[Dict]:
    """
    Parse a WeChat article from its URL.

    Args:
        url: WeChat article URL (mp.weixin.qq.com)

    Returns:
        Article metadata dict or None
    """
    try:
        print(f"  Parsing WeChat article: {url[:60]}...")

        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
        }

        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            print(f"    Error: HTTP {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract title
        title_elem = soup.find('h1', class_='rich_media_title')
        title = title_elem.get_text(strip=True) if title_elem else "未知标题"

        # Extract author/account
        author_elem = soup.find('a', class_='rich_media_meta_link')
        author = author_elem.get_text(strip=True) if author_elem else "未知公众号"

        # Extract publish time
        time_elem = soup.find('em', id='publish_time')
        publish_time = time_elem.get_text(strip=True) if time_elem else datetime.now().strftime("%Y-%m-%d")

        # Extract content summary (first 200 chars)
        content_elem = soup.find('div', class_='rich_media_content')
        if content_elem:
            content_text = content_elem.get_text(strip=True)
            summary = content_text[:200] + "..." if len(content_text) > 200 else content_text
        else:
            summary = ""

        print(f"    ✓ Parsed: {title[:40]}...")

        return {
            "title": title,
            "author": author,
            "published": publish_time,
            "url": url,
            "summary": summary
        }

    except Exception as e:
        print(f"    Error parsing article: {e}")
        return None


def check_article_relevance(article: Dict, keywords: List[str]) -> bool:
    """
    Check if article is relevant to humanoid robotics.

    Args:
        article: Article metadata dict
        keywords: List of keywords to check

    Returns:
        True if relevant, False otherwise
    """
    text = f"{article['title']} {article['summary']}".lower()

    for keyword in keywords:
        if keyword.lower() in text:
            return True

    return False


def analyze_wechat_article(article: Dict, analyzer) -> Dict:
    """
    Analyze WeChat article using AI.

    Args:
        article: Article metadata
        analyzer: AI analyzer instance

    Returns:
        Article with AI analysis
    """
    try:
        prompt = f"""你是人形机器人行业分析专家。请分析以下来自微信公众号的文章。

标题: {article['title']}
作者: {article['author']}
摘要: {article['summary'][:300]}

请用2-3句话（100字以内）总结这篇文章的核心观点和对人形机器人行业的意义。"""

        response = analyzer.client.messages.create(
            model="claude-haiku-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )

        ai_summary = response.content[0].text.strip()

        return {
            **article,
            "ai_summary": ai_summary
        }

    except Exception as e:
        print(f"    Error analyzing article: {e}")
        return {
            **article,
            "ai_summary": ""
        }


def load_wechat_urls_from_file(file_path: Path) -> List[str]:
    """
    Load WeChat article URLs from a text file.

    Args:
        file_path: Path to file containing URLs (one per line)

    Returns:
        List of URLs
    """
    if not file_path.exists():
        print(f"  No URL file found at {file_path}")
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and line.strip().startswith('http')]

        print(f"  Loaded {len(urls)} URLs from file")
        return urls

    except Exception as e:
        print(f"  Error reading URL file: {e}")
        return []


def collect_wechat_articles(url_file: Path, analyzer, keywords: List[str]) -> List[Dict]:
    """
    Collect and analyze WeChat articles.

    Args:
        url_file: Path to file with WeChat article URLs
        analyzer: AI analyzer instance
        keywords: List of keywords for relevance filtering

    Returns:
        List of analyzed articles
    """
    print("\nCollecting WeChat articles...")

    # Load URLs from file
    urls = load_wechat_urls_from_file(url_file)

    if not urls:
        print("\n提示: 请在以下文件中添加微信文章链接（每行一个）:")
        print(f"  {url_file}")
        print("\n示例:")
        print("  https://mp.weixin.qq.com/s/xxxxx")
        print("  https://mp.weixin.qq.com/s/yyyyy")
        return []

    articles = []

    for url in urls:
        # Parse article
        article = parse_wechat_article_url(url)

        if not article:
            continue

        # Check relevance
        if not check_article_relevance(article, keywords):
            print(f"    Skipped: Not relevant to humanoid robotics")
            continue

        # Analyze with AI
        if analyzer:
            print(f"    Analyzing with AI...")
            article = analyze_wechat_article(article, analyzer)

        articles.append(article)

    return articles


def save_articles_to_markdown(articles: List[Dict], output_dir: Path):
    """
    Save WeChat articles to markdown files for VitePress.

    Args:
        articles: List of analyzed articles
        output_dir: Directory to save markdown files
    """
    if not articles:
        print("\nNo articles to save.")
        return

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename with date
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_file = output_dir / f"wechat-articles-{date_str}.md"

    # Build markdown content
    content = f"""---
title: 微信公众号精选 - {date_str}
date: {date_str}
type: wechat-articles
---

# 微信公众号精选 - {date_str}

本期收录 {len(articles)} 篇优质文章。

"""

    for i, article in enumerate(articles, 1):
        content += f"""## {i}. {article['title']}

**公众号**: {article['author']}
**发布时间**: {article['published']}
**链接**: [阅读原文]({article['url']})

### AI 分析总结

{article.get('ai_summary', article.get('summary', 'N/A')[:200])}

---

"""

    # Write to file
    output_file.write_text(content, encoding='utf-8')
    print(f"\n✓ Saved {len(articles)} articles to {output_file}")


def save_articles_to_json(articles: List[Dict], output_dir: Path):
    """
    Save WeChat articles to JSON for backup/processing.

    Args:
        articles: List of articles
        output_dir: Directory to save JSON file
    """
    if not articles:
        return

    # Create cache directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename with date
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_file = output_dir / f"wechat-articles-{date_str}.json"

    # Write JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"✓ Saved JSON backup to {output_file}")


def create_example_url_file(file_path: Path):
    """
    Create an example URL file if it doesn't exist.

    Args:
        file_path: Path to create the example file
    """
    if file_path.exists():
        return

    file_path.parent.mkdir(parents=True, exist_ok=True)

    example_content = """# 微信公众号文章链接
# 每行一个链接，以 http 或 https 开头
#
# 示例:
# https://mp.weixin.qq.com/s/xxxxxxxxxxxxx
# https://mp.weixin.qq.com/s/yyyyyyyyyyyyy
#
# 关注以下公众号的人形机器人相关文章:
# - 机器人大讲堂
# - 机器人在线
# - 高工机器人
# - 智东西
# - 量子位
# - 机器之心
# - 新智元

"""

    file_path.write_text(example_content, encoding='utf-8')
    print(f"Created example URL file: {file_path}")


def main():
    """Main execution function."""
    print("=" * 60)
    print("WeChat Public Account Article Collection")
    print("=" * 60)

    # Setup paths
    project_root = Path(__file__).parent.parent
    docs_dir = project_root / "docs" / "wechat"
    cache_dir = project_root / "cache" / "wechat"
    url_file = project_root / "config" / "wechat_urls.txt"
    config_file = project_root / "config" / "sources.json"

    # Load WeChat configuration
    print("\nLoading WeChat configuration...")
    account_names, keywords = load_wechat_config(config_file)

    # Create example URL file if needed
    create_example_url_file(url_file)

    # Initialize AI analyzer
    print("\nInitializing AI analyzer...")
    try:
        analyzer = create_analyzer()
        print("✓ AI analyzer ready")
    except Exception as e:
        print(f"⚠ Warning: AI analyzer not available: {e}")
        analyzer = None

    # Collect and analyze articles
    print("\n" + "=" * 60)
    print("Collecting WeChat Articles")
    print("=" * 60)

    articles = collect_wechat_articles(url_file, analyzer, keywords)

    # Save results
    if articles:
        print("\n" + "=" * 60)
        print("Saving Results")
        print("=" * 60)

        save_articles_to_markdown(articles, docs_dir)
        save_articles_to_json(articles, cache_dir)

        print("\n" + "=" * 60)
        print(f"✓ Collection complete! Processed {len(articles)} articles.")
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
    else:
        print("\n" + "=" * 60)
        print("No articles collected.")
        print(f"Please add WeChat article URLs to: {url_file}")
        print("=" * 60)


if __name__ == "__main__":
    main()
