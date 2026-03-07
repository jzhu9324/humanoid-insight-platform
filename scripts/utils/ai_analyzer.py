"""
AI Analysis Utilities for Humanoid Insight Platform

This module provides AI-powered analysis capabilities using Claude API:
1. Relevance scoring (Claude Haiku) - Quick filtering of papers
2. Deep analysis (Claude Opus 4) - Comprehensive 5-dimension analysis
"""

import os
from typing import Dict, Optional
from anthropic import Anthropic


class AIAnalyzer:
    """AI analyzer for paper relevance and deep content analysis."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI analyzer with Claude API.

        Args:
            api_key: Anthropic API key. If None, reads from ANTHROPIC_API_KEY env var.
        """
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    def score_relevance(self, title: str, abstract: str, keywords: list[str]) -> float:
        """
        Score paper relevance using Claude Haiku (fast, cost-effective).

        Args:
            title: Paper title
            abstract: Paper abstract
            keywords: List of keywords to check relevance against

        Returns:
            Relevance score from 0.0 to 1.0
        """
        prompt = f"""你是一个人形机器人领域的专家。请评估以下论文与人形机器人技术的相关性。

关键词: {', '.join(keywords)}

论文标题: {title}

论文摘要: {abstract}

请给出一个0到1之间的相关性分数，其中:
- 0.0: 完全不相关
- 0.3: 略微相关
- 0.5: 中等相关
- 0.7: 高度相关
- 1.0: 核心相关

只返回数字分数，不需要解释。"""

        try:
            response = self.client.messages.create(
                model="claude-haiku-4-20250514",
                max_tokens=50,
                messages=[{"role": "user", "content": prompt}]
            )

            score_text = response.content[0].text.strip()
            score = float(score_text)
            return max(0.0, min(1.0, score))  # Clamp to [0, 1]

        except (ValueError, AttributeError, IndexError) as e:
            print(f"Warning: Failed to parse relevance score: {e}")
            return 0.0

    def analyze_paper(self, title: str, abstract: str, arxiv_url: str) -> Dict[str, str]:
        """
        Perform deep 5-dimension analysis using Claude Opus 4.

        Args:
            title: Paper title
            abstract: Paper abstract
            arxiv_url: URL to the paper on arXiv

        Returns:
            Dictionary with 5 analysis dimensions:
            - summary: One-sentence summary
            - problems: Current problems/pain points
            - solutions: Solutions and technical highlights
            - applications: Effects and application scenarios
            - url: Original paper URL
        """
        prompt = f"""你是一个人形机器人领域的资深专家。请对以下论文进行深度分析。

论文标题: {title}

论文摘要: {abstract}

请按以下5个维度进行分析，每个维度用一段话（50-100字）说明：

1. **一句话摘要**: 用一句话概括论文的核心贡献
2. **现状痛点**: 论文要解决的现有问题或技术瓶颈
3. **解决方案与技术亮点**: 论文提出的方法和创新点
4. **效果与应用场景**: 实验效果和潜在的实际应用
5. **论文链接**: {arxiv_url}

请严格按照以下JSON格式返回（不要包含其他文字）：
{{
  "summary": "一句话摘要内容",
  "problems": "现状痛点分析",
  "solutions": "解决方案与技术亮点",
  "applications": "效果与应用场景",
  "url": "{arxiv_url}"
}}"""

        try:
            response = self.client.messages.create(
                model="claude-opus-4-5-20251101",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )

            import json
            analysis_text = response.content[0].text.strip()

            # Try to extract JSON from markdown code blocks if present
            if "```json" in analysis_text:
                analysis_text = analysis_text.split("```json")[1].split("```")[0].strip()
            elif "```" in analysis_text:
                analysis_text = analysis_text.split("```")[1].split("```")[0].strip()

            analysis = json.loads(analysis_text)

            # Ensure all required fields are present
            required_fields = ["summary", "problems", "solutions", "applications", "url"]
            for field in required_fields:
                if field not in analysis:
                    analysis[field] = ""

            return analysis

        except (json.JSONDecodeError, AttributeError, IndexError) as e:
            print(f"Error: Failed to parse analysis: {e}")
            return {
                "summary": "",
                "problems": "",
                "solutions": "",
                "applications": "",
                "url": arxiv_url
            }


def create_analyzer(api_key: Optional[str] = None) -> AIAnalyzer:
    """
    Factory function to create an AIAnalyzer instance.

    Args:
        api_key: Optional API key. If None, uses ANTHROPIC_API_KEY env var.

    Returns:
        AIAnalyzer instance
    """
    return AIAnalyzer(api_key=api_key)
