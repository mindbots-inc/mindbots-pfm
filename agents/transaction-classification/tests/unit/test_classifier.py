"""Unit tests for TransactionClassifier."""

import pytest
from unittest.mock import AsyncMock, Mock, patch

from transaction_classification.agents.classifier import TransactionClassifier
from transaction_classification.models.transaction import (
    BatchClassificationRequest,
    BatchClassificationResponse,
    ClassificationResult,
    TransactionInput,
)


class TestTransactionClassifier:
    """Test TransactionClassifier functionality."""
    
    @pytest.fixture
    def classifier(self, mock_cache_manager):
        """Create classifier instance with mocked dependencies."""
        with patch("transaction_classification.agents.classifier.settings") as mock_settings:
            mock_settings.classification_model = "gpt-4"
            mock_settings.has_openai = True
            mock_settings.available_categories = ["restaurants", "groceries", "transportation"]
            mock_settings.confidence_threshold = 0.85
            mock_settings.cache_ttl = 3600
            mock_settings.max_concurrent_requests = 10
            
            classifier = TransactionClassifier(
                model_name="gpt-4",
                cache_manager=mock_cache_manager
            )
            return classifier
    
    @pytest.mark.asyncio
    async def test_classify_transaction_success(
        self,
        classifier,
        sample_transaction,
        mock_openai_response,
        mock_cache_manager,
    ):
        """Test successful transaction classification."""
        # Mock the chain
        mock_chain = AsyncMock()
        mock_chain.ainvoke.return_value = mock_openai_response
        
        with patch.object(classifier, "chain", mock_chain):
            result = await classifier.classify_transaction(sample_transaction)
        
        # Verify result
        assert isinstance(result, ClassificationResult)
        assert result.category == "restaurants"
        assert result.confidence == 0.95
        assert result.merchant_name == "Starbucks"
        assert result.transaction_id == "tx_123"
        
        # Verify chain was called
        mock_chain.ainvoke.assert_called_once()
        
        # Verify cache was used
        mock_cache_manager.get.assert_called_once()
        mock_cache_manager.set.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_classify_transaction_with_cache_hit(
        self,
        classifier,
        sample_transaction,
        mock_cache_manager,
    ):
        """Test classification with cache hit."""
        # Mock cache hit
        cached_result = {
            "transaction_id": "tx_123",
            "category": "restaurants",
            "confidence": 0.95,
            "merchant_name": "Starbucks",
            "model_used": "gpt-4",
            "classified_at": "2025-06-23T10:00:00",
        }
        mock_cache_manager.get.return_value = cached_result
        
        result = await classifier.classify_transaction(sample_transaction)
        
        # Verify result from cache
        assert result.category == "restaurants"
        assert result.confidence == 0.95
        
        # Verify chain was not called
        with patch.object(classifier, "chain") as mock_chain:
            mock_chain.ainvoke.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_classify_batch_success(
        self,
        classifier,
        sample_transactions,
        mock_openai_response,
    ):
        """Test batch classification."""
        # Mock the chain
        mock_chain = AsyncMock()
        mock_chain.ainvoke.return_value = mock_openai_response
        
        with patch.object(classifier, "chain", mock_chain):
            request = BatchClassificationRequest(transactions=sample_transactions)
            response = await classifier.classify_batch(request)
        
        # Verify response
        assert isinstance(response, BatchClassificationResponse)
        assert response.total_processed == 5
        assert response.failed_count == 0
        assert response.success_rate == 1.0
        assert len(response.results) == 5
        
        # Verify all results
        for result in response.results:
            assert isinstance(result, ClassificationResult)
            assert result.category == "restaurants"
    
    @pytest.mark.asyncio
    async def test_classify_batch_with_failures(
        self,
        classifier,
        sample_transactions,
    ):
        """Test batch classification with some failures."""
        # Mock chain to fail on second transaction
        mock_chain = AsyncMock()
        mock_chain.ainvoke.side_effect = [
            {"category": "groceries", "confidence": 0.9, "merchant_name": "Whole Foods"},
            Exception("API Error"),
            {"category": "entertainment", "confidence": 0.85, "merchant_name": "Netflix"},
            {"category": "transportation", "confidence": 0.92, "merchant_name": "Shell"},
            {"category": "income", "confidence": 0.99, "merchant_name": "ACME Corp"},
        ]
        
        with patch.object(classifier, "chain", mock_chain):
            request = BatchClassificationRequest(transactions=sample_transactions)
            response = await classifier.classify_batch(request)
        
        # Verify response
        assert response.total_processed == 5
        assert response.failed_count == 1
        assert response.success_rate == 0.8
        assert len(response.results) == 4
    
    @pytest.mark.asyncio
    async def test_get_categories(self, classifier):
        """Test getting available categories."""
        categories = await classifier.get_categories()
        
        assert isinstance(categories, list)
        assert "restaurants" in categories
        assert "groceries" in categories
        assert "transportation" in categories
    
    @pytest.mark.asyncio
    async def test_train_from_feedback(
        self,
        classifier,
        sample_transaction,
        mock_cache_manager,
    ):
        """Test training from user feedback."""
        await classifier.train_from_feedback(
            sample_transaction,
            correct_category="groceries",
            user_feedback="This is actually a grocery store"
        )
        
        # Verify cache was invalidated
        mock_cache_manager.delete.assert_called_once()
    
    def test_model_selection_openai(self):
        """Test OpenAI model selection."""
        with patch("transaction_classification.agents.classifier.settings") as mock_settings:
            mock_settings.has_openai = True
            mock_settings.classification_model = "gpt-4"
            
            classifier = TransactionClassifier(model_name="gpt-4")
            
            with patch("transaction_classification.agents.classifier.ChatOpenAI") as mock_openai:
                _ = classifier.llm
                mock_openai.assert_called_once_with(
                    model_name="gpt-4",
                    temperature=0.1,
                    max_tokens=500,
                )
    
    def test_model_selection_anthropic(self):
        """Test Anthropic model selection."""
        with patch("transaction_classification.agents.classifier.settings") as mock_settings:
            mock_settings.has_anthropic = True
            mock_settings.classification_model = "claude-3"
            
            classifier = TransactionClassifier(model_name="claude-3")
            
            with patch("transaction_classification.agents.classifier.ChatAnthropic") as mock_anthropic:
                _ = classifier.llm
                mock_anthropic.assert_called_once_with(
                    model_name="claude-3",
                    temperature=0.1,
                    max_tokens=500,
                )
    
    def test_model_selection_unsupported(self):
        """Test unsupported model raises error."""
        classifier = TransactionClassifier(model_name="unsupported-model")
        
        with pytest.raises(ValueError, match="Unsupported model"):
            _ = classifier.llm