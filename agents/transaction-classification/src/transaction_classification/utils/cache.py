"""Cache management for transaction classification."""

import hashlib
import json
from typing import Any, Optional

import redis.asyncio as redis
from structlog import get_logger

from transaction_classification.config import settings
from transaction_classification.models.transaction import TransactionInput

logger = get_logger()


class CacheManager:
    """Manage caching for classification results."""
    
    def __init__(self, redis_url: Optional[str] = None):
        """Initialize cache manager.
        
        Args:
            redis_url: Override default Redis URL
        """
        self.redis_url = redis_url or settings.redis_url
        self._redis = None
        self._connected = False
    
    async def connect(self) -> None:
        """Connect to Redis."""
        if not self._connected:
            try:
                self._redis = await redis.from_url(
                    self.redis_url,
                    encoding="utf-8",
                    decode_responses=True,
                )
                await self._redis.ping()
                self._connected = True
                logger.info("Connected to Redis cache")
            except Exception as e:
                logger.warning(f"Failed to connect to Redis: {e}")
                self._redis = None
                self._connected = False
    
    async def disconnect(self) -> None:
        """Disconnect from Redis."""
        if self._redis and self._connected:
            await self._redis.close()
            self._connected = False
            logger.info("Disconnected from Redis cache")
    
    def get_transaction_key(self, transaction: TransactionInput) -> str:
        """Generate cache key for a transaction.
        
        Args:
            transaction: Transaction to generate key for
            
        Returns:
            Cache key string
        """
        # Create a deterministic key based on transaction properties
        key_data = {
            "description": transaction.description.lower().strip(),
            "amount": str(transaction.amount),
            "date": transaction.date.date().isoformat(),
            "currency": transaction.currency,
        }
        
        key_str = json.dumps(key_data, sort_keys=True)
        key_hash = hashlib.sha256(key_str.encode()).hexdigest()[:16]
        
        return f"tx_class:{key_hash}"
    
    async def get(self, key: str) -> Optional[dict]:
        """Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None
        """
        if not self._connected:
            await self.connect()
        
        if not self._redis:
            return None
        
        try:
            value = await self._redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.warning(f"Cache get error: {e}")
            return None
    
    async def set(
        self,
        key: str,
        value: dict,
        ttl: Optional[int] = None,
    ) -> bool:
        """Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds
            
        Returns:
            True if successful
        """
        if not self._connected:
            await self.connect()
        
        if not self._redis:
            return False
        
        try:
            value_str = json.dumps(value)
            if ttl:
                await self._redis.setex(key, ttl, value_str)
            else:
                await self._redis.set(key, value_str)
            return True
        except Exception as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if successful
        """
        if not self._connected:
            await self.connect()
        
        if not self._redis:
            return False
        
        try:
            await self._redis.delete(key)
            return True
        except Exception as e:
            logger.warning(f"Cache delete error: {e}")
            return False
    
    async def clear_pattern(self, pattern: str) -> int:
        """Clear all keys matching pattern.
        
        Args:
            pattern: Key pattern to match
            
        Returns:
            Number of keys deleted
        """
        if not self._connected:
            await self.connect()
        
        if not self._redis:
            return 0
        
        try:
            keys = []
            async for key in self._redis.scan_iter(match=pattern):
                keys.append(key)
            
            if keys:
                return await self._redis.delete(*keys)
            return 0
        except Exception as e:
            logger.warning(f"Cache clear error: {e}")
            return 0