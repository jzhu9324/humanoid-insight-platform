"""
Tests for AI Analysis Utilities

Tests the AIAnalyzer class for relevance scoring and deep analysis.
"""

import pytest
import os
from unittest.mock import Mock, patch
from scripts.utils.ai_analyzer import AIAnalyzer, create_analyzer


class TestAIAnalyzer:
    """Test suite for AIAnalyzer class."""

    @pytest.fixture
    def mock_anthropic_client(self):
        """Create a mock Anthropic client."""
        with patch('scripts.utils.ai_analyzer.Anthropic') as mock_client:
            yield mock_client

    @pytest.fixture
    def analyzer(self, mock_anthropic_client):
        """Create an AIAnalyzer instance with mocked client."""
        return AIAnalyzer(api_key="test_key")

    def test_initialization_with_api_key(self, mock_anthropic_client):
        """Test AIAnalyzer initializes with provided API key."""
        analyzer = AIAnalyzer(api_key="test_api_key")
        mock_anthropic_client.assert_called_once_with(api_key="test_api_key")

    def test_initialization_with_env_var(self, mock_anthropic_client):
        """Test AIAnalyzer initializes with API key from environment."""
        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'env_api_key'}):
            analyzer = AIAnalyzer()
            mock_anthropic_client.assert_called_once_with(api_key='env_api_key')

    def test_score_relevance_returns_float(self, analyzer):
        """Test score_relevance returns a float between 0 and 1."""
        # Mock the API response
        mock_response = Mock()
        mock_response.content = [Mock(text="0.85")]
        analyzer.client.messages.create = Mock(return_value=mock_response)

        score = analyzer.score_relevance(
            title="Humanoid Robot Locomotion",
            abstract="This paper presents a novel approach to humanoid walking.",
            keywords=["humanoid locomotion", "walking"]
        )

        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0
        assert score == 0.85

    def test_score_relevance_clamps_values(self, analyzer):
        """Test score_relevance clamps values to [0, 1] range."""
        # Test upper bound clamping
        mock_response = Mock()
        mock_response.content = [Mock(text="1.5")]
        analyzer.client.messages.create = Mock(return_value=mock_response)

        score = analyzer.score_relevance("title", "abstract", ["keywords"])
        assert score == 1.0

        # Test lower bound clamping
        mock_response.content = [Mock(text="-0.5")]
        score = analyzer.score_relevance("title", "abstract", ["keywords"])
        assert score == 0.0

    def test_score_relevance_handles_invalid_response(self, analyzer):
        """Test score_relevance handles invalid API responses gracefully."""
        mock_response = Mock()
        mock_response.content = [Mock(text="invalid")]
        analyzer.client.messages.create = Mock(return_value=mock_response)

        score = analyzer.score_relevance("title", "abstract", ["keywords"])
        assert score == 0.0

    def test_analyze_paper_returns_dict(self, analyzer):
        """Test analyze_paper returns a dictionary with required fields."""
        mock_response = Mock()
        mock_response.content = [Mock(text='''```json
{
  "summary": "A novel approach to bipedal locomotion",
  "problems": "Current methods struggle with uneven terrain",
  "solutions": "Uses reinforcement learning with sim-to-real transfer",
  "applications": "Can be applied to real-world humanoid robots",
  "url": "https://arxiv.org/abs/2024.12345"
}
```''')]
        analyzer.client.messages.create = Mock(return_value=mock_response)

        result = analyzer.analyze_paper(
            title="Test Paper",
            abstract="Test abstract",
            arxiv_url="https://arxiv.org/abs/2024.12345"
        )

        assert isinstance(result, dict)
        assert "summary" in result
        assert "problems" in result
        assert "solutions" in result
        assert "applications" in result
        assert "url" in result

    def test_analyze_paper_extracts_json_from_markdown(self, analyzer):
        """Test analyze_paper extracts JSON from markdown code blocks."""
        mock_response = Mock()
        mock_response.content = [Mock(text='''```json
{
  "summary": "Test summary",
  "problems": "Test problems",
  "solutions": "Test solutions",
  "applications": "Test applications",
  "url": "https://arxiv.org/abs/2024.12345"
}
```''')]
        analyzer.client.messages.create = Mock(return_value=mock_response)

        result = analyzer.analyze_paper("title", "abstract", "https://arxiv.org/abs/2024.12345")

        assert result["summary"] == "Test summary"
        assert result["problems"] == "Test problems"

    def test_analyze_paper_handles_malformed_json(self, analyzer):
        """Test analyze_paper handles malformed JSON gracefully."""
        mock_response = Mock()
        mock_response.content = [Mock(text="not valid json")]
        analyzer.client.messages.create = Mock(return_value=mock_response)

        result = analyzer.analyze_paper(
            title="title",
            abstract="abstract",
            arxiv_url="https://arxiv.org/abs/2024.12345"
        )

        # Should return empty fields but preserve URL
        assert result["summary"] == ""
        assert result["problems"] == ""
        assert result["solutions"] == ""
        assert result["applications"] == ""
        assert result["url"] == "https://arxiv.org/abs/2024.12345"

    def test_analyze_paper_fills_missing_fields(self, analyzer):
        """Test analyze_paper fills in missing required fields."""
        mock_response = Mock()
        mock_response.content = [Mock(text='{"summary": "Test"}')]
        analyzer.client.messages.create = Mock(return_value=mock_response)

        result = analyzer.analyze_paper("title", "abstract", "https://arxiv.org/abs/2024.12345")

        assert "problems" in result
        assert "solutions" in result
        assert "applications" in result
        assert result["problems"] == ""


class TestCreateAnalyzer:
    """Test suite for create_analyzer factory function."""

    @patch('scripts.utils.ai_analyzer.Anthropic')
    def test_create_analyzer_returns_instance(self, mock_anthropic):
        """Test create_analyzer returns an AIAnalyzer instance."""
        analyzer = create_analyzer(api_key="test_key")
        assert isinstance(analyzer, AIAnalyzer)

    @patch('scripts.utils.ai_analyzer.Anthropic')
    def test_create_analyzer_uses_api_key(self, mock_anthropic):
        """Test create_analyzer passes API key to AIAnalyzer."""
        analyzer = create_analyzer(api_key="custom_key")
        mock_anthropic.assert_called_once_with(api_key="custom_key")
