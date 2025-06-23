"""Transaction Classification Agent implementation."""

import asyncio
import logging
from datetime import datetime
from typing import List, Optional

from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.prompts import ChatPromptTemplate
from langchain.schema import BaseMessage
from structlog import get_logger

from transaction_classification.config import settings
from transaction_classification.models.transaction import (
    ClassificationResult,
    TransactionInput,
    BatchClassificationRequest,
    BatchClassificationResponse,
)
from transaction_classification.chains.classification import create_classification_chain
from transaction_classification.utils.cache import CacheManager

logger = get_logger()


class TransactionClassifier:
    """Main transaction classification agent."""
    
    def __init__(
        self,
        model_name: Optional[str] = None,
        cache_manager: Optional[CacheManager] = None,
    ):
        """Initialize the transaction classifier.
        
        Args:
            model_name: Override default model name
            cache_manager: Optional cache manager instance
        """
        self.model_name = model_name or settings.classification_model
        self.cache_manager = cache_manager or CacheManager()
        self._llm = None
        self._chain = None
        
        logger.info(
            "Initialized TransactionClassifier",
            model=self.model_name,
            confidence_threshold=settings.confidence_threshold,
        )
    
    @property
    def llm(self):
        """Get or create LLM instance."""
        if self._llm is None:
            if self.model_name.startswith("gpt"):
                if not settings.has_openai:
                    raise ValueError("OpenAI API key not configured")
                self._llm = ChatOpenAI(
                    model_name=self.model_name,
                    temperature=0.1,
                    max_tokens=500,
                )
            elif self.model_name.startswith("claude"):
                if not settings.has_anthropic:
                    raise ValueError("Anthropic API key not configured")
                self._llm = ChatAnthropic(
                    model_name=self.model_name,
                    temperature=0.1,
                    max_tokens=500,
                )
            else:
                raise ValueError(f"Unsupported model: {self.model_name}")
        return self._llm
    
    @property
    def chain(self):
        """Get or create classification chain."""
        if self._chain is None:
            self._chain = create_classification_chain(self.llm)
        return self._chain
    
    async def classify_transaction(
        self,
        transaction: TransactionInput,
        include_reasoning: bool = False,
    ) -> ClassificationResult:
        """Classify a single transaction.
        
        Args:
            transaction: Transaction to classify
            include_reasoning: Whether to include LLM reasoning
            
        Returns:
            Classification result
        """
        # Check cache first
        cache_key = self.cache_manager.get_transaction_key(transaction)
        cached_result = await self.cache_manager.get(cache_key)
        if cached_result:
            logger.debug("Cache hit", transaction_id=transaction.id)
            return ClassificationResult(**cached_result)
        
        # Run classification
        start_time = datetime.utcnow()
        try:
            result = await self.chain.ainvoke({
                "description": transaction.description,
                "amount": str(transaction.amount),
                "date": transaction.date.isoformat(),
                "categories": ", ".join(settings.available_categories),
            })
            
            classification = ClassificationResult(
                transaction_id=transaction.id,
                category=result["category"],
                confidence=result["confidence"],
                merchant_name=result.get("merchant_name"),
                subcategory=result.get("subcategory"),
                tags=result.get("tags", []),
                reasoning=result.get("reasoning") if include_reasoning else None,
                model_used=self.model_name,
            )
            
            # Cache result
            await self.cache_manager.set(
                cache_key,
                classification.dict(),
                ttl=settings.cache_ttl
            )
            
            logger.info(
                "Transaction classified",
                transaction_id=transaction.id,
                category=classification.category,
                confidence=classification.confidence,
                duration_ms=(datetime.utcnow() - start_time).total_seconds() * 1000,
            )
            
            return classification
            
        except Exception as e:
            logger.error(
                "Classification failed",
                transaction_id=transaction.id,
                error=str(e),
                exc_info=True,
            )
            raise
    
    async def classify_batch(
        self,
        request: BatchClassificationRequest,
    ) -> BatchClassificationResponse:
        """Classify multiple transactions in batch.
        
        Args:
            request: Batch classification request
            
        Returns:
            Batch classification response
        """
        start_time = datetime.utcnow()
        results = []
        failed_count = 0
        
        # Process in batches to respect concurrency limits
        batches = [
            request.transactions[i:i + settings.max_concurrent_requests]
            for i in range(0, len(request.transactions), settings.max_concurrent_requests)
        ]
        
        for batch in batches:
            tasks = [
                self.classify_transaction(tx, request.include_reasoning)
                for tx in batch
            ]
            
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in batch_results:
                if isinstance(result, Exception):
                    failed_count += 1
                    logger.error("Batch item failed", error=str(result))
                else:
                    results.append(result)
        
        processing_time_ms = int(
            (datetime.utcnow() - start_time).total_seconds() * 1000
        )
        
        response = BatchClassificationResponse(
            results=results,
            total_processed=len(request.transactions),
            failed_count=failed_count,
            processing_time_ms=processing_time_ms,
        )
        
        logger.info(
            "Batch classification completed",
            total=response.total_processed,
            success_rate=response.success_rate,
            duration_ms=processing_time_ms,
        )
        
        return response
    
    async def get_categories(self) -> List[str]:
        """Get available transaction categories.
        
        Returns:
            List of category names
        """
        return settings.available_categories
    
    async def train_from_feedback(
        self,
        transaction: TransactionInput,
        correct_category: str,
        user_feedback: Optional[str] = None,
    ) -> None:
        """Update model with user corrections.
        
        Args:
            transaction: Original transaction
            correct_category: User-provided correct category
            user_feedback: Optional additional feedback
        """
        # Invalidate cache for this transaction
        cache_key = self.cache_manager.get_transaction_key(transaction)
        await self.cache_manager.delete(cache_key)
        
        # TODO: Implement feedback storage in Memory Cell
        logger.info(
            "Feedback received",
            transaction_id=transaction.id,
            correct_category=correct_category,
            has_feedback=bool(user_feedback),
        )