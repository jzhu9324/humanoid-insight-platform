"""
Tests for paper collection script.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / "scripts"))

import pytest
from unittest.mock import Mock, patch, MagicMock
from collect_papers import (
    search_arxiv_papers,
    filter_and_analyze_papers,
    save_papers_to_markdown,
    HUMANOID_KEYWORDS,
    RELEVANCE_THRESHOLD
)


def test_humanoid_keywords_exist():
    """Test that humanoid keywords are defined."""
    assert len(HUMANOID_KEYWORDS) > 0
    assert "humanoid robot" in HUMANOID_KEYWORDS


def test_relevance_threshold():
    """Test that relevance threshold is in valid range."""
    assert 0.0 <= RELEVANCE_THRESHOLD <= 1.0


@patch('collect_papers.arxiv.Search')
def test_search_arxiv_papers(mock_search):
    """Test arXiv paper search."""
    # Mock arXiv results
    mock_result = Mock()
    mock_result.title = "Test Humanoid Paper"
    mock_result.summary = "Test abstract"

    mock_search_instance = Mock()
    mock_search_instance.results.return_value = [mock_result]
    mock_search.return_value = mock_search_instance

    # Execute search
    papers = search_arxiv_papers("test query", max_results=10, days_back=7)

    # Verify
    assert len(papers) == 1
    assert papers[0].title == "Test Humanoid Paper"


def test_filter_and_analyze_papers():
    """Test paper filtering and analysis."""
    # Mock paper
    mock_paper = Mock()
    mock_paper.title = "Humanoid Robot Control"
    mock_paper.summary = "A novel approach to humanoid robot control"
    mock_paper.entry_id = "http://arxiv.org/abs/2401.12345"
    mock_paper.pdf_url = "http://arxiv.org/pdf/2401.12345"
    mock_paper.published = Mock()
    mock_paper.published.strftime.return_value = "2024-01-15"
    mock_paper.categories = ["cs.RO"]

    mock_author = Mock()
    mock_author.name = "John Doe"
    mock_paper.authors = [mock_author]

    # Mock analyzer
    mock_analyzer = Mock()
    mock_analyzer.score_relevance.return_value = 0.8
    mock_analyzer.analyze_paper.return_value = {
        "summary": "Test summary",
        "problems": "Test problems",
        "solutions": "Test solutions",
        "applications": "Test applications",
        "url": "http://arxiv.org/abs/2401.12345"
    }

    # Execute
    papers = filter_and_analyze_papers([mock_paper], mock_analyzer)

    # Verify
    assert len(papers) == 1
    assert papers[0]["title"] == "Humanoid Robot Control"
    assert papers[0]["relevance_score"] == 0.8
    assert "analysis" in papers[0]


def test_filter_skips_low_relevance():
    """Test that low relevance papers are skipped."""
    # Mock low relevance paper
    mock_paper = Mock()
    mock_paper.title = "Unrelated Paper"
    mock_paper.summary = "Not about humanoid robots"

    # Mock analyzer with low score
    mock_analyzer = Mock()
    mock_analyzer.score_relevance.return_value = 0.2

    # Execute
    papers = filter_and_analyze_papers([mock_paper], mock_analyzer)

    # Verify - should be empty
    assert len(papers) == 0


def test_save_papers_to_markdown(tmp_path):
    """Test saving papers to markdown format."""
    # Mock paper data
    papers = [{
        "title": "Test Paper",
        "authors": ["Author 1", "Author 2"],
        "published": "2024-01-15",
        "arxiv_id": "2401.12345",
        "arxiv_url": "http://arxiv.org/abs/2401.12345",
        "pdf_url": "http://arxiv.org/pdf/2401.12345",
        "relevance_score": 0.85,
        "categories": ["cs.RO"],
        "analysis": {
            "summary": "Test summary",
            "problems": "Test problems",
            "solutions": "Test solutions",
            "applications": "Test applications"
        }
    }]

    # Save to temporary directory
    save_papers_to_markdown(papers, tmp_path)

    # Verify file was created
    md_files = list(tmp_path.glob("papers-*.md"))
    assert len(md_files) == 1

    # Verify content
    content = md_files[0].read_text(encoding='utf-8')
    assert "Test Paper" in content
    assert "Author 1" in content
    assert "2401.12345" in content


def test_save_papers_to_markdown_empty(tmp_path):
    """Test that empty paper list doesn't create files."""
    save_papers_to_markdown([], tmp_path)

    # Verify no files created
    md_files = list(tmp_path.glob("papers-*.md"))
    assert len(md_files) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
