"""
AI Analysis Utilities for Humanoid Insight Platform

This module provides AI-powered analysis capabilities using MiniMax API:
1. Relevance scoring (MiniMax-M2.5) - Quick filtering of papers
2. Deep analysis (MiniMax-M2.5) - Comprehensive 5-dimension analysis
"""

import os
from typing import Dict, Optional
from openai import OpenAI


class AIAnalyzer:
    """AI analyzer for paper relevance and deep content analysis."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI analyzer with MiniMax API.

        Args:
            api_key: MiniMax API key. If None, reads from MINIMAX_API_KEY env var.
        """
        api_key = api_key or os.environ.get("MINIMAX_API_KEY")
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.minimax.chat/v1"
        )

    def score_relevance(self, title: str, abstract: str, keywords: list[str]) -> float:
        """
        Score paper relevance using MiniMax-M2.5 (fast, cost-effective).

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

请直接返回数字分数（例如：0.8），不要包含任何其他文字、解释或思考过程。"""

        try:
            response = self.client.chat.completions.create(
                model="MiniMax-M2.5",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10,
                temperature=0.3
            )

            score_text = response.choices[0].message.content.strip()
            # Extract first number found
            import re
            numbers = re.findall(r'\d+\.?\d*', score_text)
            if numbers:
                score = float(numbers[0])
                # If score > 1, assume it's a percentage and divide by 100
                if score > 1:
                    score = score / 100
                return max(0.0, min(1.0, score))  # Clamp to [0, 1]
            return 0.5  # Default to medium relevance if can't parse

        except (ValueError, AttributeError, IndexError) as e:
            print(f"Warning: Failed to parse relevance score: {e}")
            return 0.5  # Default to medium relevance on error

    def analyze_paper(self, title: str, abstract: str, arxiv_url: str) -> Dict[str, str]:
        """
        Perform deep 5-dimension analysis using MiniMax-M2.5.

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
            response = self.client.chat.completions.create(
                model="MiniMax-M2.5",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1500,
                temperature=0.7
            )

            import json
            analysis_text = response.choices[0].message.content.strip()

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
        api_key: Optional API key. If None, uses MINIMAX_API_KEY env var.

    Returns:
        AIAnalyzer instance
    """
    return AIAnalyzer(api_key=api_key)
